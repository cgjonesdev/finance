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
from bson import ObjectId
import controllers
from finance.app import cfg
from crypt import make_digest
from logger import logger

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
    controller = controllers.IndexController

    def get(self):
        user = controllers.LoginController(session.get('user_digest')).user
        return render_template(
            'index.html', logged_in=session.get('logged_in'), user=user)


class SignupView(MethodView):
    controller = controllers.SignupController
    context = {}

    def get(self):
        self.context.update(
            {'message': 'Enter an email address or phone number'
                ' to receive a verification email or text',
             'tiny_message': 'If you enter a phone number, you will receive a '
                'verification text to set up your account'})
        return render_template(
            'signup.html', **self.context)

    def post(self):
        users = self.controller().users
        signup_data = dict(request.form.items())
        user_digest = make_digest(
            signup_data['username'], signup_data['password'])
        del signup_data['password']
        signup_data['user_digest'] = user_digest
        users + signup_data
        session['user_digest'], session['logged_in'] = user_digest, True
        return redirect('/welcome')


class WelcomeView(MethodView):
    controller = controllers.LoginController

    @login_required
    def get(self):
        user = self.controller(session.get('user_digest')).user
        return render_template('welcome.html', user=user)


class LoginView(MethodView):
    controller = controllers.LoginController
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
    controller = controllers.BalanceSheetController
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
    def retrieve_data(self, _id=None):
        user = controllers.LoginController(session['user_digest']).user
        assets, liabilities, equities = self.controller().get(str(user._id))
        time_frame_keys = list(assets)[0].cycle._time_frame_keys if list(assets) else ()
        if _id in time_frame_keys:
            time_frame = _id
            for asset in assets:
                asset.cycle.time_frame = time_frame
            for liability in liabilities:
                liability.cycle.time_frame = time_frame
            equities = self.controller().refresh_equitiies(
                str(user._id), assets, liabilities)

        if _id in assets:
            entity = assets[_id]
        elif _id in liabilities:
            entity = liabilities[_id]
        elif _id in equities:
            entity = equities[_id]
        else:
            entity = None

        self.update_context(
            user=user,
            assets=assets,
            liabilities=liabilities,
            equities=equities,
            entity=entity,
            session_time_frame=session.get('time_frame'),
            time_frames=time_frame_keys,
            logged_in=session.get('logged_in'),
            message=self.message if hasattr(self, 'message') else '')

    def update_context(self, **kwargs):
        self.__dict__.update(kwargs)
        self.context.update(self.__dict__)

    @login_required
    def get(self, _id=None):
        if request.endpoint == 'balance_sheet-detail':
            self.retrieve_data(_id)
            self.update_context()
            try:
                ObjectId(_id)
                return render_template(
                    'balance_sheet_detail.html', **self.context)
            except:
                return render_template(
                    'balance_sheet.html', **self.context)
        elif request.endpoint == 'balance_sheet-delete':
            self.post(_id)
        return render_template('balance_sheet.html', **self.context)

    @login_required
    def post(self, _id=None):
        self.__dict__.update(self.context)
        data = dict(request.form.items())
        if request.endpoint == 'balance_sheet':
            if any([key for key in data if 'assets_form' in key]):
                self.assets + data
            elif any([key for key in data if 'liabilities_form' in key]):
                self.liabilities + data
            elif any([key for key in data if 'equities_form' in key]):
                self.equities + data
        elif request.endpoint == 'balance_sheet-update':
            if any([key for key in data if 'asset' in key]):
                if hasattr(self.assets[_id], 'one_time') and 'one_time' not in data:
                    self.assets[_id].one_time = False
                self.assets += (_id, data)
                self.message = '{}'.format(self.assets[_id].name)
            elif any([key for key in data if 'liabilit' in key]):
                if hasattr(self.liabilities[_id], 'one_time') and 'one_time' not in data:
                    self.liabilities[_id].one_time = False
                self.liabilities += (_id, data)
                self.message = '{}'.format(self.liabilities[_id].name)
            elif any([key for key in data if 'equit' in key]):
                if hasattr(self.equities[_id], 'one_time') and 'one_time' not in data:
                    self.equities[_id].one_time = False
                self.equities += (_id, data)
                self.message = '{}'.format(self.equities[_id].name)
        elif request.endpoint == 'balance_sheet-delete':
            if _id in self.assets:
                self.assets - _id
            elif _id in self.liabilities:
                self.liabilities - _id
            elif _id in self.equities:
                self.equities - _id
        self.retrieve_data(_id)
        self.update_context()
        if any([key for key in data if 'detail' in key]):
            return render_template('balance_sheet_detail.html', **self.context)
        return render_template('balance_sheet.html', **self.context)


class BudgetView(MethodView):
    controller = controllers.BudgetController
    context = {}

    @login_required
    def get(self, time_frame='monthly'):
        self.retrieve_data()
        for asset in self.budget.assets:
            asset.cycle.time_frame = time_frame
        for liability in self.budget.liabilities:
            liability.cycle.time_frame = time_frame
        self.budget = self.controller(
            session.get('user_digest')).refresh_equitiies(
                self.budget.assets, self.budget.liabilities)
        self.update_context(budget=self.budget)
        return render_template('budget.html', **self.context)

    @login_required
    def retrieve_data(self, _id=None):
        user = controllers.LoginController(session.get('user_digest')).user
        budget = self.controller(session.get('user_digest')).budget
        time_frame_keys = (list(budget.assets)[0].cycle._time_frame_keys if
                           list(budget.assets) else ())
        self.update_context(
            user=user,
            budget=budget,
            session_time_frame=session.get('time_frame'),
            time_frames=time_frame_keys,
            logged_in=session.get('logged_in'))

    def update_context(self, **kwargs):
        self.__dict__.update(kwargs)
        self.context.update(self.__dict__)


class BurnrateView(MethodView):
    controller = controllers.BurnrateController
    context = {}

    @login_required
    def get(self):
        self.retrieve_data()
        self.update_context()
        return render_template('burnrate.html', **self.context)

    @login_required
    def retrieve_data(self):
        user = controllers.LoginController(session['user_digest']).user
        self.update_context(
            user=user,
            logged_in=session.get('logged_in'))

    def update_context(self, **kwargs):
        self.__dict__.update(kwargs)
        self.context.update(self.__dict__)
