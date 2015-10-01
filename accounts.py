class Account(object):
    name = ''
    balance = 0.0

    def __str__(self):
        return self.__class__.__name__.lower()

    def __add__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] += other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] += other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] += other.limit
        return self

    def __radd__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] += other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] += other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] += other.limit
        return self

    def __sub__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] -= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] -= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] -= other.limit
        return self

    def __rsub__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] -= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] -= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] -= other.limit
        return self

    def __mul__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] *= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] *= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] *= other.limit
        return self

    def __rmul__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] *= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] *= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] *= other.limit
        return self

    def __div__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] /= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] /= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] /= other.limit
        return self

    def __rdiv__(self, other):
        if 'balance' in self.__dict__:
            self.__dict__['balance'] /= other.balance
        if 'amount' in self.__dict__:
            self.__dict__['amount'] /= other.amount
        if 'limit' in self.__dict__:
            self.__dict__['limit'] /= other.limit
        return self


class Receivable(Account):
    amount = 0.0


class Payable(Account):
    amount = 0.0


class Checking(Account):
    nickname = ''


class Savings(Account):
    nickname = ''


class Credit(Account):
    limit = 0.0
    interest_rate = 0.0


class Investment(Account):
    pass


r = Receivable()
r.amount = 500

p = Payable()
p.amount = 100

print (r / p).amount

c1 = Credit()
c2 = Credit()

c1.limit = 5000
c1.balance = 100
c2.limit = 1000
c2.balance = 500

print (c1 - c2).__dict__

print c1 - p
