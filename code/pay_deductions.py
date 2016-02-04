import sys
from pprint import pprint, pformat
from mixins import IO


data = [
    {
        'date': '2-5-16',
        'pay': 1460.01,
        'chase overdraft': -322.18,
        'rich dad education': -500.0,
        'credit cards': -97.0,
        'chase business overdraft': -164.15,
        'costco': -48.16,
        'bofa overdraft': -182.52
    },
    {
        'date': '2-12-16',
        'pay': 1460.01,
        'ford': -600.0,
        'credit cards': -500.0,
        'costco': -200.0
    }
]


class Deductions(IO):

    def __init__(self, index=-1):
        self.index = index
        self.total = data[index]['pay']
        data[self.index]['savings'] = -1 * round(self.total * .1, 2)
        self.max_len_names = max([len(k) for k in data[self.index].keys()]) + 7

    def __iter__(self):
        dates = []
        for i, date in enumerate(data):
            self.__init__(i)
            dates.append(self.__repr__())
        return (d for d in dates)

    def __repr__(self):
        line = '\n' + '=' * 60 + '\n'
        output = 'Date: {} | Pay: ${}\n\n'.format(data[self.index]['date'], self.total, line=line)
        output += 'Name'.ljust(self.max_len_names) + 'Amount'.ljust(14)  + 'Balance\n'
        output += '' + '-' * (self.max_len_names + 22) + '\n'
        for k, v in data[self.index].items():
            if k not in ('pay', 'date'):
                output += '{}${}${}\n'.format(
                    k.ljust(self.max_len_names),
                    str(abs(v)).ljust(13),
                    str(round(self.total, 2) + v))
                self.total += v
        output += '\nTotal left: ${}\n'.format(str(round(self.total, 2)))
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
        list(Deductions())

    @classmethod
    def single(cls):
        arg2 = int(cls.arg2 or -1)
        Deductions(arg2).write('logs/pay/deductions.log', True)


if __name__ == '__main__':
    Main.run()
