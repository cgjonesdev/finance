class Transaction(object):
    pass


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
