from base import *


class BankAccounts(Accounts):

    def __iter__(self):
        return (item for item in self.items if hasattr(item, 'type') and item.type == 'bank')


class BankAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    bankaccounts = BankAccounts()
    output = repr(bankaccounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/bank/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(bankaccounts), str(bankaccounts))
