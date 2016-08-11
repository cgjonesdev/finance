from base import *


class Users(Multi):
    _dataconnector = DataConnector('users')

    def __init__(self):
        self.items = [User(**item) for item in list(self._dataconnector)]

    def get_by_name(self, name):
        users = [item for item in self if item.name == name]
        return users[0] if len(users) == 1 else users

    def get_by_digest(self, user_digest):
        user = [item for item in self.items if item.user_digest == user_digest]
        return user[0] if user else None


class User(Singleton):

    def validate_login(self, user_digest):
        return self.user_digest == user_digest


if __name__ == '__main__':
    users = Users()
    print vars(users['57a3c6a9acf6088060156578'])
    print vars(users['57a5107b8922811039056a7e'])