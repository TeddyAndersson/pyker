import itertools

from modules import Player
from modules import Hand
from modules import Deck
from modules import Card
from modules import HandRankEvaluator
from modules import HandRankLookupTable


def print_header(header: str, line_char='='):
    line = '='*20
    print('\n')
    print(line, header, line)


class Pyker:
    def __init__(self, deck: Deck = None):
        self.players = []
        self.deck = deck
        self.community_cards = []
        self.evaluator = HandRankEvaluator()
        self.hands_played = 0

    def add_player(self, player):
        self.players.append(player)

    def play_hand(self):
        self._start_hand()
        self._end_hand()

    def _start_hand(self):
        print_header('NEW HAND')
        self.deck.shuffle()
        self._deal_hands()
        self._play_betting_rounds()
        winners = self._get_winners()
        self._show_winners(winners)

    def _end_hand(self):
        self._shift_positions()
        self._increase_hands_played()
        self._reset_player_hands()
        self._reset_community_cards()

    def _deal_hands(self):
        for i in range(2):
            for player in self.players:
                cards = self.deck.draw(number_of_cards=1)
                player.hand.add_card(cards[0])

    def _increase_hands_played(self):
        self.hands_played += 1

    def _reset_player_hands(self):
        for player in self.players:
            player.hand.reset()

    def _reset_community_cards(self):
        self.community_cards = []

    def _shift_positions(self):
        max_position = len(self.players)
        for player in self.players:
            position_shift = player.position-1
            if position_shift == 0:
                position_shift = max_position

            player.set_position(position_shift)

    def _play_betting_rounds(self):
        for i, stage in enumerate(['PREFLOP', 'FLOP', 'TURN', 'RIVER']):
            print_header(stage)
            if stage == 'PREFLOP':
                # preflop betting
                print('No bets where made')
            else:
                self._deal_board(stage)
                self._set_hand_ranks()
                self._set_hand_strengths()
                self._set_hand_potential()
                self._show_board()
                self._show_player_summary()

    def _deal_board(self, stage):
        self.deck.burn()
        cards = []

        if stage == 'FLOP':
            cards = self.deck.draw(number_of_cards=3)

        if stage == 'TURN':
            cards = self.deck.draw(number_of_cards=1)

        if stage == 'RIVER':
            cards = self.deck.draw(number_of_cards=1)

        self._add_community_cards(cards)

    def _set_hand_ranks(self):
        for player in self.players:
            hand_rank = self._evaluate_hand_rank(player.hand.cards)
            player.hand.set_rank(hand_rank)

    def _evaluate_hand_rank(self, hand):
        hand_card_ints = Card.cards_to_card_ints(hand)
        community_card_ints = Card.cards_to_card_ints(self.community_cards)
        hand_rank = self.evaluator.evaluate(
            hand_card_ints, community_card_ints)
        return hand_rank

    def _calculate_hand_strength(self, player, player_index):
        ahead = 0
        tied = 0
        behind = 0

        unknown_cards = self._get_unknown_cards(player_index)
        unknown_hand_combinations = itertools.combinations(
            unknown_cards, 2)

        for hand_combo in unknown_hand_combinations:
            opponent_hand_rank = self._evaluate_hand_rank(hand_combo)
            if player.hand.rank < opponent_hand_rank:
                ahead += 1
            elif player.hand.rank == opponent_hand_rank:
                tied += 1
            elif player.hand.rank > opponent_hand_rank:
                behind += 1

        hand_strength = (ahead+tied/2)/(ahead+tied+behind)
        return hand_strength

    def _set_hand_strengths(self):
        if len(self.community_cards) < 3:
            raise ValueError(
                'Expected argument community_cards to be of lenght 3')

        for player_index, player in enumerate(self.players):
            hand_strength = self._calculate_hand_strength(player, player_index)
            player.hand.set_strength(new_strength=hand_strength)

    def _get_unknown_cards(self, player_index):
        copy_players = self.players[:]
        copy_players.pop(player_index)
        opponent_cards = self._get_opponent_cards(opponents=copy_players)
        unknown_cards = opponent_cards + self.deck.cards
        return unknown_cards

    def _set_hand_potential(self):
        if len(self.community_cards) == 3:
            for player_index, player in enumerate(self.players):
                hand_potentail = self._calculate_hand_potential(
                    player, player_index)
                print(hand_potentail)

    def _calculate_hand_potential(self, player, player_index):
        zero_list = [0]*3
        potential = [zero_list[:], zero_list[:]]
        potential_total = zero_list[:]

        ahead_index = 0
        tied_index = 1
        behind_index = 2

        unknown_cards = self._get_unknown_cards(player_index)
        unknown_two_card_combinations = itertools.combinations(
            unknown_cards, 2)

        # Consider all two card combinations of
        # the remaining cards for the opponent.
        for oppoponent_hand_combo in unknown_two_card_combinations:
            potential_index = 0
            opponent_hand_rank = self._evaluate_hand_rank(
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

                player_best = self.evaluator.evaluate(
                    player_hand_card_ints, community_card_ints)

                opponent_best = self.evaluator.evaluate(
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

    def _get_opponent_cards(self, opponents):
        opponent_cards = []
        for opponent in opponents:
            opponent_cards.extend(opponent.hand.cards)
        return opponent_cards

    def _add_community_cards(self, cards):
        self.community_cards.extend(cards)

    def _get_winners(self):
        winners = []

        # +1 worse than worst hand rank
        rank_to_beat = HandRankLookupTable.MAX_HIGH_CARD + 1
        for player in self.players:
            if player.hand.rank == rank_to_beat:
                winners.append(player)
                rank_to_beat = player.hand.rank

            if player.hand.rank < rank_to_beat:
                winners = [player]
                rank_to_beat = player.hand.rank

        return winners

    def _show_winners(self, winners):
        output = [
            f'{player.name} {str(player.hand)} {HandRankEvaluator.rank_class_to_string(class_int=HandRankEvaluator.get_rank_class(hand_rank=player.hand.rank))}' for player in winners]
        print_header('WINNERS')
        print(', \n'.join(output))

    def _show_board(self):
        output = [str(card) for card in self.community_cards]
        print('Community Cards: ', ', '.join(output))

    def _show_players(self):
        output = [str(player)
                  for player in self.players]
        print(', \n'.join(output))

    def _show_player_summary(self):
        output = []
        for player in self.players:
            hand_rank_procentage = player.hand.get_rank_procentage()
            procentage_str = f'percentage rank of all hands {hand_rank_procentage}'
            hand_rank_str = HandRankEvaluator.rank_class_to_string(
                class_int=HandRankEvaluator.get_rank_class(hand_rank=player.hand.rank))
            present_hand_strength = f'\n* hand_strength: {player.hand.strength}'
            present_hand_rank = f'\n* hand_rank: {hand_rank_str}, {procentage_str}'
            present_hand_cards = f'\n* cards: {[str(card) for card in player.hand.cards]}'
            present_player = f'\n{player.name}, position: {player.position}'
            player_summary = f'{present_player}{present_hand_cards}{present_hand_strength}{present_hand_rank}'
            output.append(player_summary)
        print('\n'.join(output))


players = [Player(name=f'Player {i}', hand=Hand(),
                  starting_position=i+1) for i in range(6)]

pyker = Pyker(deck=Deck())

for player in players:
    pyker.add_player(player)

for i in range(3):
    pyker.play_hand()
