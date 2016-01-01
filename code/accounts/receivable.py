from base import *


class ReceivableAccounts(Accounts):

    def __iter__(self):
        return (item for item in self.items if hasattr(item, 'type') and item.type == 'receivable')


class ReceivableAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    receivableaccounts = ReceivableAccounts()
    output = repr(receivableaccounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/receivable/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(receivableaccounts), str(receivableaccounts))
