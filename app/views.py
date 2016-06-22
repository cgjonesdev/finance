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
        account = repr(base.Account(account_name))
        return render_template(
            'accounts/index.html',
            accounts=repr(base.Accounts()),
            account=account,
            account_name=account_name)

    def post(self, account_name=None):
        name = request.form.get('account_name')
        if name and name not in [account[0] for account in base.Accounts()]:
            base.Accounts().add_account(name)
            return render_template('accounts/index.html',
                                    accounts=sorted(base.Accounts()),
                                    account_name=None)
        else:
            if not account_name:
                return redirect('/accounts')
            else:
                return redirect('/accounts/{}'.format(account_name))
