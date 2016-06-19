import os
import logging
import time
import re
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
from code.accounts import base


app = Flask(__name__)


class IndexView(MethodView):

    def get(self):
        return render_template('index.html')


class AccountsView(MethodView):

    def get(self, account_name=None):
        account = None
        if account_name:
            account = base.Account(account_name).account
        return render_template(
            'accounts/index.html',
            accounts=sorted(base.Accounts()),
            account_name=account_name,
            account=account)

    def post(self, account_name=None):
        account_name = request.form.get('account_name')
        if account_name and account_name not in [account[0] for account in base.Accounts()]:
            base.Accounts().add_account(account_name)
            return render_template('accounts/index.html',
                                    accounts=sorted(base.Accounts()),
                                    account_name=None)
        else:
            return redirect('/accounts')
