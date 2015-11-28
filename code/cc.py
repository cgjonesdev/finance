import sys
import json
from pprint import pprint, pformat
from operator import attrgetter
from math import ceil


with open('../data/cc.json') as f:
    data = json.loads(f.read())


class CreditCard(object):
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(''.join(self.name.split()).lower())

    def __repr__(self):
        output = ''
        for k, v in self.__dict__.items():
            output += '{}: {}\n'.format(' '.join(k.split('_')).title(), v)
        return output

    def __add__(self, other):
        self.balance += other.balance
        return self

    def __radd__(self, other):
        self.balance += other.balance
        return self

    def __sub__(self, other):
        self.balance -= other.balance
        return self

    def __rsub__(self, other):
        self.balance -= other.balance
        return self

    def __gt__(self, other):
        return self if self.balance > other.balance else other

    def __lt__(self, other):
        return self if self.balance < other.balance else other


class CardHolder(object):
    def __init__(self, cards, cash=0.0):
        self.cards = cards
        self.cash = cash

    def __repr__(self):
        self.payment_amounts()
        output = ''
        output += '\nTotal balances: ${}\n'.format(self.balances())
        output += 'Total credit limit: ${}\n'.format(self.limits())
        output += 'Total available credit: ${}\n'.format(self.available_credit())
        output += 'Total minimum payments: ${}\n'.format(self.minimums())
        output += '\nPayments to make:\n\t{}\n'.format(
                pformat([{card.name: ('$'+str(round(card.payment_amount, 2)),
                         '| due by {}'.format(card.due_date))}
                         for card in self.cards]
            ).replace('\n', '\n\t')\
             .replace('u\'', '')\
             .replace('[', ' ')\
             .replace('{', ''))\
             .replace('}', '')\
             .replace('(', '')\
             .replace(')', '')\
             .replace(']', '')\
             .replace('\'', '')\
             .replace(',', '')
        output += '\nCash: ${}\n'.format(self.cash)
        return output

    def balances(self):
        return sum([card.balance for card in self.cards])

    def limits(self):
        return sum([card.limit for card in self.cards])

    def minimums(self):
        return sum([card.minimum_payment for card in self.cards])

    def available_credit(self):
        return self.limits() - self.balances()

    def payment_amounts(self):
        # Test that cash input is not less than total minimum payments
        assert self.cash >= self.minimums(), ('${} is less than the ${} '
            'required to pay your minimum balances.'.format(
                self.cash, self.minimums()
            )
        )
        payment_amounts = []
        diff = 0.0
        for card in self.cards:
            if card.balance == 0.0:
                continue
            payment_amount = round(card.balance / self.balances() * self.cash, 2)
            card.payment_amount = payment_amount
            if payment_amount < card.minimum_payment:
                card.payment_amount = card.minimum_payment
            elif payment_amount >= card.balance:
                card.payment_amount = card.balance
        over_minimum_cards = sorted(
            [card for card in self.cards if card.payment_amount >
             card.minimum_payment], key=attrgetter('payment_amount'),
            reverse=True
        )
        while sum([card.payment_amount for card in self.cards]) > self.cash:
            for card in over_minimum_cards:
                if card.payment_amount <= card.minimum_payment:
                    continue
                card.payment_amount -= .01

        # Test that cash input is not greater than the total of all balances
        assert ceil(
            sum([card.payment_amount for card in self.cards])
        ) >= ceil(self.cash), (
                '${} is more than the ${} you need to pay all your balances.'
                .format(
                    ceil(self.cash),
                    ceil(sum([card.payment_amount for card in self.cards])
                )
            )
        )
        # Test assertion that input cash == spent on card payments
        assert ceil(
            sum([card.payment_amount for card in self.cards])
        ) == ceil(self.cash), '{} != {}'.format(
            ceil(sum([card.payment_amount for card in self.cards])),
            ceil(self.cash)
        )

    def make_payment(self, card, payment_amount):
        card.balance -= payment_amount
        card.available_credit += payment_amount



credit_cards = [
    CreditCard(cc) for cc in data['credit cards']['date']['11-27-15']
]
cardholder = CardHolder(
    credit_cards, float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
)
if not cardholder.cash:
    cardholder.cash = cardholder.minimums()
print repr(cardholder)
