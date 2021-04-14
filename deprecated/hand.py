from .card import Card
from .evaluator import HandRankEvaluator
from .lookup_table import HandRankLookupTable


class Hand:
    """
    This class represents a poker hand.
    """

    def __init__(self):
        self.cards = []
        self.rank = None
        self.strength = None

    def __str__(self):
        return f'cards: {Card.cards_to_str(self.cards)}, rank: {self.rank}'

    def add_card(self, card):
        self.cards.append(card)

    def compare(self, hand):
        # compare this hand to another hand.
        pass

    def get_rank_procentage(self):
        return float(self.rank) / float(HandRankLookupTable.MAX_HIGH_CARD)

    def set_rank(self, new_rank):
        if not isinstance(new_rank, int):
            message = f'expected argument new_rank to be a integer got {new_rank} instead'
            raise TypeError(message)

        self.rank = new_rank

    def set_strength(self, new_strength: int):
        self.strength = new_strength

    def reset(self):
        self.cards = []
        self.rank = HandRankLookupTable.MAX_HIGH_CARD
