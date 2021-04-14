from .hand import Hand


class Player:
    """
    This class represents a poker player.
    """

    def __init__(self, name: str = None, hand: Hand = None, starting_position: int = None):
        if not isinstance(name, str):
            raise TypeError(f'{name} is not a string')

        if not isinstance(hand, Hand):
            raise TypeError(f'{hand} is not an instance of class Hand')

        if not isinstance(starting_position, int):
            raise TypeError(f'{starting_position} is not a integer')

        self.name = name
        self.hand = hand
        self.position = starting_position

    def __str__(self):
        return f'<Player name: {self.name}, position: {self.position}, {self.hand}>'

    def __repr__(self):
        return self.__str__()

    def set_position(self, new_position):
        if not isinstance(new_position, int):
            raise TypeError(f'{new_position} is not a integer')
        self.position = new_position

    def show_hand(self):
        print(self.hand)
