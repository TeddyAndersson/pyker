import itertools
from .lookup_table import HandRankLookupTable
from .card import Card


class HandRankEvaluator(object):
    """
    Evaluates hand strengths using a variant of Cactus Kev's algorithm:
    http://suffe.cool/poker/evaluator.html
    """

    def __init__(self):
        self.table = HandRankLookupTable()

        self.hand_size_map = {
            5: self._five_card_eval,
            6: self._six_card_plus_eval,
            7: self._six_card_plus_eval
        }

    def evaluate(self, hand, community_cards):
        cards = hand + community_cards
        number_of_cards = len(cards)
        return self.hand_size_map[number_of_cards](cards)

    def _is_hand_flushed(self, cards):
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            return True
        return False

    def _five_card_eval(self, cards):

        if self._is_hand_flushed(cards):
            q = (cards[0] | cards[1] | cards[2]
                 | cards[3] | cards[4]) >> 16
            prime = Card.prime_product_from_rankbits(q)
            return self.table.flush_lookup[prime]

        # otherwise
        else:
            prime = Card.prime_product_from_hand(cards)
            return self.table.unsuited_lookup[prime]

    def _six_card_plus_eval(self, cards):

        minimum_score = HandRankLookupTable.MAX_HIGH_CARD

        all_five_card_combinations = itertools.combinations(cards, 5)

        for five_card_combo in all_five_card_combinations:
            score = self._five_card_eval(five_card_combo)
            if score < minimum_score:
                minimum_score = score

        return minimum_score

    @staticmethod
    def get_rank_class(hand_rank):
        """
        Returns the class of hand given the hand hand_rank
        returned from evaluate.
        """
        if hand_rank >= 0 and hand_rank <= HandRankLookupTable.MAX_STRAIGHT_FLUSH:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_STRAIGHT_FLUSH]

        elif hand_rank <= HandRankLookupTable.MAX_FOUR_OF_A_KIND:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_FOUR_OF_A_KIND]

        elif hand_rank <= HandRankLookupTable.MAX_FULL_HOUSE:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_FULL_HOUSE]

        elif hand_rank <= HandRankLookupTable.MAX_FLUSH:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_FLUSH]

        elif hand_rank <= HandRankLookupTable.MAX_STRAIGHT:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_STRAIGHT]

        elif hand_rank <= HandRankLookupTable.MAX_THREE_OF_A_KIND:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_THREE_OF_A_KIND]

        elif hand_rank <= HandRankLookupTable.MAX_TWO_PAIR:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_TWO_PAIR]

        elif hand_rank <= HandRankLookupTable.MAX_PAIR:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_PAIR]

        elif hand_rank <= HandRankLookupTable.MAX_HIGH_CARD:
            return HandRankLookupTable.MAX_TO_RANK_CLASS[HandRankLookupTable.MAX_HIGH_CARD]

        else:
            raise Exception("Inavlid hand rank, cannot return rank class")

    @staticmethod
    def rank_class_to_string(class_int):
        """
        Converts the integer class hand score into a human-readable string.
        """
        return HandRankLookupTable.RANK_CLASS_TO_STRING[class_int]
