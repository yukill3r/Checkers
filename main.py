import sys
from functools import partial
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from default_ui import Ui_MainWindow
from pawns import White, Black, Queen, Pawn

class Main_Window(QMainWindow):
    """
    General gui management
    """
    positions = [
                [[None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey']],
                [[Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white']],
                [[None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey']],
                [[Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white'], [Black(), 'grey'], [None, 'white']],
                [[None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey']],
                [[None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white'], [None, 'grey'], [None, 'white']],
                [[None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey']],
                [[White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white']],
                [[None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey']],
                [[White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white'], [White(), 'grey'], [None, 'white']]
            ]
    rows = len(positions)
    columns = len(positions[0])
    turn = "white"
    base_name = "Warcaby"
    white_amount = 20
    black_amount = 20

    def generate_title(self):
        """
        Generate title based on variables
        self.base_name
        self.turn
        self.white_amount
        self.black_amount
        """
        self.setWindowTitle(f"{self.base_name} | {self.turn.capitalize()} | White: {self.white_amount} | Black: {self.black_amount}")

    def background_color(self, position, button):
        """
        Set buttons to default background colors
        """
        background_element = self.positions[position[0]][position[1]]
        button_type = None
        if isinstance(background_element[0], Queen):
            button_type = "queen"
        else:
            button_type = "pawn"

        if not button.styleSheet().replace("background-color: ", "") == background_element[1]:
            button.setStyleSheet("background-color: " + background_element[1])

        if background_element[0]:
            button.setIcon(self.cached_icons[button_type][background_element[0].color])
        else:
            button.setIcon(self.cached_icons["clean"])

    def basic_connector(self, position, button):
        """
        Set buttons connectors to default ones
        """
        background_element = self.positions[position[0]][position[1]]
        try:
            button.disconnect()
        except:
            pass
        if background_element[0] is not None:
            button.clicked.connect(partial(self.select_piece, position))

    def default_background_color_n_connectors(self):
        """
        Executor to assign default colors and connectors
        """
        for i in range(self.rows):
            for j in range(self.columns):
                button = self.ui.gridLayout.itemAtPosition(i, j).widget()
                self.background_color((i, j), button)
                self.basic_connector((i, j), button)

    def select_piece(self, position):
        """
        Select pawn on board, change visuals and connectors
        """
        if self.positions[position[0]][position[1]][0]:
            if self.positions[position[0]][position[1]][0].color == self.turn:
                self.default_background_color_n_connectors()
                button = self.ui.gridLayout.itemAtPosition(*position).widget()
                button.setStyleSheet("background-color: blue")
                button.disconnect()
                moves, enemies = self.positions[position[0]][position[1]][0].move_n_attacks(
                    position[0], position[1], self.positions)
                self.color_arena(button, position, moves, enemies)

    def color_arena(self, pawn, position, moves, enemies):
        """
        Color arena based on variables from select_piece
        """
        #if len(moves) == 0:
        #    return
        #elif len(enemies) == 0:
        #    return
        
        def generate_move_color(move_place, position, move):
            if not self.positions[move[0]][move[1]][0]:
                move_place.setStyleSheet("background-color: green")
                try:
                    move_place.disconnect()
                except:
                    pass
                move_place.clicked.connect(partial(self.move, position, move, position))

        def generate_attack_color(attack_place, attack):
            if self.positions[attack[0]][attack[1]][0] :
                attack_place.setStyleSheet("background-color: red")
                attack_place.disconnect()

        def generate_jumps_color(jump_place, position, jump, attack):
            if not self.positions[jump[0]][jump[1]][0]:
                jump_place.setStyleSheet("background-color: yellow")
                try:
                    jump_place.disconnect()
                except:
                    pass
                jump_place.clicked.connect(partial(self.move, position, jump, attack))

        NoneType = type(None)
        for move in moves:
            move_place = self.ui.gridLayout.itemAtPosition(*move).widget()
            generate_move_color(move_place, position, move)

        for attack, jump in enemies:
            attack_place = self.ui.gridLayout.itemAtPosition(*attack).widget()
            jump_place = self.ui.gridLayout.itemAtPosition(*jump).widget()
            generate_attack_color(attack_place, attack)
            generate_jumps_color(jump_place, position, jump, attack)

    def move(self, current, next_p, target):
        """
        Move target from current to next_p and remove target if attack
        """
        self.positions[next_p[0]][next_p[1]][0] = self.positions[current[0]][current[1]][0]
        if current != target:
            if (isinstance(self.positions[target[0]][target[1]][0], Black) and not
                    self.positions[target[0]][target[1]][0] is None):
                self.black_amount -= 1
            elif (isinstance(self.positions[target[0]][target[1]][0], White) and not
                    self.positions[target[0]][target[1]][0] is None):
                self.white_amount -= 1
        self.positions[current[0]][current[1]][0] = None
        self.positions[target[0]][target[1]][0] = None

        try:
            if (isinstance(self.positions[next_p[0]][next_p[1]][0], White) or
                    isinstance(self.positions[next_p[0]][next_p[1]][0], Black)):
                if not isinstance(self.positions[next_p[0]][next_p[1]][0], Queen):
                    if self.positions[next_p[0]][next_p[1]][0].color == "white" and next_p[0] == 0:
                        self.upgrade_to_queen(next_p)
                    elif (self.positions[next_p[0]][next_p[1]][0].color == "black" and
                            next_p[0] == self.rows-1):
                        self.upgrade_to_queen(next_p)
        except Exception as e:
            print(e)

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.generate_title()

        if not self.white_amount > 0:
            self.ending_win("black", "lightgrey")
        elif not self.black_amount > 0:
            self.ending_win("lightgrey", "black")
        self.default_background_color_n_connectors()

    def upgrade_to_queen(self, position):
        """
        Upgrade pawn to queen and remove old memory alloc
        """
        pawn = self.positions[position[0]][position[1]][0]
        queen = Queen()
        queen.color = pawn.color
        self.positions[position[0]][position[1]][0] = queen
        del pawn

    def ending_win(self, color_winner, color_loser):
        """
        Do not look cursed land below
        """
        for x in range(10):
            for z in [0, 1, 8, 9]:
                button = self.ui.gridLayout.itemAtPosition(x, z).widget()
                button.setStyleSheet(f"background-color: {color_winner}")
        for x in range(6,9,1):
            for z in [2, 7]:
                button = self.ui.gridLayout.itemAtPosition(x, z).widget()
                button.setStyleSheet(f"background-color: {color_winner}")
        for x in range(5,8,1):
            for z in [3, 6]:
                button = self.ui.gridLayout.itemAtPosition(x, z).widget()
                button.setStyleSheet(f"background-color: {color_winner}")
        for x in range(4,7,1):
            for z in [4, 5]:
                button = self.ui.gridLayout.itemAtPosition(x, z).widget()
                button.setStyleSheet(f"background-color: {color_winner}")
        for x in range(4):
            for y in range(2,8,1):
                button = self.ui.gridLayout.itemAtPosition(x, y).widget()
                button.setStyleSheet(f"background-color: {color_loser}")
        for x in range(2,8,1):
            button = self.ui.gridLayout.itemAtPosition(9, x).widget()
            button.setStyleSheet(f"background-color: {color_loser}")
        for x in range(3,7,1):
            button = self.ui.gridLayout.itemAtPosition(8, x).widget()
            button.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_4_2.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_4_3.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_4_6.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_4_7.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_5_2.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_5_7.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_7_4.setStyleSheet(f"background-color: {color_loser}")
        self.ui.b_7_5.setStyleSheet(f"background-color: {color_loser}")

    def __init__(self):
        super(Main_Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cached_icons = {
            "clean": QIcon(),
            "pawn": {"white": QIcon("img/pawnWhite.png"), "black": QIcon("img/pawnBlack.png")},
            "queen": {"white": QIcon("img/queenWhite.png"), "black": QIcon("img/queenBlack.png")}
            }
        self.generate_title()
        self.default_background_color_n_connectors()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())
