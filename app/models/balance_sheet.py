from base import *


class Cycle(object):
    _cycle_map = {
        'day(s)': 1.0,
        'week(s)': 7.0,
        'month(s)': 30.44,
        'year(s)': 365.28}
    _time_frame_keys = (
        'daily',
        'weekly',
        'bi-weekly',
        '15-days',
        '3-weeks',
        '4-weeks',
        'monthly',
        '5-weeks',
        '6-weeks',
        '2-months',
        'quarterly',
        '4-months',
        '6-months',
        '9-months',
        'yearly',
        '2-years',
        '3-years',
        '4-years',
        '5-years',
        '10-years')
    _time_frame_values = (
        _cycle_map['day(s)'],
        _cycle_map['week(s)'],
        _cycle_map['week(s)'] * 2,
        _cycle_map['month(s)'] / 2,
        _cycle_map['week(s)'] * 3,
        _cycle_map['week(s)'] * 4,
        _cycle_map['month(s)'],
        _cycle_map['week(s)'] * 5,
        _cycle_map['week(s)'] * 6,
        _cycle_map['month(s)'] * 2,
        _cycle_map['month(s)'] * 3,
        _cycle_map['month(s)'] * 4,
        _cycle_map['month(s)'] * 6,
        _cycle_map['month(s)'] * 9,
        _cycle_map['year(s)'],
        _cycle_map['year(s)'] * 2,
        _cycle_map['year(s)'] * 3,
        _cycle_map['year(s)'] * 4,
        _cycle_map['year(s)'] * 5,
        _cycle_map['year(s)'] * 10)
    _time_frame_map = dict(zip(_time_frame_keys, _time_frame_values))

    def __init__(self, obj, time_frame=None):
        self.obj = obj
        self._time_frame = time_frame
        self._divisor = self._time_frame_map[time_frame] if time_frame else 1.0

    def __str__(self):
        return '{}.{}'.format(str(self.obj), self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def _attribute_check(self):
        if not hasattr(self.obj, 'cycle_int') or not hasattr(self.obj, 'cycle_str'):
            raise AttributeError(
                '{} (name: {}, id: {}) doesn\'t have one or both of the attributes '
                '"cycle_int" or "cycle_str"'.format(
                    str(self.obj), self.obj.name, str(self.obj._id)))

    @property
    def days(self):
        # self._attribute_check()
        try:
            return self.obj.cycle_int * self._cycle_map[self.obj.cycle_str]
        except:
            return 1.0

    @property
    def time_frame(self):
        return self._time_frame

    @time_frame.setter
    def time_frame(self, value):
        if value not in self._time_frame_map:
            raise AttributeError(
                '{} is not an available time frame'.format(value))
        self._time_frame = value
        self._divisor = self._time_frame_map[self._time_frame]

    @property
    def amount(self):
        # self._attribute_check()
        try:
            self._amount = self.obj.amount / (
                (self.obj.cycle_int * self._cycle_map[self.obj.cycle_str]) /
                 self._divisor)
            return round(self._amount, 2)
        except:
            return 0.0


class BaseSingleton(Singleton):

    def __init__(self, time_frame='monthly', **kwargs):
        Singleton.__init__(self, **kwargs)
        self.cycle = Cycle(self, time_frame)


class Assets(Multi):
    _dataconnector = DataConnector('assets')
    form = Form('BALANCE_SHEET')

    def __init__(self, user_id):
        self.user_id = user_id
        self.items = [Asset(**item) for item in
                      self._dataconnector.collection.find(
                          {'user_id': self.user_id})]


class Asset(BaseSingleton):
    pass


class Liabilities(Multi):
    _dataconnector = DataConnector('liabilities')
    form = Form('BALANCE_SHEET')

    def __init__(self, user_id):
        self.user_id = user_id
        self.items = [Liability(**item) for item in
                      self._dataconnector.collection.find(
                          {'user_id': self.user_id})]


class Liability(BaseSingleton):

    def __init__(self, **kwargs):
        BaseSingleton.__init__(self, **kwargs)
        kwargs['amount'] = -kwargs['amount']
        self.__dict__.update(kwargs)


class Equities(Multi):
    _dataconnector = DataConnector('equities')
    form = Form('BALANCE_SHEET')

    def __init__(self, user_id, assets=None, liabilities=None):
        self.user_id = user_id
        self.items = [Equity(**item) for item in
                      self._dataconnector.collection.find(
                          {'user_id': self.user_id})]
        if assets:
            self.items.append(
                Equity(
                    **{'user_id': assets.user_id,
                       'name': 'Assets',
                       'amount': assets.cycle_total}))
        if liabilities:
            self.items.append(
                Equity(
                    **{'user_id': liabilities.user_id,
                       'name': 'Liabilities',
                       'amount': liabilities.cycle_total}))


class Equity(BaseSingleton):
    _id = None


if __name__ == '__main__':
    assets = Assets('57b4eb27acf608ac5d56c2ba')
    print 'Assets cycle total: {}'.format(assets.cycle_total)
    for asset in assets:
        print '{}; Time frame: {}, Number of days: {}, Original amount: {}, New amount: {}'.format(str(asset), asset.cycle.time_frame, asset.cycle.days, asset.amount, asset.cycle.amount)
    liabilities = Liabilities('57b4eb27acf608ac5d56c2ba')
    print '\nLiabilities cycle total: {}'.format(liabilities.cycle_total)
    for liability in liabilities:
        print '{}; Time frame: {}, Number of days: {}, Original amount: {}, New amount: {}'.format(str(liability), liability.cycle.time_frame, liability.cycle.days, liability.amount, liability.cycle.amount)
    # # assets.clear()
    # job = Asset(**{'user_id': assets.user_id, 'name': 'job', 'amount': 5000.0})
    # assets + job
    # print 'assets.total: {}'.format(assets.total)

    # liabilities = Liabilities('57a3c6a9acf6088060156578')
    # # liabilities.clear()
    # rent = Liability(**{'user_id': assets.user_id, 'name': 'rent', 'amount': 1000.0})
    # liabilities + rent
    # print 'liabilities.total: {}'.format(liabilities.total)

    # equities = Equities()
    # # equities.clear()
    # equities += assets
    # equities += liabilities

    # print 'equities.total: {}'.format(equities.total)
