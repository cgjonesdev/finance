import sys
from mixins import Magic, IO


class Base(Magic, IO):

    def __init__(self):
        self.filename = '../data/{}.json'.format(str(self).lower())
        self.read()
        self.__dict__.update(self.data)


class BaseMany(Base):

    def __repr__(self):
        output = ''
        for item in self.items:
            output += repr(item) + '\n'
        return output

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


class BaseSingleton(Base):

    def __init__(self, data):
        self.__dict__.update(data)

    def __str__(self):
        return '{}: {} | {}'.format(self.__class__.__name__, self.name, self.id)

    def __add__(self, other):
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float)):
                if isinstance(other, (int, float)):
                    self.__dict__[k] += other
                elif isinstance(other, self.__class__):
                    self.__dict__[k] += other.__dict__[k]
        return self

    __radd__ = __add__

    def __sub__(self, other):
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float)):
                if isinstance(other, (int, float)):
                    self.__dict__[k] -= other
                elif isinstance(other, self.__class__):
                    self.__dict__[k] -= other.__dict__[k]
        return self

    __rsub__ = __sub__

    def __mul__(self, other):
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float)):
                if isinstance(other, (int, float)):
                    self.__dict__[k] *= other
                elif isinstance(other, self.__class__):
                    self.__dict__[k] *= other.__dict__[k]
        return self

    __rmul__ = __mul__

    def __div__(self, other):
        for k, v in self.__dict__.items():
            if isinstance(v, (int, float)):
                if isinstance(other, (int, float)):
                    self.__dict__[k] /= other
                elif isinstance(other, self.__class__):
                    self.__dict__[k] /= other.__dict__[k]
        return self

    __rdiv__ = __div__


if __name__ == '__main__':

    class TestBase(BaseSingleton):
        def __init__(self, balance=500.0, amount=100.0, limit=1000.0):
            self.balance = balance
            self.amount = amount
            self.limit = limit

    tb1, tb2 = [TestBase()] * 2
    print (tb1 + tb2).__dict__
    tb1, tb2 = [TestBase()] * 2
    print (tb1 - tb2).__dict__
    tb1, tb2 = [TestBase()] * 2
    print (tb1 * tb2).__dict__
    tb1, tb2 = [TestBase()] * 2
    print (tb1 / tb2).__dict__
    tb1 = TestBase()
    print (tb1 + 5).__dict__
    tb1 = TestBase()
    print (tb1 - 5).__dict__
    tb1 = TestBase()
    print (tb1 * 5).__dict__
    tb1 = TestBase()
    print (tb1 / 5).__dict__
    tb1 = TestBase()
    print (5 + tb1).__dict__
    tb1 = TestBase()
    print (5 - tb1).__dict__
    tb1 = TestBase()
    print (5 * tb1).__dict__
    tb1 = TestBase()
    print (5 / tb1).__dict__
