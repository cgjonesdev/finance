import os
import logging
import time
import re
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

app = Flask(__name__)


class IndexView(MethodView):

    def get(self):
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

    def get(self, name=None):
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()
        return render_template(
            'balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities)

    def post(self, name=None, endpoint=None):
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
        elif request.endpoint == 'balance-sheet-update':
            if any([key for key in data if 'assets_form' in key]):
                assets += data
            elif any([key for key in data if 'liablities_form' in key]):
                liabilities += data
            elif any([key for key in data if 'equities_form' in key]):
                equities += data
        assets, liabilities, equities = controllers.BalanceSheetController()\
            .get()
        return render_template('balance_sheet.html',
            assets=assets,
            liabilities=liabilities,
            equities=equities)
