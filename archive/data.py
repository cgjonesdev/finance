import os

import accounts
import transactions


files = os.listdir('data')

print 'files:'
for f in files:
    f = 'data/{}'.format(f)
    print '\t', f
    with open(f) as _:
        lines = _.readlines()
    for line in lines:
        if 'account' in f:
            print '\t\t{}'.format(line.split('|')[3])
        elif 'transaction' in f:
            print '\t\t', line.split('|')[1]
print '\n'

print 'accounts:'
for attr in dir(accounts):
    if not attr.startswith('__') and 'Base' not in attr:
        print '\t', attr
print '\n'

print 'transactions:'
for attr in dir(transactions):
    if not attr.startswith('__') and 'Base' not in attr:
        print '\t', attr
print '\n'
