with open('accounts.json') as _:
    a = _.readlines()

for i, line in enumerate(a, 1):
    print i, str(line[:-1])

