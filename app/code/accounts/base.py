import json
from pprint import pprint
from uuid import uuid4


with open('./data/accounts.json') as _:
    data = json.loads(_.read())


class Accounts(object):

    def __init__(self):
        for k, v in data.items():
            self.__dict__[k] = v

    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())

    def __getitem__(self, item):
        for account in self:
            if account[0].lower() == ' '.join(item.split('_')):
                return account

    def add_account(self, account_name):
        data[account_name] = {'id': str(uuid4())}
        with open('./data/accounts.json', 'w') as _:
            _.write(json.dumps(data))


class Account(object):

    def __init__(self, name):
        accounts = Accounts()
        self.account = accounts[name]



if __name__ == '__main__':
    Accounts()
