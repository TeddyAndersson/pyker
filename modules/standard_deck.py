from random import shuffle
from .card_int import CardInt


class StandardDeck(list):

    _CARDS_IN_ORDER = list()

    def __init__(self):
        super().__init__()
        self.setup()
        self.burned_cards = list()

    def __str__(self):
        output = [str(card) for card in self]
        return ', '.join(output)

    def __repr__(self):
        return f'Deck()'

    def setup(self):
        cards = self.populate()
        self.extend(cards)

    def shuffle(self):
        self = shuffle(self)

    def get_card(self, rank, suit):
        card_int = CardInt(rank+suit)
        card_index = self.index(card_int)
        return self.pop(card_index)

    def draw_card(self):
        card = self.pop()
        return card

    def draw_several_cards(self, number: int):
        cards = [self.draw_card() for i in range(number)]
        return cards

    def burn_card(self):
        card = self.pop()
        self.burned_cards.append(card)

    def populate(self):
        if self._CARDS_IN_ORDER:
            return list(self._CARDS_IN_ORDER)

        suits = CardInt.STR_SUITS
        ranks = CardInt.STR_RANKS
        for suit in suits:
            for rank in ranks:
                card_str = rank+suit
                card_int = CardInt(card_str)
                self._CARDS_IN_ORDER.append(card_int)
        return list(self._CARDS_IN_ORDER)
