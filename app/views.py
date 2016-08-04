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
    abort
)
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
        login_controller = controllers.LoginController()
        session['user_digest'] = user_digest
        if session['user_digest'] == login_controller.validate_user_digest(
            login_data['username'], user_digest):
            return func(message='You have successfully logged in', *args, **kwargs)
        else:
            return func(message='Could not log in', *args, **kwargs)
    return inner


class IndexView(MethodView):

    def get(self):
        return render_template('index.html')


class LoginView(MethodView):

    def get(self):
        return render_template('login.html')

    @login_required
    def post(self, message=''):
        data = dict(request.form.items())
        message = 'Username: {}, Password: {}'.format(data['username'], data['password'])
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()
        print assets, liabilities, equities        
        return render_template('balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities)


class AccountsView(MethodView):

    def get(self, account_name=None):
        account = repr(accounts.Account(account_name))
        return render_template(
            'accounts/index.html',
            accounts=repr(accounts.Accounts()),
            account=account,
            account_name=account_name)

    def post(self, account_name=None):
        data = dict(request.form)
        pprint(data)
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
        if request.endpoint == 'balance_sheet-delete':
            self.post(_id)

        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()
        return render_template(
            'balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities)

    def post(self, _id=None):
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()

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

        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()
        return render_template('balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities)
