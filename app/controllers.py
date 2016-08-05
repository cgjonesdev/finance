from code.balance_sheet import *
from code.data import DataConnector


class IndexController(object):
    pass


class LoginController(object):
    dc = DataConnector('users')

    def __init__(self, username):
        self.user = self.dc.get_by_name(username)

    def get_user_digest(self, username, user_digest):
        if self.user:
            return self.user['user_digest']


class BalanceSheetController(object):

    def get(self, user_id):
        assets, liabilities = Assets(user_id), Liabilities(user_id)
        return assets, liabilities, Equities(user_id, assets, liabilities)
