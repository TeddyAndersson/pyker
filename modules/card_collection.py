from .hand_rank_lookup import HandRankLookupTable
from .poker_hand_evaluator import HandEvaluator
from .card_int import CardInt


class CardCollection(list):

    def __init__(self, evaluator: HandEvaluator = None):
        self.rank = None
        self.strength = None
        self.potential = None
        self.evaluator = evaluator

    def __str__(self):
        cards_string = ', '.join([str(card) for card in self])
        return f'cards: {cards_string}'

    def __repr__(self):
        return 'CardCollection()'

    def append(self, item):
        if not isinstance(item, CardInt):
            raise TypeError(f'{item} is not of instance {CardInt}')
        super(CardCollection, self).append(item)

    def set_strength(self):
        pass

    def set_potential(self):
        pass

    def set_rank(self, community_cards):
        pass
