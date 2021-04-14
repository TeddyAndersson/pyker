from .hand_rank_lookup import HandRankLookupTable


class HandEvaluator:

    def __init__(self):
        self.lookup_table = HandRankLookupTable()

    def evaluate_hand_potential(self, hand, community_cards, unknown_cards):
        zero_list = [0]*3
        potential = [zero_list[:], zero_list[:]]
        potential_total = zero_list[:]

        ahead_index = 0
        tied_index = 1
        behind_index = 2

        unknown_two_card_combinations = itertools.combinations(
            unknown_cards, 2)

        # Consider all two card combinations of
        # the remaining cards for the opponent.
        for oppoponent_hand_combo in unknown_two_card_combinations:
            potential_index = 0
            opponent_hand_rank = self.evaluate_hand_rank(
                oppoponent_hand_combo)
            if player.hand.rank < opponent_hand_rank:
                potential_index = ahead_index
            elif player.hand.rank == opponent_hand_rank:
                potential_index = tied_index
            else:
                potential_index = behind_index

            potential_total[potential_index] += 1

            # All possible board cards to come.
            for turn_river_combo in unknown_two_card_combinations:
                board_cards = self.community_cards + list(turn_river_combo)

                community_card_ints = Card.cards_to_card_ints(board_cards)

                player_hand_card_ints = Card.cards_to_card_ints(
                    player.hand.cards)

                opponent_hand_card_ints = Card.cards_to_card_ints(
                    oppoponent_hand_combo)

                player_best = self.evaluate_hand_rank(
                    player_hand_card_ints, community_card_ints)

                opponent_best = self.evaluate_hand_rank(
                    opponent_hand_card_ints, community_card_ints)

                if player_best < opponent_best:
                    potential[potential_index][ahead_index] += 1
                elif player_best == opponent_best:
                    potential[potential_index][tied_index] += 1
                else:
                    potential[potential_index][behind_index] += 1

        # Were behind but moved ahead
        positive_potential = (int(potential[behind_index][ahead_index]) + int(potential[behind_index][tied_index])/2 +
                              int(potential[tied_index][ahead_index])/2) / (int(potential_total[behind_index]) + int(potential_total[tied_index]))

        # Were ahead but fell behind
        negative_potential = (int(potential_total[ahead_index][behind_index])+int(potential[tied_index]
                                                                                  [behind_index])/2+int(potential[ahead_index][tied_index])/2) / (int(potential_total[ahead_index])+int(potential_total[tied_index]))

        return positive_potential, negative_potential

    def evaluate_hand_strength(self, hand, community_cards, unknown_cards):
        ahead = 0
        tied = 0
        behind = 0

        hand_rank = self.evaluate_hand_rank(hand, community_cards)
        unknown_hand_combinations = itertools.combinations(
            unknown_cards, 2)

        for hand_combo in unknown_hand_combinations:
            opponent_hand_rank = self.evaluate_hand_rank(
                hand_combo, community_cards)
            if hand_rank < opponent_hand_rank:
                ahead += 1
            elif hand_rank == opponent_hand_rank:
                tied += 1
            elif hand_rank > opponent_hand_rank:
                behind += 1

        hand_strength = (ahead+tied/2)/(ahead+tied+behind)
        return hand_strength

    def evaluate_hand_rank(self, hand, community_cards):
        cards = hand + community_cards
        number_of_cards = len(cards)

        if number_of_cards == 2:
            return self._two_card_eval(cards)

        elif number_of_cards == 5:
            return self._five_card_eval(cards)

        elif number_of_cards == 6 or number_of_cards == 7:
            return self._six_and_seven_card_eval(cards)

    def _five_card_eval(self, cards):

        if self._is_hand_flushed(cards):
            q = (cards[0] | cards[1] | cards[2]
                 | cards[3] | cards[4]) >> 16
            prime = Card.prime_product_from_rankbits(q)
            return self.lookup_table.flush_lookup[prime]

        else:
            prime = Card.prime_product_from_hand(cards)
            return self.lookup_table.unsuited_lookup[prime]

    def _six_card_plus_eval(self, cards):

        min_rank = HandRankLookupTable.MAX_HIGH_CARD

        all_five_card_combinations = itertools.combinations(cards, 5)

        for five_card_combo in all_five_card_combinations:
            rank = self._five_card_eval(five_card_combo)
            if rank < min_rank:
                min_rank = rank

        return min_rank

    def _is_hand_flushed(self, cards):
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            return True
        return False
