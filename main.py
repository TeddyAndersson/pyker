import tkinter as tk
import math

from typing import Dict
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

from modules.helpers import create_rectangle_with_rounded_corners
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
        return self.players[player.id]

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
        self.configure(bg='#2A363B')

        self.game = game
        self.table = table
        self.main_frame = tk.Frame(self)
        self.canvas = tk.Canvas(
            self.main_frame, bg='#2A363B', bd=0, highlightthickness=0)
        self.images = {}
        self.seats = {}
        self.set_images()
        self.set_seats()
        self.setup_window()

    def set_seats(self):
        for i, seat in enumerate(self.table.seats):
            self.seats[seat.id] = {
                'card_images': [],
                'variables': {
                    'player_name_entry_value': tk.StringVar(''),
                },
                'elements': {

                }
            }

    def set_images(self):
        self.images['active_cardback_image'] = ImageTk.PhotoImage(
            file='assets/images/cardback_red.png')

        self.images['in_active_cardback_image'] = ImageTk.PhotoImage(
            file='assets/images/cardback_grey.png')

        self.images['cardback_overlay_image'] = ImageTk.PhotoImage(
            file='assets/images/cardback_overlay.png')

        self.images['table_background_image'] = ImageTk.PhotoImage(
            file='assets/images/pyker_bg.png')

    def setup_window(self):
        self.title(f'{self.table.tournament.name} - Table {self.table.id}')

        self.minsize(1200, 800)
        self.maxsize(1200, 1200)

        self.render_main_frame()
        self.render_canvas()
        self.render_background()
        self.render_nine_seats()

    def render_main_frame(self):
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def render_canvas(self):
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def render_background(self):
        self.canvas.create_image(
            600, 400, image=self.images['table_background_image'])
        self.canvas.update()

    def render_nine_seats(self):
        frist_card_coordinates_list = [(580, 550), (365, 530), (235, 390), (305, 225),
                                       (490, 185), (675, 185), (860, 225), (930, 390), (795, 530)]

        for i, seat_key in enumerate(self.seats.keys()):
            first_card_coordinates = frist_card_coordinates_list[i]
            first_card_x_coordinate, first_card_y_coordinate = first_card_coordinates
            second_cards_coordinates = (
                first_card_x_coordinate + 35, first_card_y_coordinate + 20)

            for coordinates in [first_card_coordinates, second_cards_coordinates]:
                image = self.images['cardback_overlay_image']
                if i == 0:
                    image = self.images['active_cardback_image']

                card_image = self.canvas.create_image(
                    *coordinates, image=image)
                self.seats[seat_key]['card_images'].append(card_image)

            rectangle_coordinates = (first_card_x_coordinate-55, first_card_y_coordinate + 40, first_card_x_coordinate + 95,
                                     first_card_y_coordinate + 80)

            create_rectangle_with_rounded_corners(
                self.canvas, *rectangle_coordinates, radius=10, fill="#ECECEC")

            text_coordinates = (first_card_x_coordinate + 15,
                                first_card_y_coordinate + 60)

            player_name_text = self.canvas.create_text(
                text_coordinates[0], text_coordinates[1], anchor=tk.CENTER)
            self.seats[seat_key]['elements']['player_name_text'] = player_name_text

            self.canvas.update()

            if not i == 0:
                entry_coordinates = (first_card_x_coordinate,
                                     first_card_y_coordinate + 60)
                player_name_entry = tk.Entry(
                    self.canvas, textvariable=self.seats[seat_key]['variables']['player_name_entry_value'], width=10, highlightbackground='#ECECEC')

                self.seats[seat_key]['elements']['player_name_entry'] = player_name_entry

                player_name_entry.bind(
                    "<Return>", (lambda event, seat_key=seat_key, command=self.handle_player_name_entry: command(event, seat_key)))

                player_name_entry.place(
                    x=entry_coordinates[0], y=entry_coordinates[1], anchor=tk.CENTER)

            else:
                self.seats[seat_key]['variables']['player_name_entry_value'].set(
                    'Hero')

            self.canvas.itemconfig(
                self.seats[seat_key]['elements']['player_name_text'], text=self.seats[seat_key]['variables']['player_name_entry_value'].get())

    def handle_player_name_entry(self, event, seat_key):
        player_name = self.seats[seat_key]['variables']['player_name_entry_value'].get(
        )

        if len(player_name) == 0:
            pass

        new_player = self.game.new_player(name=player_name, private=True)
        self.seats[seat_key]['elements']['player_name_entry'].destroy()

        self.canvas.itemconfig(
            self.seats[seat_key]['elements']['player_name_text'], text=new_player.name)

        self.master.after(
            1, (lambda seat_key=seat_key, func=self.set_active_cardbacks: func(seat_key)))

    def set_active_cardbacks(self, seat_key):
        for card_image in self.seats[seat_key]['card_images']:
            self.canvas.itemconfigure(
                card_image, image=self.images['active_cardback_image'])


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
