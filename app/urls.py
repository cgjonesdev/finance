from datetime import timedelta
from flask import Flask, session
import views
from config import Config

cfg = Config('app.cfg')


app = Flask(__name__)
app.config['SECRET_KEY'] = cfg['SECRET_KEY']
app.permanent_session_lifetime = timedelta(hours=int(cfg['SESSION_LIFETIME']))

# Url resolvers
app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
app.add_url_rule('/login', view_func=views.LoginView.as_view('login'))
app.add_url_rule('/accounts', view_func=views.AccountsView.as_view('accounts'))
app.add_url_rule('/accounts/<string:account_name>', view_func=views.AccountsView.as_view('accounts_byname'))
app.add_url_rule('/balance_sheet', view_func=views.BalanceSheetView.as_view('balance_sheet'), methods=['GET', 'POST'])
app.add_url_rule('/balance_sheet/<string:_id>/update', view_func=views.BalanceSheetView.as_view('balance_sheet-update'))
app.add_url_rule('/balance_sheet/<string:_id>/delete', view_func=views.BalanceSheetView.as_view('balance_sheet-delete'))
