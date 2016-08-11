from base import *


class Assets(Multi):
    _dataconnector = DataConnector('assets')

    def __init__(self, user_id):
        self.user_id = user_id
        self.items = [Asset(**item) for item in
                      self._dataconnector.collection.find(
                          {'user_id': self.user_id})]


class Asset(Singleton):
    pass


class Liabilities(Multi):
    _dataconnector = DataConnector('liabilities')

    def __init__(self, user_id):
        self.user_id = user_id
        self.items = [Liability(**item) for item in
                      self._dataconnector.collection.find(
                          {'user_id': self.user_id})]


class Liability(Singleton):
    pass


class Equities(Multi):
    _dataconnector = DataConnector('equities')

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
                       'amount': assets.total}))
        if liabilities:
            self.items.append(
                Equity(
                    **{'user_id': liabilities.user_id,
                       'name': 'Liabilities',
                       'amount': -liabilities.total}))


class Equity(Singleton):
    _id = None


if __name__ == '__main__':
    assets = Assets('57a3c6a9acf6088060156578')
    # assets.clear()
    job = Asset(**{'user_id': assets.user_id, 'name': 'job', 'amount': 5000.0})
    assets + job
    print 'assets.total: {}'.format(assets.total)

    liabilities = Liabilities()
    # liabilities.clear()
    rent = Liability(**{'name': 'rent', 'amount': 1000.0})
    liabilities + rent
    print 'liabilities.total: {}'.format(liabilities.total)

    equities = Equities()
    # equities.clear()
    equities += assets
    equities += liabilities

    print 'equities.total: {}'.format(equities.total)
