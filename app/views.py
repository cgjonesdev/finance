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

cfg = Config('app.cfg')
app = Flask(__name__)


def login_required(func):
    def inner(*args, **kwargs):
        session['referrer'] = request.url
        if 'user_digest' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return inner


class IndexView(MethodView):

    def get(self):
        return render_template(
            'index.html', logged_in=session.get('logged_in'))


class SignupView(MethodView):

    def get(self):
        return render_template(
            'signup.html',
            message='Enter an email address to receive a verification email or '
            'phone # to receive a verification text to activate your account')

    def post(self):
        users = controllers.SignupController().users
        signup_data = dict(request.form.items())
        logger.debug(signup_data)
        user_digest = make_digest(
            signup_data['username'], signup_data['password'])
        signup_data['name'] = signup_data['username']
        del signup_data['username'], signup_data['password']
        signup_data['user_digest'] = user_digest
        users + signup_data
        session['user_digest'], session['logged_in'] = user_digest, True
        return render_template('signup.html', signup_data=signup_data)


class WelcomeView(MethodView):

    def get(self):
        user = controllers.WelcomeController(session.get('user_digest')).user
        return render_template('welcome.html', user=user)


class LoginView(MethodView):

    def get(self):
        if 'user_digest' in session:
            return redirect(request.referrer)
        if not 'referrer' in session:
            session['referrer'] = request.referrer
        return render_template('login.html')

    def post(self, message=''):
        login_data = dict(request.form.items())
        user_digest = make_digest(
            login_data['username'], login_data['password'])
        login_controller = controllers.LoginController(user_digest)
        session['user_digest'], session['logged_in'] = user_digest, True
        referrer = session.get('referrer') if not any(
            item for item in ('None', 'logout') if item in
            str(session.get('referrer'))) else '/'
        if 'referrer' in session:
            del session['referrer']
        return redirect(referrer)


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

    def __init__(self, *args, **kwargs):
        MethodView.__init__(self, *args, **kwargs)
        self.user = controllers.LoginController(session['user_digest']).user
        self.assets, self.liabilities, self.equities = controllers.BalanceSheetController()\
            .get(str(self.user._id))

    @login_required
    def get(self, _id=None):
        if request.endpoint == 'balance_sheet-delete':
            self.post(_id)

        return render_template(
            'balance_sheet.html',
            assets=self.assets,
            liabilities=self.liabilities,
            equities=self.equities,
            logged_in=session.get('logged_in'))

    def post(self, _id=None):
        data = dict(request.form.items())
        if request.endpoint == 'balance_sheet':
            if any([key for key in data if 'assets_form' in key]):
                self.assets + data
            elif any([key for key in data if 'liablities_form' in key]):
                self.liabilities + data
            elif any([key for key in data if 'equities_form' in key]):
                self.equities + data
        elif request.endpoint == 'balance_sheet-update':
            if any([key for key in data if 'assets_form' in key]):
                self.assets += (_id, data)
            elif any([key for key in data if 'liablities_form' in key]):
                self.liabilities += (_id, data)
            elif any([key for key in data if 'equities_form' in key]):
                self.equities += (_id, data)
        elif request.endpoint == 'balance_sheet-delete':
            if _id in assets:
                self.assets - _id
            elif _id in liabilities:
                self.liabilities - _id
            elif _id in equities:
                self.equities - _id
        return render_template('balance_sheet.html',
            assets=self.assets,
            liabilities=self.liabilities,
            equities=self.equities,
            logged_in=session.get('logged_in'))
