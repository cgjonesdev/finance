from base import AccountBase


class Transaction(AccountBase):
    amount = 0.0
    date = None
    note = ''
    conf = ''
    kind = ''


class Credit(Transaction):
    pass


class Debit(Transaction):
    pass


class Deposit(Transaction):
    pass


class Payment(Transaction):
    pass


class Transfer(Transaction):
    pass


class InsufficientFunds(Transaction):
    pass
