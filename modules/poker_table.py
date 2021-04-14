import uuid

from dataclasses import dataclass

from .standard_deck import StandardDeck
from .player import Player
from .blinds import BlindStructure
from .seats import SeatCollection
from .helpers import argument_exception_message
from .helpers import find_index_for_first_none_value


class CommunityCards(list):

    _CARD_LIMIT = 5

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self = [None] * CommunityCards._CARD_LIMIT

    def add_card(self, card, position: int = None):
        assert isinstance(card, Card)
        card_index = position - 1
        if card_index == None:
            card_index == find_index_for_first_none_value(self)
        self[card_index] = card
        if len(self) == CommunityCards._CARD_LIMIT:
            raise ValueError('Can not add more than 5 cards')
        self.append(card)


@dataclass
class PokerTableConfig:
    size: int
    tournament: dataclass
    deck: StandardDeck
    button_starting_index: int = -1


class PokerTable(object):

    _MAX_COMMUNITY_CARDS = 5

    def __init__(self, config: PokerTableConfig = None):
        self.id = uuid.uuid4()
        self.deck = config.deck
        self.seats = config.size
        self.tournament = config.tournament
        self.button_index = config.button_starting_index
        self.community_cards = []
        self.deals = []
        self.bets = []

    def __str__(self):
        return f'The table [ {self.id} ] currently has {len(self.seats.occupied)} out of {len(self.seats)} seats occupied'

    def __repr__(self):
        return f'PokerTable( size={len(self.seats)}, deck={self.deck}, button_index: int = {self.button_index})'

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, value):
        assert isinstance(value, StandardDeck), argument_exception_message(
            'deck', Deck, value)
        self._deck = value

    @property
    def blinds(self):
        return self._blinds

    @blinds.setter
    def blinds(self, value):
        assert isinstance(value, BlindStructure), argument_exception_message(
            'blind_strucutre', BlindStructure, value)
        self.__blinds = value

    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, value):
        assert isinstance(value, int), argument_exception_message(
            'seats', int, value)
        self._seats = SeatCollection(size=value)

    @property
    def community_cards(self):
        return self._community_cards

    @community_cards.setter
    def community_cards(self, value):
        self._community_cards = CommunityCards()

    @property
    def button_index(self):
        return self._button_index

    @button_index.setter
    def button_index(self, value):
        assert isinstance(value, int), argument_exception_message(
            'button_index', int, value)
        self._button_index = value

    def move_button_forward(self, steps: int = 1):
        next_button_index = self.button_index + steps
        if self.button_index == len(self.seats.occupied) - 1:
            self.button_index = 0
        else:
            self.button_index = next_button_index

    def move_button_to_player(self, player):
        player_index = self.players.index(player)
        self.button_index = player_index

    def get_player(self, index):
        max_index = len(self.players) - 1
        if index > max_index:
            exceded_max_index_by = index - max_index
            return self.players[exceded_max_index_by - 1]
        return self.players[index]

    @property
    def player_on_button(self) -> Player:
        """
        Returns the player who is currently on the button
        """
        return self.seats.players[self.button_index]

    @property
    def player_on_small_blind(self) -> Player:
        small_blind_index = self.button_index+2
        player = self.get_player(small_blind_index)
        return player

    @property
    def player_on_big_blind(self) -> Player:
        big_blind_index = self.button_index+1
        player = self.get_player(big_blind_index)
        return player

    def add_player(self, player: Player = None, seat_number: int = None):
        if len(self.seats.available) == 0:
            raise Exception('All seats are currently occupied')

        if seat_number == None:
            seat = self.seats.get_first_available_seat()
            seat.player = player

        elif self.seats.is_seat_available(seat_number):
            self.seats[seat_number] = player

        else:
            raise Exception('The seat is already taken')

    def remove_player(self, player):
        pass

    def deal_card(self, player, rank, suit):
        card = self.deck.get_card(rank, suit)
        player.add_card(card)

    # def action(player: Player = None, action_type: str = None)
    # actions = ['fold', 'raise', 'call']
    # action_index = actions.index(action_type)
    # acton = actions[action_index]
    # player.action(action)

    # def post_blinds(self):
    #     blind = self.blind_structure.current_blind_level
    #     self.post_big_blind(size=blind.small_blind,
    #                         player=self.player_on_big_blind)
    #     self.post_small_blind(size=blind.big_blind,
    #                           player=self.player_on_small_blind)

    # def post_big_blind(self, size: int = None, player: Player = None):
    #     player.place_bet(size)
    #     pass

    # def post_small_blind(self, player):
    #     pass

    def get_all_opponent_cards(self, hero):
        opponent_hands = [
            player.hand for player in self.players if not player == hero]
        opponent_cards = []
        for hand in opponent_hands:
            opponent_cards.extend(hand)
        return opponent_cards

    def get_private_cards(self, player):
        opponent_cards = self.get_all_opponent_cards()
        private_cards = deck + deck.burned_cards + opponent_cards
        return private_cards

    @property
    def number_of_players(self):
        return len(self.players)

    @property
    def player_hands(self):
        return [player.hand for player in self.players]

    def get_str_hands(self):
        return [str(player.hand) for player in self.players]

    def add_community_cards(self, number=1):
        cards = self.deck.draw_cards(number=number)
        for card in cards:
            empty_card_slot_index = find_index_for_first_none_value(
                self.community_cards)
            if empty_card_slot_index == None:
                break

            self.community_cards[empty_card_slot_index] = card
