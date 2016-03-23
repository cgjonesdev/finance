import os
from datetime import datetime as dt
import json


class IO(object):

    def __str__(self):
        return self.__class__.__name__

    def read(self, filename):
        with open(filename) as _:
            self.text = _.read()
        return self.text

    def write(self, filename, daylog=False, no_date=False):
        directory = os.path.split(filename)[0]
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        timefunc = lambda x: '_' + x.replace(' ', '_').replace(':', '-') + '.'
        if daylog:
            daylog = dt.now().strftime('%a %b %d %Y')
        if not no_date:
            filename = timefunc(daylog or dt.now().strftime('%c')).join(filename.split('.'))
        with open(filename, 'w') as _:
            _.write(repr(self))


class Add(object):

    def __add__(self, other):
        for k, v in self.__dict__.items():
            if k in self.update_attrs:
                if isinstance(v, (int, float)):
                    if isinstance(other, (int, float)):
                        self.__dict__[k] += other
                    elif isinstance(other, self.__class__):
                        self.__dict__[k] += other.__dict__[k]
            else:
                raise Exception('{} not in {}'.format(k, self.update_attrs))
        return self

    __radd__ = __add__


class Subtract(object):

    def __sub__(self, other):
        for k, v in self.__dict__.items():
            if k in self.update_attrs:
                if isinstance(v, (int, float)):
                    if isinstance(other, (int, float)):
                        self.__dict__[k] -= other
                    elif isinstance(other, self.__class__):
                        self.__dict__[k] -= other.__dict__[k]
            else:
                raise Exception('{} not in {}'.format(k, self.update_attrs))
        return self

    __rsub__ = __sub__


class Multiply(object):

    def __mul__(self, other):
        for k, v in self.__dict__.items():
            if k in self.update_attrs:
                if isinstance(v, (int, float)):
                    if isinstance(other, (int, float)):
                        self.__dict__[k] *= other
                    elif isinstance(other, self.__class__):
                        self.__dict__[k] *= other.__dict__[k]
            else:
                raise Exception('{} not in {}'.format(k, self.update_attrs))
        return self

    __rmul__ = __mul__


class Divide(object):

    def __div__(self, other):
        for k, v in self.__dict__.items():
            if k in self.update_attrs:
                if isinstance(v, (int, float)):
                    if isinstance(other, (int, float)):
                        self.__dict__[k] /= other
                    elif isinstance(other, self.__class__):
                        self.__dict__[k] /= other.__dict__[k]
            else:
                raise Exception('{} not in {}'.format(k, self.update_attrs))
        return self

    __rdiv__ = __div__


class Affirm(object):

    def __pos__(self):
        return +self.balance


class Negate(object):

    def __neg__(self):
        return -self.balance
