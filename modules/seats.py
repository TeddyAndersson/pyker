from .player import Player
from .helpers import argument_exception_message


class Seat:
    def __init__(self, player: Player = None, index: int = None):
        self.player = player
        self.index = index

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        if isinstance(value, Player) or value == None:
            self._player = value
        else:
            raise TypeError(argument_exception_message(
                'player', Player, value))

    def reset(self):
        self.player = None


class SeatCollection(list):

    def __init__(self, size: int = 9):
        super().__init__()
        self._setup_available_seats(size=size)

    def _setup_available_seats(self, size):
        for i in range(size):
            self.append(Seat(index=i))

    def add(self, seat: Seat):
        self.append(seat)

    def reset_all(self):
        for seat in self:
            seat.reset()

    def reset(self, seat):
        seat_index = self.index(seat)
        self[seat_index].reset()

    def is_seat_available(self, index: int = None):
        if not isinstance(index, int):
            raise TypeError(f'{index} is not a integer')

        seat = self[index]
        if not seat:
            return False
        return True

    def get_first_available_seat(self):
        if len(self.available) == None:
            return None

        return self.available[0]

    @property
    def players(self):
        return [seat.player for seat in self if not seat.player == None]

    @property
    def occupied(self):
        seat_list = self
        return [seat for seat in seat_list if not seat.player == None]

    @property
    def available(self):
        seat_list = self
        available_seats = [seat for seat in seat_list if seat.player == None]
        if len(available_seats) == 0:
            return None
        return available_seats

    @property
    def active_players(self):
        occupied_seats = self.occupied
        return [seat.player for seat in occupied_seats if seat.player.active]

    @property
    def folded_players(self):
        occupied_seats = self.occupied
        return [seat.player for seat in occupied_seats if not seat.player.active]

    @property
    def dead_players(self):
        occupied_seats = self.occupied
        return [seat.player for seat in occupied_seats if seat.player.dead]

    def get_next_available(self):
        available
