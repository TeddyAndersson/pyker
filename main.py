from typing import Dict
import tkinter as tk
import math

from PIL import Image, ImageTk

from modules import StandardDeck
from modules import PokerTable
from modules import HandEvaluator
from modules import Player
from modules import HandEvaluator
from modules import CardCollection
from modules import Blind
from modules import BlindStructure, blind_structures_data_set
from modules import Tournament, tournaments_data_set
from modules import PokerTable, PokerTableConfig

from modules.helpers import shift
from modules.helpers import select_action_input

tournaments_dict = {key: Tournament(name=tournaments_data_set[key]['name'], table_size=tournaments_data_set[key]['table_size'], blind_structure=tournaments_data_set[key]['blind_structure_type'],
                                    start_stack=tournaments_data_set[key]['start_stack'], buy_in=tournaments_data_set[key]['buy_in']) for key in tournaments_data_set}


def generate_tournaments_dict(blind_structures_dict):
    _dict = {}
    for key in tournaments_data_set:
        tournament = tournaments_data_set[key]
        name = tournament['name']
        start_stack = tournament['start_stack']
        table_size = tournament['table_size']
        buy_in = tournament['buy_in']
        blind_structure = blind_structures_dict[tournament['blind_structure_type']]
        _dict[key] = Tournament(name=name, start_stack=start_stack,
                                table_size=table_size, buy_in=buy_in, blind_structure=blind_structure)
    return _dict


def generate_blind_strucutres_dict():
    data_set = blind_structures_data_set
    _dict = {}

    for key in data_set:
        blinds = []
        blind_structure_data = data_set[key]
        blind_levels = blind_structure_data['levels']
        for index, level in enumerate(blind_levels):
            ante = 0
            ante_dict = blind_structure_data['ante']
            ante_start_index = ante_dict['start_index']
            ante_procent_of_big_blind_size = ante_dict['procent_of_big_blind_size']
            if index == ante_start_index:
                ante = level * ante_procent_of_big_blind_size
            blinds.append(Blind(big_blind_size=level, ante=ante))

        _dict[key] = BlindStructure(blinds=blinds)

    return _dict


class Game:

    def __init__(self, tournaments_dict: Dict[str, Tournament] = None, evaluator: HandEvaluator = None, blind_structure: BlindStructure = None):
        self.tournaments_dict = tournaments_dict
        self.evaluator = evaluator
        self.players = {}
        self.tables = {}

    def options(self):
        # handle game options
        pass

    def new_table(self, table_config: PokerTableConfig = None, PokerTable: PokerTable = None):
        table = PokerTable(config=table_config)
        self.tables[table.id] = table
        return self.tables[table.id]

    def new_player(self, name, private):
        player = Player(name=name, cards=CardCollection(), private=private)
        self.players[player.id] = player

    def start(self, table_id):
        self.new_hand(table)

    def new_hand(self):
        # go thorugh hand stages (pre-flop, flop, turn, river...)
        pass

    def new_betting_round(self):
        # let all players on a table take action (fold, check, raise...)
        pass

    def end_game(self):
        pass

    def post_blinds(self):
        pass

    def post_big_blind(self):
        pass

    def post_small_blind(self):
        pass


blind_structures_dict = generate_blind_strucutres_dict()
tournaments_dict = generate_tournaments_dict(blind_structures_dict)


class App:
    def __init__(self):
        self.__welcome()

    def __welcome(self):
        window = sg.Window(window_title="Test")


def pyker():
    evaluator = HandEvaluator()

    game = Game(tournaments_dict=tournaments_dict, evaluator=HandEvaluator())
    game.new_player(name='Mr. Andersson', private=False)
    for i in range(6):
        game.new_player(name=f'Evil guy {i+1}', private=True)

    # add player from players to table

    table = game.new_table()


