import json
from pprint import pprint
from uuid import uuid4
import re


try:
    with open('./data/accounts.json') as _:
        data = json.loads(_.read())
except:
    with open('../../data/accounts.json') as _:
        data = json.loads(_.read())


class Accounts(object):

    def __init__(self):
        for k, v in data.items():
            self.__dict__[k] = v

    def __repr__(self):
        html = '<h3>Add Account</h3>'
        form = '<form class="account" method="POST" action="/accounts">'
        _input = '<input type="text" name="account_name" placeholder="Account Name"/>'
        _input += '<input type="submit" value="Add"/>'
        form += _input + '</form>'
        html += form
        html += '<h3>Accounts</h3>'
        for item, details in sorted(self):
            html += ('<div id="account"><a href="/accounts/{}"><b>{}</b></a></div>'
                     .format('_'.join(item.split(' ')).lower(), item))
        return html + '<br><br><br>'

    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())

    def __getitem__(self, item):
        for account in self:
            if account[0].lower() == ' '.join(item.split('_')):
                return account

    def add_account(self, account_name):
        data[account_name] = {'id': str(uuid4())}
        with open('./data/accounts.json', 'w') as _:
            _.write(json.dumps(data))


class Account(object):

    def __init__(self, name):
        accounts = Accounts()
        try:
            self.account = accounts[name]
        except:
            self.account = ''

    def __repr__(self):
        html = ''
        sk = lambda k: ' '.join(k.split('_')).title()
        ks = lambda k: '_'.join(k.split(' ')).lower()
        cv = lambda v: '$%.2f' % v if isinstance(v, (int, float)) else v
        wlink = lambda w: '<a href="{}" target="_blank">{}</a>'.format(w, w)
        plink = lambda p: '<a href="tel:{}">{}</a>'.format(''.join(re.findall('\d', p)), p)
        alink = lambda a: '<a href="{}" target="_blank">{}</a>'.format('https://www.google.com/search?q={}'.format('+'.join(a.split(' '))), a)
        elink = lambda e: '<a href="mailto:{}">{}</a>'.format(e, e)
        def test_for_link(k, l, v):
            if any([link for link in ('http', 'https') if link in str(v)]):
                v = wlink(v)
            elif '@' in str(v):
                v = elink(v)                
            elif k.lower() == 'phone' or l.lower() == 'phone':
                v = plink(v)
            elif k.lower() == 'address' or l.lower() == 'address':
                v = alink(v)
            return v
        if self.account:
            html = '<h3>Update {}</h3>'.format(self.account[0])
            form = '<center><form class="account" method="POST" action="/accounts/{}">'.format(ks(self.account[0]))
            _input = '<input type="text" name="aname" placeholder="Name"/>'
            _input += '<input type="text" name="balance" placeholder="Balance"/>'
            _input += '<input type="text" name="due_date" placeholder="Due Date"/>'
            _input += '<input type="text" name="account_no" placeholder="Account Number"/>'
            select = '<select name="status">'
            select += '<option value="default" selected disabled>Status</option>'
            select += '<option value="paid">Paid</option>'
            select += '<option value="late">Late</option>'
            select += '<option value="pending">Pending</option>'
            _input += select
            _input += '<br><textarea placeholder="Description"></textarea>'
            _input += '<input type="submit" value="   Add/Update   "/>'
            _input += '<button id="delete">Delete</button>'
            form += _input + '</form></center><br>'
            html += form            
            html += '<h3>{} details</h3>'.format(self.account[0])
            for k, v in self.account[1].items():
                if isinstance(v, dict):
                    html += '<div id="account-detail"><b>{}</b>:</div>'.format(sk(k))
                    for l, w in v.items():
                        if isinstance(w, dict):
                            html += '<div id="account-sub-detail"><b>{}</b>:</div>'.format(sk(l))
                            for m, x in w.items():
                                html += '<div id="account-sub-sub-detail"><b>{}</b>: {}</div>'.format(sk(m), test_for_link(l, m, cv(x)))
                        else:
                            html += '<div id="account-sub-detail"><b>{}</b>: {}</div>'.format(sk(l), test_for_link(k, l, cv(w)))
                else:
                    html += '<div id="account-detail"><b>{}</b>: {}</div>'.format(sk(k), test_for_link(k, k, cv(v)))
        return html + '<br><br><br>'



if __name__ == '__main__':
    print repr(Account('asset_acceptance'))
