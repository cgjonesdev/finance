'''
A python connector to the plaid RESTful api for downloading bank transactions
'''
import requests
import json


INSTITUTIONS = {
    'amex': 'American Express',
    'bofa': 'Bank of America',
    'capone360': 'Capital One 360',
    'schwab': 'Charles Schwab',
    'chase': 'Chase',
    'citi': 'Citi',
    'fidelity': 'Fidelity',
    'pnc': 'PNC',
    'svb': 'Silicon Valley Bank',
    'us': 'US Bank',
    'usaa': 'USAA',
    'wells': 'Wells Fargo'
}


class Base(object):
    plaid_base_url = 'https://tartan.plaid.com'
    data = {
        'client_id': '555a566f3b5cadf40371c2e2',
        'secret': 'd575f23781eb06347ae14b4cc48b1a'
        # 'public_key': '2f2beddcdb65b88f01d717bbc13b68'
    }

    def __init__(self, **kwargs):
        kwargs['type'] = str(self)
        self.data.update(kwargs)

    def __str__(self):
        return self.__class__.__name__.lower()

    def connect(self):
        '''
        allows developers to receive user-authorized transaction and account
        data
        '''
        response = json.loads(
            requests.post(
                '{}/connect'.format(self.plaid_base_url), self.data
            ).text
        )
        self.data.update(
            {'access_token': response.get('access_token'),
             'accounts': response.get('accounts'),
             'transactions': response.get('transactions')}
        )

    def auth(self):
        '''
        allows you to collect a user's bank account and routing number,
        along with basic account data and balances
        '''
        return requests.post(
            '{}/auth'.format(self.plaid_base_url), self.data
        ).text

    def balance(self):
        '''
        returns the real-time balance of a user's accounts
        '''
        response = json.loads(
            requests.post(
                '{}/connect'.format(self.plaid_base_url), self.data
            ).text
        )
        self.data.update({'access_token': response.get('access_token')})
        response = json.loads(
            requests.post(
                '{}/balance'.format(self.plaid_base_url), self.data
            ).text
        )
        for account in response.get('accounts'):
            print response.get('meta').get('name')

    def upgrade(self):
        pass

    def institutions(self, _id=None):
        if not _id:
            return requests.get(
                '{}/institutions'.format(self.plaid_base_url)
            ).text
        else:
            return requests.get(
                '{}/institutions/{}'.format(self.plaid_base_url, _id)
            ).text

    def categories(self):
        pass


class Chase(Base):
    pass


class BofA(Base):

    def connect(self, mfa):
        '''
        allows developers to receive user-authorized transaction and account
        data
        '''
        # self.data.update({'mfa': mfa, 'options': json.dumps({'login_only': True})})
        # raise Exception(self.data)
        response = json.loads(
            requests.post(
                '{}/connect'.format(self.plaid_base_url), self.data
            ).text
        )
        raise Exception(response)
        self.data.update(
            {'access_token': response.get('access_token'),
             'accounts': response.get('accounts'),
             'transactions': response.get('transactions')}
        )
        pprint(self.data)

    def auth(self, mfa=None):
        self.data.update({'mfa': mfa})
        return requests.post(
            '{}/auth/step'.format(self.plaid_base_url), self.data
        ).text
