from datetime import timedelta
from flask import Flask, session
import views
from finance.app import cfg


app = Flask(__name__)
app.config['SECRET_KEY'] = cfg['SECRET_KEY']
app.permanent_session_lifetime = timedelta(minutes=int(cfg['SESSION_LIFETIME']))

# Url resolvers
app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
app.add_url_rule('/signup', view_func=views.SignupView.as_view('signup'), methods=['GET', 'POST'])
app.add_url_rule('/welcome', view_func=views.WelcomeView.as_view('welcome'))
app.add_url_rule('/login', view_func=views.LoginView.as_view('login'), methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=views.LogoutView.as_view('logout'))
app.add_url_rule('/accounts', view_func=views.AccountsView.as_view('accounts'))
app.add_url_rule('/accounts/<string:account_name>', view_func=views.AccountsView.as_view('accounts_byname'))
app.add_url_rule('/balance_sheet', view_func=views.BalanceSheetView.as_view('balance_sheet'), methods=['GET', 'POST'])
app.add_url_rule('/balance_sheet/<string:_id>', view_func=views.BalanceSheetView.as_view('balance_sheet-detail'))
app.add_url_rule('/balance_sheet/<string:_id>/update', view_func=views.BalanceSheetView.as_view('balance_sheet-update'))
app.add_url_rule('/balance_sheet/<string:_id>/delete', view_func=views.BalanceSheetView.as_view('balance_sheet-delete'))
app.add_url_rule('/budget', view_func=views.BudgetView.as_view('budget'))
app.add_url_rule('/budget/<string:time_frame>', view_func=views.BudgetView.as_view('budget-time_frame'))
