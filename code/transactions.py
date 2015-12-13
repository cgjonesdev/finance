from datetime import datetime
from base import BaseMany, BaseSingleton


class Transactions(BaseMany):

    def __init__(self):
        BaseMany.__init__(self)
        for i, item in enumerate(self.items):
            self.items[i] = TransactionSingleton(item)


class TransactionSingleton(BaseSingleton):
    pass


if __name__ == '__main__':
    transactions = Transactions()
    output = repr(transactions)
    print output
    with open(
        datetime.now().strftime(
            'logs/transactions/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print len(transactions)

