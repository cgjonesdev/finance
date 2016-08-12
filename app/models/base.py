import sys
from pprint import pprint, pformat
from data import DataConnector
from forms import Form
from finance.app.logger import logger


class Base(object):

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return pformat(
            [vars(item) for item in self.items])\
            if hasattr(self, 'items') else pformat(vars(self))


class Multi(Base):

    def __init__(self, user_id=None):
        self.user_id = user_id

    def __iter__(self):
        return (item for item in self.items)

    def __contains__(self, _id):
        return any(_id == str(item._id) for item in self)

    def __getitem__(self, _id):
        for item in self:
            if hasattr(item, '_id') and str(item._id) == _id:
                return item

    def __add__(self, data):
        data = vars(data) if not isinstance(data, dict) else data
        obj = self.form.to_obj(data, self.__class__)
        self.items.append(obj)
        self._dataconnector + {k: v for k, v in vars(obj).items()
                               if k not in ('_id', '__doc__', '__module__')}
        return self

    def __sub__(self, _id):
        if _id in self:
            data = self._dataconnector[_id]
            obj = self.form.to_obj(data, self.__class__)
            self._dataconnector - _id
        else:
            raise Exception('DELETE: _id {} not found in the database'.format(_id))
        return self

    def __iadd__(self, update_info):
        _id, data = update_info
        if _id in self:
            obj = self.form.to_obj(data, self.__class__)
            self._dataconnector += (_id,
                                    {k: v for k, v in vars(obj).items() if k not
                                     in ('_id', '__doc__', '__module__')})
        else:
            raise Exception('PUT: _id {} not found in the database'.format(_id))
        return self

    @property
    def total(self):
        if str(self) == 'Liabilities':
            return round(sum(-item.amount for item in self), 2)
        else:
            return round(sum(item.amount for item in self), 2)

    def clear(self):
        self._dataconnector.clear()


class Singleton(Base):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __iadd__(self, data):
        self.__dict__.update(data)
        self._dataconnector += data
