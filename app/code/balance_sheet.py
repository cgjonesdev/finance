from data import DataConnector as DC


class Base(object):

    def __str__(self):
        return self.__class.__.__name__


class BalanceSheet(object):

    def __init__(self):
        self.assets = []
        self.liabilities = []

    def __iter__(self):
        return (x for x in self.assets + self.liabilities)

    def __add__(self, object):
        if isinstance(object, Assets):
            self.assets.extend(object)
        else:
            raise TypeError(
                'object must be Assets type, you supplied: {}'.format(
                    type(object)))

    def __sub__(self, object):
        if isinstance(object, Liabilities):
            self.assets.extend(object)
        else:
            raise TypeError(
                'object must be Liabilities type, you supplied: {}'.format(
                    type(object)))


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

    @property
    def total(self):
        return sum(x.amount for x in self)


class Singleton(Base):
    
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount



class Assets(Multi):
    pass 


class Asset(Singleton):
    pass


class Liabilities(Multi):
    pass


class Liability(Singleton):
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
    balance_sheet - liabilities
    pprint(vars(balance_sheet))
    pprint(list(balance_sheet))
