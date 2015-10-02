from base import AccountBase


class Account(AccountBase):
    balance = 0.0
    number = ''
    kind = ''


class Cashflow(Account):
    amount = 0.0
    date = None


class Receivable(Cashflow):
    pass


class Payable(Cashflow):
    pass


class Institution(Account):
    nickname = ''


class Checking(Institution):
    nickname = ''


class Savings(Institution):
    nickname = ''


class Credit(Institution):
    limit = 0.0
    rate = 0.0


class CreditCard(Credit):
    pass


class LineOfCredit(Credit):
    pass


class Investment(Institution):
    pass
