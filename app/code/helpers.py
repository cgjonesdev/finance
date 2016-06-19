from datetime import datetime as dt
from uuid import uuid4


def generate_uuids(num):
    uuids = []
    if isinstance(num, int):
        for i in range(num):
            uuids.append(str(uuid4()))
        return '\n'.join(uuids)
    else:
        raise TypeError('{} is not of type <int>'.format(num))


class Date(object):

    def __init__(self, date=''):
        self.date = date

    def __str__(self):
        if isinstance(self.date, (str, unicode)):
            if len(self.date.split('-')) > 1:
                date = self.date.split('-')
                date = int('20' + date[2]), int(date[0]), int(date[1])
                self.date = dt(*date)
                return self.date.ctime()
        return dt.now().ctime()


if __name__ == '__main__':
    print Date('1-1-16')
    print Date()
