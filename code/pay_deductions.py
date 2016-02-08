import sys
from pprint import pprint, pformat
from datetime import datetime as dt
from mixins import IO


data = [
    {
        'date': '2-5-16',
        'estimated': {
            'pay': 1460.01,
            'ford': -462.08,
            'chase overdraft': -322.18,
            'credit cards': -97.0,
            'chase ink': -76.00,
            'gas': -75.00,
        },
        'actual': {
            'chase overdraft': -322.18,
            'pay': 1460.01,
            'ford': -462.08,
            'gas': sum([-24.53, -15.81, -19.70]),
            'car supplies': -14.05,
            'snacks': sum([-3.83, -2.15, -4.20, -2.15, -2.71]),
            'chase ink': -76.00,
            'post office': -13.78,
            'premier bank card': -97.0,
            'costco': -141.08,
            'itunes': -1.07,
            'groceries': -2.51,
            'food': sum([-2.79, -8, -5.57, -5.15, -10.5])
        }
    },
    {
        'date': '2-12-16',
        'estimated': {
            'pay': 1460.01,
            'rich dad education': -500.0,
            'chase business overdraft': -232.15,
            'chase ink': -116.00,
            'renters insurance': -220,
            'cps energy': -64.47
        },
        'actual': {'pay': 1460.01}
    },
    {
        'date': '2-19-16',
        'estimated': {
            'pay': 1460.01,
            'credit cards': -200.0,
            'toll bill': sum([-83.84, -37.41]),
            'bofa overdraft': -182.52,
            'ford': -600
        },
        'actual': {'pay': 1460.01}
    },
    {
        'date': '2-26-16',
        'estimated': {
            'pay': 1460.01,
            'rent': -1133,
        },
        'actual': {'pay': 1460.01}
    }
]

line = '\n' + '=' * 60 + '\n'


class Deductions(IO):

    def __init__(self, index=-1):
        self.index = index
        self.date = data[index]['date']

    def __iter__(self):
        dates = []
        for i, date in enumerate(data):
            self.__init__(i)
            dates.append(self.__repr__())
        return (d for d in dates)

    def __repr__(self):
        return self._estimated() + self._actual()

    def _estimated(self):
        output = 'Date: {} | Pay: ${} | ESTIMATED\n\n'.format(
            data[self.index]['date'], data[self.index]['estimated']['pay'], line=line)
        return self._prepare_output('estimated', output)

    def _actual(self):
        output = 'Date: {} | Pay: ${} | ACTUAL\n\n'.format(
            data[self.index]['date'], data[self.index]['actual']['pay'], line=line)
        return self._prepare_output('actual', output)

    def _prepare_output(self, key, output):
        self.total = data[self.index][key]['pay']
        data[self.index][key]['savings'] = -1 * round(self.total * .1, 2)
        if self.index != 0:
            data[self.index][key]['misc'] = -1 * round(self.total * .06849, 2)
        else:
            data[self.index][key]['misc'] = -1 * round(self.total * .05, 2)
        self.max_len_names = max([len(k) for k in data[self.index][key].keys()]) + 7
        output += 'Name'.ljust(self.max_len_names) + 'Amount'.ljust(14)  + 'Balance\n'
        output += '' + '-' * (self.max_len_names + 22) + '\n'
        for k, v in sorted(data[self.index][key].items()):
            if k not in ('pay', 'date'):
                output += '{}${}${}\n'.format(
                    k.ljust(self.max_len_names),
                    str(abs(v)).ljust(13),
                    str(round(self.total, 2) + v))
                self.total += v
        self.total = round(self.total, 2)
        # Fix -0.0 case
        self.total = abs(self.total) if str(self.total) == '-0.0' else self.total
        output += '\nTotal left: ${}\n'.format(str(self.total))
        output += line
        print output
        return output


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
        output = ''.join(list(Deductions()))
        print output
        with open('logs/pay/deductions_all_{}.txt'.format(
            dt.now().strftime('%a_%b_%d_%Y')), 'w') as out:
            out.write(output)

    @classmethod
    def single(cls):
        arg2 = int(cls.arg2 or -1)
        d = Deductions(arg2)
        d.write('logs/pay/deductions_{}.txt'.format(d.date), True)


if __name__ == '__main__':
    Main.run()
