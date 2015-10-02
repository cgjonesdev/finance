class AccountBase(object):
    name = ''

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
