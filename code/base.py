import sys
from mixins import *


class Base(Magic, IO):
    update_attrs = []

    def __init__(self):
        self.filename = '../../data/{}.json'.format(str(self).lower()) if \
        str(self) == 'Accounts' else '../data/{}.json'.format(str(self)\
                .lower())
        self.read()
        self.__dict__.update(self.data)


class BaseMany(Base):

    def __repr__(self):
        return '\n'.join(repr(item) for item in self)

    def __iter__(self):
        return (item for item in self.items)

    def __getitem__(self, item):
        if item in self:
            return item

    def __add__(self, item):
        if item not in self.items:
            self.items.append(item)
        else:
            raise AttributeError('{} is aready in self'.format(item))

    def __iadd__(self, update_info):
        if isinstance(update_info, tuple):
            _id, data = update_info
            self[item].__dict__.update(data)
        else:
            raise TypeError('{} is not a tuple'.format(update_info))

    def __sub__(self, item):
        if item in self:
            self.items.remove(item)
        else:
            raise AttributeError('{} not in self'.format(item))


class BaseSingleton(Base, Add, Subtract, Multiply, Divide):
    update_attrs = ['balance', 'amount', 'limit']

    def __init__(self, data):
        self.__dict__.update(data)

    def __str__(self):
        return '{}: {} | {}'.format(self.__class__.__name__, self.name, self.id)


if __name__ == '__main__':
    data = {
        'balance': 500.0,
        'amount': 100.0,
        'limit': 1000.0
    }
    tb1, tb2 = [BaseSingleton(data)] * 2
    print (tb1 + tb2).__dict__
    tb1, tb2 = [BaseSingleton(data)] * 2
    print (tb1 - tb2).__dict__
    tb1, tb2 = [BaseSingleton(data)] * 2
    print (tb1 * tb2).__dict__
    tb1, tb2 = [BaseSingleton(data)] * 2
    print (tb1 / tb2).__dict__
    tb1 = BaseSingleton(data)
    print (tb1 + 5).__dict__
    tb1 = BaseSingleton(data)
    print (tb1 - 5).__dict__
    tb1 = BaseSingleton(data)
    print (tb1 * 5).__dict__
    tb1 = BaseSingleton(data)
    print (tb1 / 5).__dict__
    tb1 = BaseSingleton(data)
    print (5 + tb1).__dict__
    tb1 = BaseSingleton(data)
    print (5 - tb1).__dict__
    tb1 = BaseSingleton(data)
    print (5 * tb1).__dict__
    tb1 = BaseSingleton(data)
    print (5 / tb1).__dict__
