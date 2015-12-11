import sys
import os
import json
from datetime import datetime
from pprint import pprint, pformat
from operator import attrgetter
from math import ceil


path = sys.argv[0].split('/')
if path[0] == 'code':
    path = '.'
elif path[0] == 'creditcards.py':
    path = '..'
else:
    path = '/'.join(path[:-2])
with open(path + '/data/creditcards.json') as f:
    data = json.loads(f.read())

class CreditCard(object):
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        output = ''
        output += '{}\n'.format(self.name)
        output += '   PAYMENT AMOUNT: ${}\n'.format(round(abs(self.payment_amount), 2))
        for k, v in self.__dict__.items():
            if k not in ('name', 'payment_amount'):
                if isinstance(v, float):
                    output += '   {}: ${}\n'.format(k, round(abs(v), 2))\
                        .replace('_', ' ').title()
                else:
                    if k == 'confirmation':
                        output += '   {}: {}\n'.format(k.title(), v.upper())\
                            .replace('_', ' ')
                    else:
                        output += '   {}: {}\n'.format(k, v)\
                            .replace('_', ' ').title()
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
    def __init__(self, cash=0.0):
        self.cards = []
        self.cash = cash

    def __repr__(self):
        self.payment_amounts()
        line = '-' * 60
        output = \
            '\n{}\n{line}\n\nTotal Balances: ${}'\
            '\nTotal Credit Limit: ${}'\
            '\nTotal Available Credit: ${}'\
            '\nTotal Minimum Payments: ${}'\
            '\n\nCash: ${}\n'\
            .format(
                '\n'.join([repr(card) for card in self]),
                self.balances(),
                self.limits(),
                self.available_credit(),
                self.minimums(),
                self.cash,
                line=line)
        with open(
            datetime.now().strftime(path + '/code/%d%b%Y_cc.log'), 'w') as _:
            _.write(output)
        return output

    def __iter__(self):
        return (card for card in self.cards)

    def __len__(self):
        count = 0
        for card in self.cards:
            count += 1
        return count

    def __contains__(self, card):
        return card in self.cards

    def __add__(self, card):
        self.cards.append(card)
        self.name = card

    def __sub__(self, card):
        if card in self:
            self.cards.remove(card)

    def __getitem__(self, card_name):
        for card in self:
            if card_name in (card.name for card in self):
                return card

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


if __name__ == '__main__':
    cardholder = CardHolder()
    credit_cards = data['credit_cards']
    for card in credit_cards:
        name = card.keys()[0]
        data = card[name]['transactions'][-1]
        data.update({'name': name})
        cardholder + CreditCard(data)
        # print repr(cardholder[name])

    cardholder.cash = float(sys.argv[1]) if len(sys.argv) > 1 else cardholder.minimums()
    print repr(cardholder)
