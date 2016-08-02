from pprint import pprint

from code.balance_sheet import *


class IndexController(object):
    pass


class BalanceSheetController(object):

    def get(self):
        assets = Assets()
        liabilities = Liabilities()
        equities = Equities(assets, liabilities)
        return assets, liabilities, equities
