from data import DataConnector


class Base(object):
    _dataconnector = DataConnector('finance', 'balance_sheet')


class BalanceSheet(object):

    def __init__(self):
        self.assets = []
        self.liabilities = []

    def __iter__(self):
        return (x for x in self.assets + self.liabilities)

    def __add__(self, object):
        if isinstance(object, Assets):
            self.assets.extend(object)

        if isinstance(object, Liabilities):
            self.liabilities.extend(object)


class Multi(Base):

    def __init__(self):
        self.items = []
        self._total = 0.0

    def __iter__(self):
        return (x for x in self.items)

    def __add__(self, other):
        self.items.append(other)

    def __sub__(self, other):
        try:
            self.items.remove(other)
        except:
            raise IndexError('{} is not in the list'.format(other))

    def sum(self):
        return sum(item.amount for item in self)

    @property
    def total(self):
        return sum(x.amount for x in self)

    def save(self):
        for item in self:
            self._dataconnector + vars(item)


class Singleton(Base):

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def save(self):
        self._dataconnector + vars(self)



class Assets(Multi):
    pass


class Asset(Singleton):
    pass


class Liabilities(Multi):
    pass


class Liability(Singleton):
    pass


class Equities(Multi):
    pass


class Equity(Singleton):
    pass


if __name__ == '__main__':
    assets = Assets()
    assets + Asset('job', 5000.0)
    assets + Asset('investments', 200.0)
    print assets.total
    liabilities = Liabilities()
    liabilities + Liability('rent', 0.0)
    print liabilities.total
    from pprint import pprint
    pprint(vars(assets))
    pprint(vars(liabilities))

    balance_sheet = BalanceSheet()
    balance_sheet + assets
    balance_sheet + liabilities
    pprint(vars(balance_sheet))
    pprint(list(balance_sheet))

    equities = Equities()
    equities + assets
    print str(assets)
    print str(liabilities)
    pprint(list(equities))
    equities + liabilities

    assets.save()
    liabilities.save()
