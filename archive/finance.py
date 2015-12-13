'''
Code to parse text files and convert line items to html tables
'''

import sys
import os
from pprint import pprint, pformat


for f in os.listdir('data'):
    f = 'data/{}'.format(f)
    if os.path.splitext(f)[-1] == '.txt':
        try:
            with open(f) as _:
                setattr(
                    sys.modules[__name__],
                    'parsed_{}'.format(f.split('.txt')[0].split('/')[1]),
                    [_[:-1] for _ in _.readlines()]
                )
        except:
            setattr(
                sys.modules[__name__],
                'parsed_{}'.format(f.split('.txt')[0].split('/')[1]),
                []
            )

class Base(object):

    def __init__(self, data):
        if 'balance' in data:
            try:
                data['balance'] = float(data['balance'])
            except:
                data['balance'] = 0.0
        if 'limit' in data:
            try:
                data['limit'] = float(data['limit'])
            except:
                data['limit'] = 0.0
        if 'amount' in data:
            try:
                data['amount'] = float(data['amount'])
            except:
                data['amount'] = 0.0
        self.__dict__.update(data)

    def __str__(self):
        return self.__class__.__name__

    def __add__(self, other):
        if str(self) == 'Account':
            self.__dict__.update(
                {'balance': float(self.balance) + float(other.amount)}
            )
        else:
            self.__dict__.update(
                {'amount': float(self.amount) + float(other.amount)}
            )
        return Base(self.__dict__)

    def __radd__(self, other):
        if str(self) == 'Account':
            self.__dict__.update(
                {'balance': float(self.balance) + float(other.amount)}
            )
        else:
            self.__dict__.update(
                {'amount': float(self.amount) + float(other.amount)}
            )
        return Base(self.__dict__)

    def __sub__(self, other):
        if str(self) == 'Account':
            self.__dict__.update(
                {'balance': float(self.balance) - float(other.amount)}
            )
        else:
            self.__dict__.update(
                {'amount': float(self.amount) - float(other.amount)}
            )
        return Base(self.__dict__)

    def __rsub__(self, other):
        if str(self) == 'Account':
            self.__dict__.update(
                {'balance': float(self.balance) - float(other.amount)}
            )
        else:
            self.__dict__.update(
                {'amount': float(self.amount) - float(other.amount)}
            )
        return Base(self.__dict__)


class Account(Base):
    pass


class Income(Base):
    pass


class Expense(Base):
    pass


class Transaction(Base):
    pass


accounts = []
for i, p in enumerate(parsed_accounts):
    data = dict(
        zip(('name', 'balance', 'limit', 'type', 'nickname'),
            p.split('|'))
    )
    accounts.append(Account(data))

incomes = []
for i, p in enumerate(parsed_incomes):
    data = dict(
        zip(('name', 'amount', 'date', 'note', 'confirmation', 'account'),
            p.split('|'))
    )
    incomes.append(Income(data))

expenses = []
for i, p in enumerate(parsed_expenses):
    data = dict(
        zip(('name', 'amount', 'date', 'note', 'confirmation', 'account'),
            p.split('|'))
    )
    expenses.append(Expense(data))


with open('templates/template.html') as f:
    finances = f.read()

def create_table(objectlist):
    with open('templates/table.html') as t:
        table = t.read()
    with open('templates/table1.html') as t:
        table1 = t.read()
    arows = []
    rows = []
    for i in objectlist:
        if str(i) == 'Account':
            row = ('<tr><td>{}</td><td>${}</td><td>${}</td><td>{}</td><td>{}'
                '</td></tr>'
                .format(
                    i.__dict__.get('name').title(),
                    i.__dict__.get('balance'),
                    i.__dict__.get('limit') or ' ---',
                    i.__dict__.get('type') or '---',
                    i.__dict__.get('nickname') or '---'
                )
            )
            arows.append(row)
        else:
            row = ('<tr><td>{}</td><td>${}</td><td>{}</td><td>{}</td><td>{}'
                '</td></tr>'
                .format(
                    i.__dict__.get('name').title(),
                    i.__dict__.get('amount'),
                    i.__dict__.get('date'),
                    i.__dict__.get('note') or '---',
                    i.__dict__.get('confirmation') or '---'
                )
            )
            rows.append(row)
    if objectlist and str(objectlist[0]) == 'Account':
        style = 'style="color:darkblue"'
    elif objectlist and str(objectlist[0]) == 'Income':
        style = 'style="color:darkgreen"'
    elif objectlist and str(objectlist[0]) == 'Expense':
        style = 'style="color:darkred"'
    if str(i) == 'Account':
        arows.append(
            '<tr><td {}><b>Total</b></td><td {}><b>${}</b></td></tr>'
            .format(style, style, sum([o.balance for o in objectlist]))
        )
    else:
        rows.append(
            '<tr><td {}><b>Total</b></td><td {}><b>${}</b></tr>'
            .format(style, style, sum([o.amount for o in objectlist]))
        )
    if str(i) == 'Account':
        # arows.append(
        #     '<tr><form method="POST"><td><input type="text" name="_name"></td>'
        #     '<td><input type="text" name="balance"></td><td><select name="type"'
        #     '><option value="checking">checking</option><option value="savings">'
        #     'savings</option><option value="'
        #     'credit card">credit card</option></select><td><input type="text" '
        #     'name="nickname"></td'
        #     '><td><input style="width:7em" type="submit" value="Add Row"></td>'
        #     '</form><tr>'
        # )
        return table1.replace('{rows}', ''.join(arows))
    else:
        # rows.append(
        #     '<tr><form method="POST"><td><input type="text" name="_name"></td>'
        #     '<td><input type="text" name="amount"><td><input style="width:7em" '
        #     'type="submit" value="Add Row"></td><td><input type="text" name="'
        #     'note"></td><td><input type="text" name="confirmation"></td></form>'
        #     '<tr>'
        # )
        return table.replace('{rows}', ''.join(rows))

accounts_table = create_table(accounts)
incomes_table = create_table(incomes)
expenses_table = create_table(expenses)

def create_balance():
    balance_table = (
        '<table border=0><th>Total Credits</th><th>Total Debits</th><th>Total '
        'Balance</th><tr><td style="color:darkgreen"><b>${}</b></td><td style='
        '"color:darkred"><b>${}</b></td><td style="color:darkblue"><b>${}</b>'
        '</td></tr></table>'
        .format(
            sum([i.amount for i in incomes]),
            sum([e.amount for e in expenses]),
            sum([i.amount for i in incomes]) - sum([e.amount for e in expenses]),
        )
    )
    return balance_table

create_balance()

finances = (
    finances.replace('{accounts}', accounts_table)
    .replace('{incomes}', incomes_table)
    .replace('{expenses}',expenses_table)
    .replace('{balance}', create_balance())
)

with open('templates/index.html', 'w') as out:
    out.write(finances)

