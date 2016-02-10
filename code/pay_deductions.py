import sys
import json
from pprint import pprint, pformat
from datetime import datetime as dt
from mixins import IO

line = '\n' + '=' * 60 + '\n\n'


class Deductions(IO):

    def __init__(self, index=-1):
        self.index = index
        self.data = json.loads(self.read('../data/deductions.json'))['items']
        self.date = self.data[index]['date']

    def __iter__(self):
        dates = []
        for i, date in enumerate(self.data):
            self.__init__(i)
            dates.append(self.__repr__())
        return (d for d in dates)

    def __repr__(self):
        return self._estimated() + self._actual()

    def _estimated(self):
        output = 'Date: {} | Pay: ${} | ESTIMATED\n\n'.format(
            self.data[self.index]['date'],
            self.data[self.index]['estimated']['pay'],
            line=line)
        return self._prepare_output('estimated', output)

    def _actual(self):
        output = 'Date: {} | Pay: ${} | ACTUAL\n\n'.format(
            self.data[self.index]['date'],
            self.data[self.index]['actual']['pay'],
            line=line)
        return self._prepare_output('actual', output)

    def _prepare_output(self, key, output):
        self.total = self.data[self.index][key]['pay']
        self.data[self.index][key]['savings'] = -1 * round(self.total * .1, 2)
        self.max_len_names = max([len(k) for k in self.data[self.index]
                                 [key].keys()]) + 7
        self._misc(key)
        output += 'Name'.ljust(self.max_len_names) + 'Amount'.ljust(14)  +\
            'Balance\n'
        output += '' + '-' * (self.max_len_names + 22) + '\n'
        for k, v in sorted(self.data[self.index][key].items()):
            v = sum(v) if isinstance(v, list) else v
            if k not in ('pay', 'date'):
                output += '{}${}${}\n'.format(
                    k.ljust(self.max_len_names),
                    str(v).ljust(13),
                    str(round(self.total, 2) + v))
                self.total += v
        self.total = round(self.total, 2)
        self.total = abs(self.total) if str(self.total) == '-0.0' else\
            self.total
        output += '\nTotal left: ${}\n'.format(str(self.total))
        output += line
        return output

    def _misc(self, key):
        if self.index != 0:
            self.data[self.index][key]['misc'] = -1 * round(
                self.total * .06849, 2)
        else:
            self.data[self.index][key]['misc'] = -1 * round(self.total * .05, 2)

class Reports(object):

    def __repr__(self):
        return self._totals() + self._balance()

    def _totals(self):
        self.totals = {}
        output = 'Totals:\n'
        for actual in self:
            for k, v in actual.items():
                _sum = round(sum(v) if isinstance(v, list) else v, 2)
                if k in self.totals:
                    self.totals[k] += _sum
                else:
                    self.totals[k] = _sum
        for k, v in sorted(self.totals.items()):
            output += '\t{}: {}\n'.format(k, v)
        return output

    def _balance(self):
        output = '\nBalance: '
        balance = 0.0
        for t in self.totals:
            balance += self.totals[t]
        output += '${}'.format(balance)
        return output

    def __iter__(self):
        return (x['actual'] for x in Deductions().data)


class Main(object):
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    arg_map = {
        '-a': 'all',
        '-s': 'single',
        None: 'single'
    }

    @classmethod
    def run(cls):
        getattr(cls, cls.arg_map[cls.arg1])()

    @classmethod
    def all(cls):
        output = ''.join(list(Deductions())) + repr(Reports())
        print output
        with open('logs/pay/deductions_all_{}.txt'.format(
            dt.now().strftime('%a_%b_%d_%Y')), 'w') as out:
            out.write(output)

    @classmethod
    def single(cls):
        arg2 = int(cls.arg2 or -1)
        d = Deductions(arg2)
        print repr(d)
        d.write('logs/pay/deductions_{}.txt'.format(d.date), True)


if __name__ == '__main__':
    Main.run()
