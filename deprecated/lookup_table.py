from .card import Card
import itertools


class HandRankLookupTable(object):
    """
    Number of Distinct Hand Values

    Straight Flush:     10
    Four of a Kind:     156
    Full House:         156
    Flush:              1277
    Stright:            10
    Three of a Kind:    858
    Two Pair:           858
    One Pair:           2860
    High Card:          + 1277
    -----------------------------
    Total               7462


    Here we create a lookup table which maps
        5 card hand's unique prime product => rank in range [1, 7462]

    Examples:
    * Royal flush (best hand possible)              => 1
    * 7-5-4-3-2 unsuited (worst hand possible)      => 7462

    """

    MAX_STRAIGHT_FLUSH = 10
    MAX_FOUR_OF_A_KIND = 166
    MAX_FULL_HOUSE = 322
    MAX_FLUSH = 1599
    MAX_STRAIGHT = 1609
    MAX_THREE_OF_A_KIND = 2467
    MAX_TWO_PAIR = 3325
    MAX_PAIR = 6185
    MAX_HIGH_CARD = 7462

    MAX_TO_RANK_CLASS = {
        MAX_STRAIGHT_FLUSH: 1,
        MAX_FOUR_OF_A_KIND: 2,
        MAX_FULL_HOUSE: 3,
        MAX_FLUSH: 4,
        MAX_STRAIGHT: 5,
        MAX_THREE_OF_A_KIND: 6,
        MAX_TWO_PAIR: 7,
        MAX_PAIR: 8,
        MAX_HIGH_CARD: 9
    }

    RANK_CLASS_TO_STRING = {
        1: "Straight Flush",
        2: "Four of a Kind",
        3: "Full House",
        4: "Flush",
        5: "Straight",
        6: "Three of a Kind",
        7: "Two Pair",
        8: "Pair",
        9: "High Card"
    }

    def __init__(self):

        self._high_cards = 1277

        self.flush_lookup = {}
        self.unsuited_lookup = {}

        self.set_lookups()

    def get_straight_flush_ranks(self):
        straight_flushes_in_rank_order = [
            7936,  # int('0b1111100000000', 2), # royal flush
            3968,  # int('0b111110000000', 2),
            1984,  # int('0b11111000000', 2),
            992,  # int('0b1111100000', 2),
            496,  # int('0b111110000', 2),
            248,  # int('0b11111000', 2),
            124,  # int('0b1111100', 2),
            62,  # int('0b111110', 2),
            31,  # int('0b11111', 2),
            4111  # int('0b1000000001111', 2) # 5 high
        ]
        return straight_flushes_in_rank_order

    def get_other_flush_ranks(self, straight_flushes_ranks):

        other_flushes = []
        flush_generator = self.compute_lexographically_next_bit_permutation(
            int('0b11111', 2))

        number_of_straight_flushes = len(straight_flushes_ranks)
        number_of_hands_with_all_unique_card_ranks = self._high_cards + \
            number_of_straight_flushes - 1

        for i in range(number_of_hands_with_all_unique_card_ranks):
            flush = next(flush_generator)

            is_straight_flush = False
            for straight_flush_rank in straight_flushes_ranks:
                if not flush ^ straight_flush_rank:
                    is_straight_flush = True

            if not is_straight_flush:
                other_flushes.append(flush)

        return other_flushes

    def update_flush_lookup(self, starting_rank, ranks):
        rank = starting_rank
        for i in ranks:
            primary_product = Card.prime_product_from_rankbits(i)
            self.flush_lookup[primary_product] = rank
            rank += 1

    def update_unsuited_lookup(self, starting_rank, ranks):
        rank = starting_rank
        for i in ranks:
            primary_product = Card.prime_product_from_rankbits(i)
            self.unsuited_lookup[primary_product] = rank
            rank += 1

    def set_lookups(self):
        straight_flush_ranks = self.get_straight_flush_ranks()
        other_flushes_ranks = self.get_other_flush_ranks(straight_flush_ranks)

        self.set_straight_flushes(straight_flush_ranks=straight_flush_ranks)

        self.set_other_flushes(other_flushes_ranks=other_flushes_ranks)

        self.set_straights(straight_ranks=straight_flush_ranks)

        self.set_high_cards(high_card_ranks=other_flushes_ranks)

        number_of_card_ranks = len(Card.INT_RANKS)
        backwards_ranks = list(range(number_of_card_ranks - 1, -1, -1))

        self.set_four_of_a_kind(backwards_ranks=backwards_ranks)

        self.set_full_house(backwards_ranks=backwards_ranks)

        self.set_three_of_a_kind(backwards_ranks=backwards_ranks)

        self.set_two_pairs(backwards_ranks=backwards_ranks)

        self.set_pairs(backwards_ranks=backwards_ranks)

    def set_straight_flushes(self, straight_flush_ranks):
        self.update_flush_lookup(starting_rank=1, ranks=straight_flush_ranks)

    def set_other_flushes(self, other_flushes_ranks):
        starting_rank = HandRankLookupTable.MAX_FULL_HOUSE + 1
        other_flushes_ranks.reverse()
        self.update_flush_lookup(
            starting_rank=starting_rank, ranks=other_flushes_ranks)

    def set_straights(self, straight_ranks):
        starting_rank = HandRankLookupTable.MAX_FLUSH + 1
        self.update_unsuited_lookup(
            starting_rank=starting_rank, ranks=straight_ranks)

    def set_high_cards(self, high_card_ranks):
        starting_rank = HandRankLookupTable.MAX_PAIR + 1
        self.update_unsuited_lookup(
            starting_rank=starting_rank, ranks=high_card_ranks)

    def set_four_of_a_kind(self, backwards_ranks):
        rank = HandRankLookupTable.MAX_STRAIGHT_FLUSH + 1

        for i in backwards_ranks:
            kicker_ranks = backwards_ranks[:]
            kicker_ranks.remove(i)
            for kicker_rank in kicker_ranks:
                primary_product = Card.PRIME_NUMBERS[i]**4 * \
                    Card.PRIME_NUMBERS[kicker_rank]
                self.unsuited_lookup[primary_product] = rank
                rank += 1

    def set_full_house(self, backwards_ranks):

        rank = HandRankLookupTable.MAX_FOUR_OF_A_KIND + 1

        for i in backwards_ranks:
            pair_ranks = backwards_ranks[:]
            pair_ranks.remove(i)
            for pair_rank in pair_ranks:
                primary_product = Card.PRIME_NUMBERS[i]**3 * \
                    Card.PRIME_NUMBERS[pair_rank]**2
                self.unsuited_lookup[primary_product] = rank
                rank += 1

    def set_three_of_a_kind(self, backwards_ranks):

        rank = HandRankLookupTable.MAX_STRAIGHT + 1

        for i in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(i)

            kicker_combinations = itertools.combinations(kickers, 2)

            for kicker_combo in kicker_combinations:
                card_1, card_2 = kicker_combo
                primary_product = Card.PRIME_NUMBERS[i]**3 * \
                    Card.PRIME_NUMBERS[card_1] * Card.PRIME_NUMBERS[card_2]
                self.unsuited_lookup[primary_product] = rank
                rank += 1

    def set_two_pairs(self, backwards_ranks):
        rank = HandRankLookupTable.MAX_THREE_OF_A_KIND + 1

        tow_pair_combinations = itertools.combinations(backwards_ranks, 2)
        for two_pair_combo in tow_pair_combinations:
            pair_one, pair_two = two_pair_combo

            kickers = backwards_ranks[:]
            kickers.remove(pair_one)
            kickers.remove(pair_two)
            for kicker in kickers:
                primary_product = Card.PRIME_NUMBERS[pair_one]**2 * \
                    Card.PRIME_NUMBERS[pair_two]**2 * \
                    Card.PRIME_NUMBERS[kicker]
                self.unsuited_lookup[primary_product] = rank
                rank += 1

    def set_pairs(self, backwards_ranks):
        rank = HandRankLookupTable.MAX_TWO_PAIR + 1

        for pair_rank in backwards_ranks:

            kickers = backwards_ranks[:]
            kickers.remove(pair_rank)
            kickers_combinations = itertools.combinations(kickers, 3)

            for kicker_combo in kickers_combinations:
                kicker_one, kicker_two, kicker_three = kicker_combo
                primary_product = Card.PRIME_NUMBERS[pair_rank]**2 * Card.PRIME_NUMBERS[kicker_one] * \
                    Card.PRIME_NUMBERS[kicker_two] * \
                    Card.PRIME_NUMBERS[kicker_three]
                self.unsuited_lookup[primary_product] = rank
                rank += 1

    def compute_lexographically_next_bit_permutation(self, bits):
        """
        Computes the lexicographically next bit permutation

        Bit hack from here:
        http://www-graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation

        Generator does this in poker order rank
        so no need to sort when done.
        """

        t = (bits | (bits - 1)) + 1
        next = t | ((((t & -t) // (bits & -bits)) >> 1) - 1)

        yield next
        while True:
            t = (next | (next - 1)) + 1
            next = t | ((((t & -t) // (next & -next)) >> 1) - 1)
            yield next
