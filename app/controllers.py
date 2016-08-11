from code.users import Users, User
from code.balance_sheet import Assets, Liabilities, Equities
from code.data import DataConnector
from logger import logger


class IndexController(object):
    pass


class SignupController(object):

    def __init__(self):
        self.users = Users()


class WelcomeController(object):

    def __init__(self, user_digest):
        self.users = Users()
        self.user = self.users.get_by_digest(user_digest)


class LoginController(object):

    def __init__(self, user_digest):
        self.users = Users()
        self.user = self.users.get_by_digest(user_digest)


class BalanceSheetController(object):

    def get(self, user_id):
        assets, liabilities = Assets(user_id), Liabilities(user_id)
        return assets, liabilities, Equities(user_id, assets, liabilities)
