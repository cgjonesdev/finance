from base import *


class PayableAccounts(Accounts):

    def __iter__(self):
        return (item for item in self.items if hasattr(item, 'type') and item.type == 'payable')


class PayableAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    payableaccounts = PayableAccounts()
    output = repr(payableaccounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/payable/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(payableaccounts), str(payableaccounts))
