from models.users import Users, User
from models.balance_sheet import Assets, Liabilities, Equities
from code.budget import Budget
from logger import logger


class IndexController(object):
    pass


class SignupController(object):
    users = Users()


class LoginController(object):

    def __init__(self, user_digest=None):
        self.user = Users().get_by_digest(user_digest)

    def __nonzero__(self):
        return bool(self.user)


class BalanceSheetController(object):

    def get(self, user_id):
        assets, liabilities = Assets(user_id), Liabilities(user_id)
        return assets, liabilities, Equities(user_id, assets, liabilities)


class BudgetController(object):

    def __init__(self, user_digest):
        self.user = LoginController(user_digest).user
        self.budget = Budget(str(self.user._id))

    def refresh_equitiies(self, assets, liabilities):
        self.budget.assets = assets
        self.budget.liabilities = liabilities
        self.budget.equities = Equities(str(self.user._id), assets, liabilities)
        return self.budget
