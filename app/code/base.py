from pprint import pprint, pformat
from data import DataConnector
from finance.app.logger import logger


class Base(object):

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return pformat(
            [vars(item) for item in self.items])\
            if hasattr(self, 'items') else pformat(vars(self))

    def _strip_keys(self, data):
        # Strip identifier key and extranoues text from data keys coming from
        # form data

        data = vars(data) if not isinstance(data, dict) else data

        for k, v in data.items():
            if 'form' in k:
                del data[k]
                try:
                    data[k.split('_')[-1]] = abs(float(v))
                except:
                    data[k.split('_')[-1]] = v
        return type(str(self), (Singleton,), data)


class Multi(Base):

    def __init__(self, user_id=None):
        if user_id:
            self.user_id = user_id

    def __iter__(self):
        return (item for item in self.items)

    def __contains__(self, _id):
        return any(_id == item._id for item in self)

    def __getitem__(self, _id):
        item = [i for i in self.items if i._id == _id]
        return item[0] if item else None

    def __add__(self, data):
        data = vars(data) if not isinstance(data, dict) else data

        obj = self._strip_keys(data)
        self.items.append(obj)
        self._dataconnector + {k: v for k, v in vars(obj).items()
                               if k not in ('_id', '__doc__', '__module__')}
        return self

    def __sub__(self, _id):
        data = self._dataconnector[_id]
        obj = self._strip_keys(data)
        if _id in self:
            self._dataconnector - _id
        return self

    def __iadd__(self, update_info):
        _id, data = update_info
        obj = self._strip_keys(data)
        self._dataconnector += (_id,
                                {k: v for k, v in vars(obj).items() if k not
                                 in ('_id', '__doc__', '__module__')})
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
        for k, v in kwargs.items():
            if str(self) == 'Liability' and k == 'amount':
                self.__dict__[k] = -float(v)
            elif k == 'amount':
                self.__dict__[k] = float(v)
            else:
                self.__dict__[k] = v

    def __iadd__(self, data):
        self.__dict__.update(data)
        self._dataconnector += data
