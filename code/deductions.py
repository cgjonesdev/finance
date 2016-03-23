import sys
import json
from pprint import pprint, pformat
from datetime import datetime as dt
from operator import itemgetter
from mixins import IO

double_line = '\n' + '=' * 60 + '\n\n'
_sum = lambda v: round(sum(v) if isinstance(v, list) else v, 2)
avg = lambda v, c: round(_sum(v) / c, 2)


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
        line = '-' * 60 + '\n'
        output = 'Date: {} | Pay: ${} | ESTIMATED\n\n'.format(
            self.data[self.index]['date'],
            self.data[self.index]['estimated']['pay'],
            line=double_line)
        return self._prepare_output('estimated', output)

    def _actual(self):
        try:
            output = 'Date: {} | Pay: ${} | ACTUAL\n\n'.format(
                self.data[self.index]['date'],
                self.data[self.index]['actual']['pay'],
                line=double_line)
            return self._prepare_output('actual', output)
        except:
            return ''

    def _prepare_output(self, key, output):
        self.total = self.data[self.index][key]['pay']
        if self.index in range(3):
            self.data[self.index][key]['savings'] = -1 * round(self.total * .1, 2)
        elif self.index == 3:
            self.data[self.index][key]['savings'] = -1 * round(self.total * .15, 2)
        else:
            self.data[self.index][key]['savings'] = -1 * round(self.total * .2, 2)
        self.max_len_names = max([len(k) for k in self.data[self.index]
                                 [key].keys()]) + 7
        # if key == 'estimated':
        #     self.data[self.index][key]['misc'] = -1 * round(
        #         self.total * (100.0 / (self.data[self.index][key]['pay'] or 1.0)), 2)
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
        output += double_line
        return output


class HTMLTable(Deductions):

    def __repr__(self):
        output = '<table>\n\t'
        self.total = self.data[self.index]['actual']['pay']
        if self.index in range(3):
            self.data[self.index]['actual']['savings'] = -1 * round(self.total * .1, 2)
        elif self.index == 3:
            self.data[self.index]['actual']['savings'] = -1 * round(self.total * .15, 2)
        else:
            self.data[self.index]['actual']['savings'] = -1 * round(self.total * .2, 2)
        self.max_len_names = max([len(k) for k in self.data[self.index]
                                 ['actual'].keys()]) + 7

        output += '<th>\n\t\t<tr>{}</tr>\n\t\t<tr>{}</tr>\n\t\t<tr>{}</tr>\n\t</th>\n\t'.format(
            'Name', 'Amount', 'Balance')
        for k, v in sorted(self.data[self.index]['actual'].items()):
            output += '<tr>\n\t'
            v = sum(v) if isinstance(v, list) else v
            if k not in ('pay', 'date'):
                output += '\t<td>{}</td>\n\t\t<td>${}</td>\n\t\t<td>${}</td>'.format(
                    k,
                    str(v),
                    str(round(self.total, 2) + v))
                self.total += v
            output += '\n\t</tr>\n\t'
        self.total = round(self.total, 2)
        output += '\n</table>'
        return output                                 


class Upcoming(IO):

    def __init__(self):
        self.data = json.loads(self.read('../data/deductions.json'))['upcoming']

    def __repr__(self):
        output = '\nUpcoming:\n\n'
        for item in self:
            output += '\t{}: ${}\n'.format(item['name'].title(), item['amount'])
        output += '\nTotal: ${}\n'.format(self.sum)
        return output

    def __iter__(self):
        return (x for x in sorted(self.data, key=itemgetter('amount'), reverse=True))

    def __add__(self, other):
        return self.sum + other

    def __sub__(self, other):
        return self.sum - other

    def __iadd__(self, other):
        self.data.append(other)
        return self

    @property
    def names(self):
        return (str(x['name']) for x in self)

    @property
    def amounts(self):
        return (x['amount'] for x in self)

    @property
    def sum(self):
        return sum(list(self.amounts))


