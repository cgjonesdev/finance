from datetime import timedelta
from flask import Flask, session
import views


app = Flask(__name__)
app.config['SECRET_KEY'] = ('zpbAIZMjLy0sCxIZ0wYDPixd31ipYLI4sTfvy2wyteZzBeQs'
                            'yg5O9Q7v5f78Yf6abjQwrgfJjQOUfNRFuLuMiJ0BpDALESrn'
                            '5qMVVlqiNJUGKGRRWXmjXJAor3ACtGq6')
app.permanent_session_lifetime = timedelta(hours=2)

# Url resolvers
app.add_url_rule('/', view_func=views.IndexView.as_view('index'))
app.add_url_rule('/accounts', view_func=views.AccountsView.as_view('accounts'))
app.add_url_rule('/accounts/<string:account_name>', view_func=views.AccountsView.as_view('accounts_byname'))
app.add_url_rule('/balance_sheet', view_func=views.BalanceSheetView.as_view('balance_sheet'))
