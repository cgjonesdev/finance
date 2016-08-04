from code.balance_sheet import *
from code.data import DataConnector


class IndexController(object):
    pass


class LoginController(object):

    def validate_user_digest(self, username, user_digest):
        dc = DataConnector('users')
        user = dc.get_by_name(username)
        if user:
            return user['user_digest']




class BalanceSheetController(object):

    def get(self):
        assets, liabilities = Assets(), Liabilities()
        return assets, liabilities, Equities(assets, liabilities)

