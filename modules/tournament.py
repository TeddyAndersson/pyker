import uuid
from dataclasses import dataclass
from .standard_deck import StandardDeck
from .poker_table import PokerTable, PokerTableConfig
from .blinds import BlindStructure


@dataclass
class Tournament:

    name: str
    blind_structure: BlindStructure
    table_size: int
    buy_in: float
    start_stack: int
    _id: str = uuid.uuid4()

    def get_table_config(self):
        return PokerTableConfig(size=self.table_size, tournament=self)


tournaments_data_set = {
    'after_work': {
        'name': 'After Work 12,5K GRT',
        'table_size': 9,
        'buy_in': 198,
        'start_stack': 3000,
        'blind_structure_type': 'normal'
    }


}
