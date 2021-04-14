from typing import List


class Blind(object):

    def __init__(self, big_blind_size: int = None, ante: int = 0):
        self.set_blinds(big_blind_size)
        self.ante = ante

    def __str__(self):
        return f'[ SB: {self.small_blind}, BB: {self.big_blind}, Rake: {self.rake} ]'

    def set_blinds(self, big_blind_size):
        self.small_blind = int(big_blind_size / 2)
        self.big_blind = big_blind_size

    def increase_blinds(self):
        self.small_blind = self.small_blind * self.increase_by
        self.big_blind = self.big_blind * self.increase_by


class BlindStructure:
    _STRUCTURE_TYPES = ['normal']

    def __init__(self, name: str = None, blinds: List[Blind] = None, starting_index: int = 0):
        self.blinds = blinds
        self.level_index = starting_index

    def __str__(self):
        current_level = self.current_level
        return f'Current blind: {self.current_level}\nNext blind: {self.next_level}\nAll blind levels: {[ str(blind) for blind in self.blind_levels]}'

    def increase_blind_level(self):
        next_level_index = self._get_next_level_index()
        self.level_index = next_level_index

    def _get_next_level_index(self):
        max_index = len(self.levels) - 1
        next_index = self.level_index + 1
        if next_index == max_index:
            return max_index
        return next_index

    @property
    def next_blind_level(self):
        next_blind_level = self._get_next_level_index()
        return next_blind_level

    @property
    def current_blind_level(self):
        return self.blinds[self.level_index]


blind_structures_data_set = {
    'normal': {
        'levels': [20, 30, 40, 50, 100, 150, 200, 250, 300, 400, 500, 600, 800, 1200, 1800, 2400, 3000, 4000, 5000, 8000, 12000, 16000, 20000, 25000, 30000, 35000, 40000, 50000, 60000, 70000, 80000, 100000, 150000, 200000, 300000, 400000, 600000, 1000000],
        'ante': {
            'start_index': 5,
            'procent_of_big_blind_size': 0.1
        }
    }
}
