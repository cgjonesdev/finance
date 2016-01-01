from base import *


class CreditCardAccounts(Accounts):

    def __iter__(self):
        return (item for item in self.items if hasattr(item, 'type') and item.type == 'creditcard')


class CreditCardAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    creditcardaccounts = CreditCardAccounts()
    output = repr(creditcardaccounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/creditcard/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(creditcardaccounts), str(creditcardaccounts))
