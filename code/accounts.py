from base import AccountBase


class Account(AccountBase):
    balance = 0.0
    number = ''


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


class CreditCard(Credit):
    pass


class LineOfCredit(Credit):
    pass


class Investment(Account):
    pass

