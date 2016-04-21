import json
from pprint import pprint, pformat
from datetime import datetime
from code.base import BaseMany, BaseSingleton
from mixins import *


class Accounts(BaseMany):

    def __init__(self):
        self.filename = '../../data/accounts.json'
        self.read(self.filename)
        self.text = json.loads(self.text)
        ObjectBuilder.dict_to_obj(self, self.text)

    def __iter__(self):
        return (item for item in self.__dict__.items())

    def __contains__(self, item):
        return item in self.__dict__

    def __len__(self):
        return sum(1 for x in self)

    def __repr__(self):
        return '\n'.join([attr for attr in dir(self) if not attr.startswith('_')])


class AccountSingleton(BaseSingleton):
    pass


if __name__ == '__main__':
    accounts = Accounts()
    print repr(accounts)