class Reports(object):

    def __repr__(self):
        line_item_format = '{item}{total}{average}{percentage}'
        perc = lambda v, c, pay: round((avg(v, c) / pay) * 100, 1)
        line_items = set()
        items = set()
        counts = {}
        totals = {}
        averages = {}
        percentages = {}
        for actual in self:
            actual['savings'] = round(actual['pay'] * -1 * .15, 2)
            for k, v in actual.items():
                items.add(k)
                counts[k] = 1 if k not in counts else counts[k] + 1
                totals[k] = (_sum(v) if k not in totals else
                             round(totals[k] + _sum(v), 2))
                averages[k] = (avg(v, counts[k]) if k not in averages else
                               avg(totals[k], counts[k]))
                percentages[k] = (round(averages[k] / averages['pay'] if 'pay'
                                  in averages else averages[k] / actual['pay'], 3)
                                  * 100)
        self.totals = totals
        max_len_items = max([len(v) for v in items]) + 5
        max_len_totals = max([len(str(v)) for v in totals.values()]) + 10
        max_len_averages = max([len(str(v)) for v in averages.values()]) + 10
        max_len_percentages = max([len(str(v)) for v in percentages.values()]) + 10
        rows = []
        for row in zip(items, totals.values(), averages.values(), percentages.values()):
            rows.append(dict(zip(('item', 'total', 'average', 'percentage'), row)))
        for row in rows:
            row['item'] = row['item'].ljust(max_len_items)
            row['total'] = '$' + str(row['total']).ljust(max_len_totals)
            row['average'] = '$' + str(row['average']).ljust(max_len_totals)
        rows = sorted(rows, key=itemgetter('percentage'))

        items = [item.ljust(max_len_items) for item in items]
        totals = ['$' + str(v).ljust(max_len_totals) for v in
                  totals.values()]
        averages = ['$' + str(v).ljust(max_len_averages) for v in
                    averages.values()]
        percentages = [str(v) + '%'.ljust(max_len_percentages) for v in
                       percentages.values()]
        total_lens = (max_len_items + max_len_totals + max_len_averages +
                      max_len_percentages)
        header = ('Item name'.ljust(max_len_items) +
                  'Total +/-'.ljust(max_len_totals + 1) +
                  'Average +/-'.ljust(max_len_averages + 2) +
                  '% of avg pay\n' + '-' *  (total_lens + 1))
        result = [header]
        for row in rows:
            result.append(line_item_format.format(**row))
        return 'REPORTS:\n\n' + '\n'.join(result) + self.total_income + \
            self.total_expenses + self.balance

    def __iter__(self):
        return (x['actual'] for x in Deductions().data if 'actual' in x)

    def __len__(self):
        return sum(1 for x in self)

    @property
    def total_income(self):
        output = '\n\nTotal Income: '
        output += '${}'.format(
            str(sum(v for k, v in self.totals.items() if k in
                ('pay', 'starting balance', 'xfer from savings'))))
        return output

    @property
    def total_expenses(self):
        output = ' | Total Expenses: '
        output += '${}'.format(
            str(sum(v for k, v in self.totals.items() if k not in
                ('pay', 'starting balance', 'xfer from savings'))))
        return output

    @property
    def balance(self):
        output = ' | Balance: '
        self._balance = 0.0
        for t in self.totals:
            self._balance += self.totals[t]
        output += '${}'.format(self._balance)
        return output + '\n'



class Main(object):
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    arg_map = {
        '-a': 'all',
        '-s': 'single',
        '-u': 'upcoming',
        None: 'all'
    }
    for i in range(-1000, 1000):
        arg_map.update({str(i): 'single'})

    @classmethod
    def run(cls):
        getattr(cls, cls.arg_map[cls.arg1])()

    @classmethod
    def all(cls):
        output = ''.join(list(Deductions())) + repr(Reports())
        print output
        with open('logs/pay/deductions_all_{}.log'.format(
            dt.now().strftime('%a_%b_%d_%Y')), 'w') as out:
            out.write(output)

    @classmethod
    def single(cls):
        arg2 = (int(cls.arg2) if cls.arg2 else int(cls.arg1) if
                cls.arg1.isdigit() else -1)
        d = Deductions(arg2)
        print repr(d)
        d.write('logs/pay/deductions_{}.log'.format(d.date), True)

    @classmethod
    def upcoming(cls):
        upcoming = Upcoming()
        print repr(upcoming)
        upcoming.write('logs/pay/upcoming.log', True)


if __name__ == '__main__':
    Main.run()
