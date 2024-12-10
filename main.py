import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream
from PyQt6.QtGui import QIcon
from functools import partial
from default_ui import Ui_MainWindow
from pawns import *

class Main_Window(QMainWindow):
    positions = [
                [None, Black(), None, Black(), None, Black(), None, Black(), None, Black()],
                [Black(), None, Black(), None, Black(), None, Black(), None, Black(), None],
                [None, Black(), None, Black(), None, Black(), None, Black(), None, Black()],
                [Black(), None, Black(), None, Black(), None, Black(), None, Black(), None],
                [None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None],
                [None, White(), None, White(), None, White(), None, White(), None, White()],
                [White(), None, White(), None, White(), None, White(), None, White(), None],
                [None, White(), None, White(), None, White(), None, White(), None, White()],
                [White(), None, White(), None, White(), None, White(), None, White(), None]
            ]
    rows = len(positions)
    columns = len(positions[0])
    turn = "white"
    base_name = "Warcaby"
    white_amount = 20
    black_amount = 20

    def generate_title(self):
        self.setWindowTitle(f"{self.base_name} | {self.turn.capitalize()} | White: {self.white_amount} | Black: {self.black_amount}")
        
    def background_color(self, position, button):
        first = "white"
        second = "grey"
        if(position[0] % 2 == 1):
            first = "grey"
            second = "white"
        if(position[1] % 2 == 0):
            button.setStyleSheet("background-color: " + first)
        else:
            button.setStyleSheet("background-color: " + second)

        if(self.positions[position[0]][position[1]]):
            button.setIcon(QIcon(self.positions[position[0]][position[1]].image))
        else:
            button.setIcon(QIcon())

    def basic_connector(self, position, button):
        try:
            button.disconnect()
        except:
            pass
        if (self.positions[position[0]][position[1]] != None):
            button.clicked.connect(partial(self.selectPiece, position))

    def default_background_color_n_connectors(self):
        for i in range(self.rows):
            for j in range(self.columns):
                button = self.ui.gridLayout.itemAtPosition(i, j).widget()
                self.background_color((i, j), button)
                self.basic_connector((i, j), button)
    
    def selectPiece(self, position):
        print(position)
        if(self.positions[position[0]][position[1]]):
            if(self.positions[position[0]][position[1]].color == self.turn):
                self.default_background_color_n_connectors()
                button = self.ui.gridLayout.itemAtPosition(*position).widget()
                button.setStyleSheet("background-color: blue")
                button.disconnect()
                moves, enemies = self.positions[position[0]][position[1]].move_n_attacks(
                    position[0], position[1], self.positions)
                self.color_arena(button, position, moves, enemies)

    def color_arena(self, pawn, position, moves = [], enemies = []):
        def generate_move_color(move_place, position, move):
            if not self.positions[move[0]][move[1]]:
                move_place.setStyleSheet("background-color: green")
                try:
                    move_place.disconnect()
                except:
                    pass
                move_place.clicked.connect(partial(self.move, position, move, position))

        def generate_attack_color(attack_place, attack):
            if(self.positions[attack[0]][attack[1]]):
                attack_place.setStyleSheet("background-color: red")
                attack_place.disconnect()
        
        def generate_jumps_color(jump_place, position, jump, attack):
            if not self.positions[jump[0]][jump[1]]:
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

    def move(self, current, next, target):
        self.positions[next[0]][next[1]] = self.positions[current[0]][current[1]]
        if current != target:
            if isinstance(self.positions[target[0]][target[1]], Black) and not self.positions[target[0]][target[1]] == None:
                self.black_amount -= 1
            elif isinstance(self.positions[target[0]][target[1]], White) and not self.positions[target[0]][target[1]] == None:
                self.white_amount -= 1
        self.positions[current[0]][current[1]] = None
        self.positions[target[0]][target[1]] = None
        
        try:
            if isinstance(self.positions[next[0]][next[1]], White) or isinstance(self.positions[next[0]][next[1]], Black):
                if not isinstance(self.positions[next[0]][next[1]], Queen):
                    if self.positions[next[0]][next[1]].color == "white" and next[0] == 0:
                        self.upgrade_to_queen(next)
                    elif self.positions[next[0]][next[1]].color == "black" and next[0] == self.rows-1:
                        self.upgrade_to_queen(next)
        except Exception as e:
            print(e)
        
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.generate_title()

        if not self.white_amount > 0:
            self.ending("Black")
        elif not self.black_amount > 0:
            self.ending("white")
        self.default_background_color_n_connectors()

    def upgrade_to_queen(self, position):
        pawn = self.positions[position[0]][position[1]]
        queen = Queen()
        queen.color = pawn.color
        queen.image = f"img/queen{pawn.color.capitalize()}"
        self.positions[position[0]][position[1]] = queen
        del pawn

    def ending_win(self, color_winner, color_loser):
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
        self.generate_title()
        self.default_background_color_n_connectors()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())