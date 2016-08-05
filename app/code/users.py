from data import DataConnector as DC


class Users(object):
    _dataconnector = DC('users')

    def __init__(self):
        self.items = (User(**user) for user in list(self._dataconnector))

    def __iter__(self):
        return (item for item in self.items)

    def __contains__(self, _id):
        return any(_id == item._id for item in self)

    def __add__(self, data):
        if isinstance(data, dict):
            obj = type(str(self), (User,), data)
            self.items.append(obj)
        elif isinstance(data, User):
            obj = data
            self.items.append(obj)
        self._dataconnector + {k: v for k, v in vars(obj).items()
                               if k not in ('_id', '__doc__', '__module__')}
        return self

    def __sub__(self, _id):
        data = self._dataconnector[_id]
        obj = type(str(self), (User,), data)
        if _id in self:
            self._dataconnector - _id
        return self

    def __iadd__(self, update_info):
        _id, data = update_info
        obj = type(str(self), (User,), data)
        self._dataconnector += (_id,
                                {k: v for k, v in vars(obj).items() if k not
                                 in ('_id', '__doc__', '__module__')})
        return self

    def clear(self):
        self._dataconnector.clear()


class User(object):

    def __init__(self, _id, name, user_digest):
        self._id = _id
        self.name = name
        self.user_digest = user_digest

    def validate(self, user_digest):
        return self.user_digest == user_digest


if __name__ == '__main__':
    users = Users()
    _users = list(users)
    print _users[0].validate('f8c02215856f2203eefaf093c4216bfb')
    print _users[0].name
