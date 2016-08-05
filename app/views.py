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

cfg = Config('app.cfg')
app = Flask(__name__)


def login_required(func):
    def inner(*args, **kwargs):
        login_data = dict(request.form.items())
        user_digest = make_digest(
            login_data['username'], login_data['password'])
        login_controller = controllers.LoginController(login_data['username'])
        session['user_digest'] = user_digest
        if session['user_digest'] == login_controller.get_user_digest(
            login_data['username'], user_digest):
            session['logged_in'] = True
            return func(message='You have successfully logged in', *args, **kwargs)
        else:
            return func(message='Could not log in', *args, **kwargs)
    return inner


class IndexView(MethodView):

    def get(self):
        if not 'logged_in' in session:
            session['logged_in'] = False
        logged_in = session['logged_in']
        return render_template('index.html', logged_in=logged_in)


class LoginView(MethodView):

    def get(self):
        return render_template('login.html')

    @login_required
    def post(self, message=''):
        logged_in = session['logged_in']
        login_data = dict(request.form.items())
        user_data = controllers.LoginController(login_data['username']).user
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get(user_data['_id'])
        return render_template('balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities,
            logged_in=logged_in)


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

    def get(self, _id=None):
        logged_in = session['logged_in']
        if request.endpoint == 'balance_sheet-delete':
            self.post(_id)

        user_data = controllers.LoginController(login_data['username']).user
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get(user_data['_id'])
        return render_template(
            'balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities,
            logged_in=logged_in)

    def post(self, _id=None):
        user_data = controllers.LoginController(login_data['username']).user
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get(user_data['_id'])

        data = dict(request.form.items())
        if request.endpoint == 'balance_sheet':
            if any([key for key in data if 'assets_form' in key]):
                assets + data
            elif any([key for key in data if 'liablities_form' in key]):
                liabilities + data
            elif any([key for key in data if 'equities_form' in key]):
                equities + data
        elif request.endpoint == 'balance_sheet-update':
            if any([key for key in data if 'assets_form' in key]):
                assets += (_id, data)
            elif any([key for key in data if 'liablities_form' in key]):
                liabilities += (_id, data)
            elif any([key for key in data if 'equities_form' in key]):
                equities += (_id, data)
        elif request.endpoint == 'balance_sheet-delete':
            if _id in assets:
                assets - _id
            elif _id in liabilities:
                liabilities - _id
            elif _id in equities:
                equities - _id

        user_data = controllers.LoginController(login_data['username']).user
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get(user_data['_id'])
        return render_template('balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities,
            logged_in=logged_in)
