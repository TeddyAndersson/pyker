from random import shuffle
from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static
    deck with the list of Card instances. Each object instantiated simply
    makes a copy of this object and shuffles it.
    """

    _COMPLETE_DECK = list()

    def __init__(self):
        self.shuffle()

    def __str__(self):
        output = [str(card) for card in self.cards]
        return ', '.join(output)

    def __repr__(self):
        return f'Deck()'

    def shuffle(self):
        self.cards = Deck.get_ordered_deck()
        shuffle(self.cards)

    def draw(self, number_of_cards=1):
        drawn_cards = [self.cards.pop() for i in range(number_of_cards)]
        return drawn_cards

    def burn(self):
        self.draw(number_of_cards=1)

    @staticmethod
    def get_ordered_deck():
        if Deck._COMPLETE_DECK:
            return list(Deck._COMPLETE_DECK)

        for rank in Card.STR_RANKS:
            for suit in Card.STR_SUITS:
                Deck._COMPLETE_DECK.append(Card(rank=rank, suit=suit))

        return list(Deck._COMPLETE_DECK)
