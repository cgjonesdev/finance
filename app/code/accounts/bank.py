from base import *


class BankAccounts(Accounts):

    def __iter__(self):
        return (getattr(self, attr) for attr in dir(self) if
                hasattr(self, 'type') and self.type == 'bank')


class BankAccountSingleton(AccountSingleton):
    pass


if __name__ == '__main__':
    bankaccounts = BankAccounts()
    print repr(bankaccounts)
