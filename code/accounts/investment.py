from base import *


class InvestmentAccounts(Accounts):

    def __iter__(self):
        return (item for item in self.items if hasattr(item, 'type') and item.type == 'investment')


class InvestmentAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    investmentaccounts = InvestmentAccounts()
    output = repr(investmentaccounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/investment/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(investmentaccounts), str(investmentaccounts))
