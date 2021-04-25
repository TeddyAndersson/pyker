from .card_int import CardInt
from .card_collection import CardCollection

from .helpers import argument_exception_message


class Player(object):

    def __init__(self, name: str = None, cards: CardCollection = None, initial_stack: int = 0, active: bool = False, private: bool = True):
        self.name = name
        self.cards = cards
        self.balance = initial_stack
        self.private = private
        self.active = active
        self.dead = False

    def __str__(self):
        return f'{self.name} with {str(self.cards)}'

    def __repr__(self):
        return f'Player(name={self.name}, cards={repr(self.cards)})'

    def add_card(self, card: CardInt):
        if not self.private:
            self.cards.append(card)

    def swap_card(self, card, index):
        self.cards.replace(card, index)

    def set_balance(self, amount: int = None):
        assert isinstance(amount, int), argument_exception_message(
            'amount', int, amount)
        self.balance = amount
