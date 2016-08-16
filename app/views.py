import sys
import os
import logging
import time
import re
import hmac
from pprint import pprint, pformat
from datetime import timedelta
from operator import itemgetter
from flask import (
    Flask,
    render_template,
    request,
    session,
    make_response,
    redirect,
    url_for,
    abort)
from flask.views import MethodView
import controllers
from config import Config
from crypt import make_digest
from logger import logger

cfg = Config('configs/app.cfg')
app = Flask(__name__)


def login_required(func):
    def inner(*args, **kwargs):
        session['referrer'] = request.url
        if 'user_digest' in session:
            user_is_valid = controllers.LoginController(session['user_digest'])
            return func(*args, **kwargs) if user_is_valid else redirect('/login')
        return redirect('/login')
    return inner


class IndexView(MethodView):

    def get(self):
        user = controllers.LoginController(session.get('user_digest')).user
        return render_template(
            'index.html', logged_in=session.get('logged_in'), user=user)


class SignupView(MethodView):
    context = {}

    def get(self):
        self.context.update(
            {'message': 'Enter an email address or phone number'
                ' to receive a verification email or text to activate your account',
             'tiny_message': 'If you enter a phone number, you will receive a '
                'verification text to set up your account'})
        return render_template(
            'signup.html', **self.context)

    def post(self):
        users = controllers.SignupController().users
        signup_data = dict(request.form.items())
        user_digest = make_digest(
            signup_data['username'], signup_data['password'])
        del signup_data['password']
        signup_data['user_digest'] = user_digest
        users + signup_data
        session['user_digest'], session['logged_in'] = user_digest, True
        return redirect('/welcome')


class WelcomeView(MethodView):

    def get(self):
        user = controllers.WelcomeController(session['user_digest']).user
        return render_template('welcome.html', user=user)


class LoginView(MethodView):
    context = {'message': '', 'color': 'black'}

    def get(self):
        return render_template('login.html')

    def post(self, message=''):
        login_data = dict(request.form.items())
        user_digest = make_digest(
            login_data['username'], login_data['password'])
        if controllers.LoginController(user_digest).user:
            session['user_digest'], session['logged_in'] = user_digest, True
            referrer = session.get('referrer') if not any(
                item for item in ('None', 'logout') if item in
                str(session.get('referrer'))) else '/'
            if 'referrer' in session:
                del session['referrer']
            return redirect(referrer)
        else:
            self.context.update(
                {'message': 'The login credentials you provided are not '
                 'correct. Please try again',
                 'color': 'red'})
            return render_template('login.html', **self.context)


class LogoutView(MethodView):

    def get(self):
        session.clear()
        return render_template('index.html')


class AccountsView(MethodView):

    def get(self, account_name=None):
        account = repr(accounts.Account(account_name))
        return render_template(
            'accounts/index.html',
            accounts=repr(accounts.Accounts()),
            account=account,
            account_name=account_name)

    def post(self, account_name=None):
        data = dict(request.form.items())
        if data['method'] == 'delete':
            accounts.Account(account_name).delete()
            return redirect('/accounts')
        elif data['method'] == 'update':
            if account_name not in [account[0] for account in accounts.Accounts()]:
                accounts.Accounts().add(name)
                return render_template('accounts/index.html',
                                        accounts=repr(accounts.Accounts()),
                                        account_name=None)
        elif data and 'name' not in data:
            accounts.Account(account_name).update(data)
            return redirect('/accounts/{}'.format(account_name))
        else:
            if not account_name:
                return redirect('/accounts')
            else:
                return redirect('/accounts/{}'.format(account_name))

class BalanceSheetView(MethodView):
    context = {
        'user': None,
        'assets': [],
        'liabilities': [],
        'equities': [],
        'logged_in': False}

    def __init__(self, *args, **kwargs):
        MethodView.__init__(self, *args, **kwargs)
        self.retrieve_data()

    @login_required
    def retrieve_data(self):
        user = controllers.LoginController(session['user_digest']).user
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get(str(user._id))
        self.update_context(
            user=user,
            assets=assets,
            liabilities=liabilities,
            equities=equities,
            logged_in=session.get('logged_in'))
        self.__dict__.update(self.context)

    def update_context(self, **kwargs):
        self.context.update(kwargs)

    @login_required
    def get(self, _id=None):
        if request.endpoint == 'balance_sheet-detail':
            self.retrieve_data()
            if _id in self.assets:
                self.entity = self.assets[_id]
            elif _id in self.liabilities:
                self.entity = self.liabilities[_id]
            elif _id in self.equities:
                self.entity = self.equities[_id]
            else:
                self.entity = None
            self.update_context(**self.__dict__)
            return render_template(
                'balance_sheet_detail.html', **self.context)
        elif request.endpoint == 'balance_sheet-delete':
            self.post(_id)
        return render_template('balance_sheet.html', **self.context)

    @login_required
    def post(self, _id=None):
        self.__dict__.update(self.context)
        data = dict(request.form.items())
        logger.debug('data: {}, request.endpoint: {}'.format(data, request.endpoint))
        if request.endpoint == 'balance_sheet':
            if any([key for key in data if 'assets_form' in key]):
                self.assets + data
            elif any([key for key in data if 'liabilities_form' in key]):
                self.liabilities + data
            elif any([key for key in data if 'equities_form' in key]):
                self.equities + data
        elif request.endpoint == 'balance_sheet-update':
            if any([key for key in data if 'asset' in key]):
                data.update(vars(self.assets[_id]))
                self.assets += (_id, data)
            elif any([key for key in data if 'liabilit' in key]):
                data.update(vars(self.liabilities[_id]))
                self.liabilities += (_id, data)
            elif any([key for key in data if 'equit' in key]):
                data.update(vars(self.equities[_id]))
                self.equities += (_id, data)
        elif request.endpoint == 'balance_sheet-delete':
            if _id in self.assets:
                self.assets - _id
            elif _id in self.liabilities:
                self.liabilities - _id
            elif _id in self.equities:
                self.equities - _id
        self.retrieve_data()
        self.update_context(**self.__dict__)
        if any([key for key in data if 'detail' in key]):
            return render_template('balance_sheet_detail.html', **self.context)
        return render_template('balance_sheet.html', **self.context)
