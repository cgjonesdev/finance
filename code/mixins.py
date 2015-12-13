import json
from lib.mixins import Magic


class IO(object):

    def read(self):
        with open(self.filename) as _:
            self.data = json.loads(_.read())

    def write(self):
        with open(self.filename, 'w') as _:
            _.write(json.dumps(self.data))


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
