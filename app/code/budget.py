from finance.app.models.users import *
from finance.app.models.balance_sheet import *
from finance.app.logger import logger


class Budget(object):

    def __init__(self, user_id):
        self.assets = Assets(user_id)
        self.liabilities = Liabilities(user_id)
        self.equities = Equities(user_id, self.assets, self.liabilities)

    @property
    def bills(self):
        return self.liabilities.cycle_total

    @property
    def savings(self):
        return round(self.equities.total * self.savings_calculation_ratio, 2)

    @property
    def spending(self):
        return round(self.equities.total - self.savings, 2)

    @property
    def liability_to_asset_ratio(self):
        try:
            return self.liabilities.cycle_total / self.assets.cycle_total
        except ZeroDivisionError:
            return 0.0

    @property
    def asset_to_liability_ratio(self):
        try:
            return self.assets.cycle_total / self.liabilities.cycle_total
        except ZeroDivisionError:
            return 0.0

    @property
    def savings_calculation_ratio(self):
        return 1 - (self.liability_to_asset_ratio ** 2)

    @property
    def savings_ratio(self):
        try:
            return self.savings / self.assets.cycle_total
        except ZeroDivisionError:
            return 0.0


if __name__ == '__main__':
    users = Users()
    user_index = 4
    user = list(users)[user_index]
    print vars(user)
    budget = Budget(str(user._id))
    logger.debug(
        (user.username,
         budget.assets.total,
         budget.bills,
         budget.savings,
         budget.spending,
         budget.savings + budget.spending))
