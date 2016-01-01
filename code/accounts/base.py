from pprint import pprint, pformat
from datetime import datetime
from code.base import BaseMany, BaseSingleton
from code.mixins import Magic


class Accounts(BaseMany):

    def __init__(self):
        self.filename = '../../data/accounts.json'
        self.read()
        self.__dict__.update(self.data)
        for i, item in enumerate(self.items):
            self.items[i] = AccountSingleton(item)
            if 'contact' in item:
                self.items[i].contact = Contact(item['contact'])


class AccountSingleton(BaseSingleton):
    pass


class Contact(Magic):

    def __init__(self, contact_dict):
        self.__dict__.update(contact_dict)


if __name__ == '__main__':
    accounts = Accounts()
    output = repr(accounts)
    print output
    with open(
        datetime.now().strftime(
            '../logs/accounts/%a%d%b%Y.log'), 'w') as _:
        _.write(output)
    print '{} {}'.format(len(accounts), str(accounts))