class TableWindow(tk.Toplevel):
    def __init__(self, game, table):
        tk.Toplevel.__init__(self)
        self.game = game
        self.table = table
        self.setup_window()

    def setup_window(self):
        self.title(f'{self.table.tournament.name} - Table {self.table.id}')

        self.minsize(1200, 800)
        self.maxsize(1200, 1200)

        self.main_frame = tk.Frame(self, bg='#2A363B')
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.setup_canvas()
        # self.table_background()
        # self.place_cards()

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.main_frame)
        self.background_image = ImageTk.PhotoImage(file='pyker_bg.png')
        self.canvas.create_image(600, 400, image=self.background_image)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.place_players()

    def table_background(self):
        background_image = Image.open('pyker_bg.png')
        background_image = ImageTk.PhotoImage(background_image)
        background_image_label = tk.Label(self.canvas, image=background_image, bg='#2A363B')
        background_image_label.image = background_image
        background_image_label.place(relx=0, rely=0, relheight=1, relwidth=1)

        # canvas.create_arc(30, 200, 90, 100, start=0,
        #     extent=210, outline="#faceab", fill="#99B898", width=2)
        # points = [150, 100, 200, 120, 240, 180, 210,
        #     200, 150, 150, 100, 200]
        # canvas.create_polygon(points, outline='#faceab',
        #     fill='#99B898', width=2)

    def place_players(self):
        card1_coordinates = [(580,550),(365,530),(235,390),(305,225),(490,185),(675,185),(860,225),(930,390),(795,530)]
        card2_coordinates = [(coordinates[0]+35, coordinates[1]+20) for coordinates in card1_coordinates]
        label_coordinates = [(coordinates[0]-55, coordinates[1]+40, coordinates[0]+95, coordinates[1]+80) for coordinates in card1_coordinates]

        self.cardback_image = ImageTk.PhotoImage(file='cardback.png')
        for i, seat in enumerate(self.table.seats):
            self.canvas.create_image(*card1_coordinates[i], image=self.cardback_image)
            self.canvas.create_image(*card2_coordinates[i], image=self.cardback_image)
            round_rectangle(self.canvas, *label_coordinates[i], r=10, fill="#FFFFFF")
        self.canvas.update()

    def place_seats(self):
        origin_rel = 0.5
        radius = 0.3
        points = len(self.table.seats)
        pi = math.pi
        ang = 0 % 360

        for i, seat in enumerate(self.table.seats):
            print(i*40)
            seat_frame = tk.Frame(self.main_frame, bg='#FFF')
            rel_x = math.cos(i*40) * radius + origin_rel
            rel_y = math.sin(i*40) * radius + origin_rel
            print(rel_x, rel_y)
            seat_frame.place(relx=rel_x, rely=rel_y,
                             relheight=0.1, relwidth=0.1)

def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

class GameWindow:
    def __init__(self, master, game):
        self.game = game
        self.master = master
        self.setup()

    def setup(self):
        self.master.minsize(1200, 800)
        self.master.maxsize(1200, 800)

        self.canvas = tk.Canvas(self.master, height=800, width=1200)
        self.canvas.pack()

        self.main_frame = tk.Frame(self.master, bg='#2A363B')
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.tournament_option_menu()

    def new_table_window(self, tournament: Tournament):
        table_config = PokerTableConfig(
            size=tournament.table_size, deck=StandardDeck(), tournament=tournament)
        table = game.new_table(table_config=table_config,
                               PokerTable=PokerTable)
        self.app = TableWindow(game=game, table=table)

    def selected_tournament(self, event):
        tournament = next(self.game.tournaments_dict[key] for key in self.game.tournaments_dict.keys(
        ) if self.game.tournaments_dict[key].name == event)
        self.new_table_window(tournament)

    def tournament_option_menu(self):
        tournament_options = [
            self.game.tournaments_dict[key].name for key in self.game.tournaments_dict]
        drop_value = tk.StringVar()
        drop_value.set('Select Tournament')
        drop = tk.OptionMenu(self.main_frame, drop_value, *
                             tournament_options, command=self.selected_tournament)
        drop.pack()

if __name__ == "__main__":
    game = Game(tournaments_dict=tournaments_dict, evaluator=HandEvaluator())
    root = tk.Tk()
    my_gui = GameWindow(root, game)
    root.mainloop()
