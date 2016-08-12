from base import *
from finance.app.crypt import validate_digest


class Users(Multi):
    _dataconnector = DataConnector('users')
    form = Form('USER')

    def __init__(self):
        self.items = [User(**item) for item in list(self._dataconnector)]

    def get_by_name(self, name):
        for user in self:
            if user.name == name:
                return user

    def get_by_digest(self, user_digest):
        for user in self:
            user.validate(user_digest)
            if user:
                return user


class User(Singleton):
    _validated = False

    def validate(self, user_digest):
        self._validated = validate_digest(self.user_digest, user_digest)

    def __nonzero__(self):
        return self._validated


if __name__ == '__main__':
    users = Users()
    test = User(**{{'username': u'test', 'phone': u'555-1212', 'email': u'test@gmail.com', 'user_digest': '1b82612f41b68dc8b2ecde8e0b4ee0ec'}       })
    print list(users)
    print vars(users['57a3c6a9acf6088060156578'])
    print vars(users['57a5107b8922811039056a7e'])
    print vars(users['57acd862acf6081516112db2'])