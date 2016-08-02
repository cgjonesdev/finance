from pprint import pprint, pformat

from data import DataConnector as DC


class Base(object):

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return pformat(
            [vars(item) for item in self.items])\
            if hasattr(self, 'items') else pformat(vars(self))


class Multi(Base):

    def __iter__(self):
        return (item for item in self.items)

    def __add__(self, other):
        self.items.append(other)
        self._dataconnector + {k: v for k, v in vars(other).items() if k != '_id'}
        return self

    def __sub__(self, other):
        if other in self:
            self.items.remove(other)
            self._dataconnector - vars(other)
        return self

    def __iadd__(self, others):
        self.items.extend(others.items)
        for other in others:
            self._dataconnector + {k: v for k, v in vars(other).items() if
                                   k != '_id'}
        return self

    def __isub__(self, others):
        for other in others:
            if other in self:
                self.items.remove(other)
                self._dataconnector - vars(other)

    @property
    def total(self):
        if isinstance(self, Liabilities):
            return sum(-item.amount for item in self)
        else:
            return sum(item.amount for item in self)

    def clear(self):
        self._dataconnector.clear()


class Singleton(Base):

    def __init__(self, _id=None, name='', amount=0.0):
        self._id = str(_id)
        self.name = name
        self.amount = amount


class Assets(Multi):
    _dataconnector = DC('assets')

    def __init__(self):
        self.items = [Asset(**item) for item in list(self._dataconnector)]


class Asset(Singleton):
    pass


class Liabilities(Multi):
    _dataconnector = DC('liabilities')

    def __init__(self):
        self.items = [Liability(**item) for item in list(self._dataconnector)]


class Liability(Singleton):

    def __init__(self, _id=None, name='', amount=0.0):
        self.name = name
        self.amount = -amount


class Equities(Multi):
    _dataconnector = DC('equities')

    def __init__(self):
        self.items = [Equity(**item) for item in list(self._dataconnector)]


class Equity(Singleton):
    pass


if __name__ == '__main__':
    assets = Assets()
    # assets.clear()
    job = Asset(**{'name': 'job', 'amount': 5000.0})
    assets + job
    print 'assets.total: {}'.format(assets.total)

    liabilities = Liabilities()
    # liabilities.clear()
    rent = Liability(**{'name': 'rent', 'amount': 1000.0})
    liabilities + rent
    print 'liabilities.total: {}'.format(liabilities.total)

    equities = Equities()
    # equities.clear()
    equities += assets
    equities += liabilities

    print 'equities.total: {}'.format(equities.total)
