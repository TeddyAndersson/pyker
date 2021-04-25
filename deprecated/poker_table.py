from .deck import Deck
from .player import Player
from .card import Card


class PokerTable:
    """
    This class represents the poker table.
    """
    STAGES = {
        1: 'PREFLOP',
        2: 'FLOP',
        3: 'TURN',
        4: 'RIVER'
    }

    def __init__(self, name: str = None, total_seats: int = 6, deck: Deck = None):
        if not isinstance(name, str):
            raise TypeError(f'{name} is not a string')

        if not isinstance(total_seats, int):
            raise TypeError(f'{total_seats} is not a integer')

        if not isinstance(deck, Deck):
            raise TypeError(f'{deck} is not an instance of class Deck')

        self.name = name
        self.total_seats = total_seats

        self.deck = deck
        self.players = []
        self.community_cards = []

    def __str__(self):
        return f'<Table name: {self.name}, total_seats: {self.total_seats},  deck: {self.deck}, players: {self.players}, community_cards: {self.community_cards}>'

    def add_player(self, player: Player = None):
        if not isinstance(player, Player):
            message = f'expected argument card to be instance of class Player got {player} instead'
            TypeError(message)

        if self.seat_available():
            self.players.append(player)
            print(f'Added {player.name} to table {self.name}')
        else:
            print(
                f'Max amount of seats is reach, [ {player.name} ] can not join table [ {self.name} ]')

    def seat_available(self):
        number_of_players = len(self.players)
        if number_of_players >= self.total_seats:
            return False
        return True

    def _discard_card(self):
        self.deck.draw(number_of_cards=1)

    def _add_community_cards(self, number_of_cards: int = 1):
        if not isinstance(number_of_cards, int):
            message = f'expected argument number_of_cards to be an integer got {number_of_cards} instead'
            raise TypeError(message)

        self._discard_card()
        cards = self.deck.draw(number_of_cards=number_of_cards)
        self.community_cards.extend(cards)

    def _deal_hands(self):
        for i in range(2):
            for player in self.players:
                player_card = self.deck.draw(number_of_cards=1)
                player.hand.add_card(player_card[0])

    def show_flop(self):
        print("Show Flop")
        self._add_community_cards(number_of_cards=3)

    def show_turn(self):
        print("Show Turn")
        self._add_community_cards(number_of_cards=1)

    def show_river(self):
        print("Show River")
        self._add_community_cards(number_of_cards=1)

    def _clear_community_cards(self):
        self.community_cards = []

    def new_round(self):
        self._clear_community_cards()
        self._reset_player_hands()
        self.deck.shuffle()
        self._deal_hands()
        self._shift_positions()

    def _shift_positions(self):
        max_position = len(self.players)
        for player in self.players:
            position_shift = player.position-1
            if position_shift == 0:
                position_shift = max_position
            player.set_position(position_shift)

    def set_hand_ranks(self, evaluator):
        for player in self.players:
            player.hand.set_rank(
                self.community_cards, evaluator)

    def _reset_player_hands(self):
        for player in self.players:
            player.hand.reset()

    def print_players(self):
        for player in self.players:
            print(player)
