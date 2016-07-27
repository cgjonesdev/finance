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
from code.accounts import accounts


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

    def get(self):
        return render_template('balance_sheet.html')
