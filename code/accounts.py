from datetime import datetime
from base import BaseMany, BaseSingleton


class Accounts(BaseMany):

    def __init__(self):
        BaseMany.__init__(self)
        for i, item in enumerate(self.items):
            self.items[i] = AccountSingleton(item)


class AccountSingleton(BaseSingleton):
    pass


if __name__ == '__main__':
    accounts = Accounts()
    output = repr(accounts)
    print output
    with open(
        datetime.now().strftime(
            'logs/accounts/%d%b%Y.log'), 'w') as _:
        _.write(output)
    print len(accounts)
    print dir(accounts)
