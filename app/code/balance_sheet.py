import sys
from pprint import pprint, pformat

from data import DataConnector as DC


class Base(object):

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return pformat(
            [vars(item) for item in self.items])\
            if hasattr(self, 'items') else pformat(vars(self))

    def _strip_keys(self, data):
        # Strip identifier key and extranoues text from data keys coming from
        # form data

        for k, v in data.items():
            if 'form' in k:
                del data[k]
            else:
                del data[k]
                data[k.split('_')[-1]] = v
            try:
                data[k.split('_')[-1]] = abs(float(v))
            except:
                pass
        return type(str(self), (Singleton,), data)


class Multi(Base):

    def __iter__(self):
        return (item for item in self.items)

    def __contains__(self, _id):
        return any(_id == item._id for item in self)

    def __add__(self, data):
        if isinstance(data, dict):
            obj = self._strip_keys(data)
        self.items.append(obj)
        self._dataconnector + {k: v for k, v in vars(obj).items()
                               if k not in ('_id', '__doc__', '__module__')}
        return self

    def __sub__(self, _id):
        data = self._dataconnector[_id]
        obj = self._strip_keys(data)
        if _id in self:
            self._dataconnector - _id
        return self

    def __iadd__(self, update_info):
        _id, data = update_info
        obj = self._strip_keys(data)
        self.__dict__.update(vars(obj))
        self._dataconnector += (_id,
                                {k: v for k, v in vars(obj).items() if k not
                                 in ('_id', '__doc__', '__module__')})
        return self

    @property
    def total(self):
        if isinstance(self, Liabilities):
            return round(sum(-item.amount for item in self), 2)
        else:
            return round(sum(item.amount for item in self), 2)

    def clear(self):
        self._dataconnector.clear()


class Singleton(Base):

    def __init__(self, _id=None, name='', amount=0.0):
        self._id = str(_id)
        self.name = name if name else 'Unknown'
        self.amount = amount if amount else 0.0

    def __iadd__(self, data):
        self.__dict__.update(data)
        self._dataconnector += data


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
        self._id = str(_id)
        self.name = name if name else 'Unknown'
        self.amount = -amount if amount else 0.0


class Equities(Multi):
    _dataconnector = DC('equities')

    def __init__(self, assets=None, liabilities=None):
        self.items = [Equity(**item) for item in list(self._dataconnector)]
        if assets:
            self.items.append(
                Equity(**{'name': 'Assets', 'amount': assets.total}))
        if liabilities:
            self.items.append(
                Equity(**{'name': 'Liabilities', 'amount': -liabilities.total}))


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
