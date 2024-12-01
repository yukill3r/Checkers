import PySide6.QtWidgets
import PySide6.QtGui
import PySide6.QtCore
from functools import partial
import sys
from pawns import *

class Window():
    positions = [
                [None, Black(), None, Black(), None, Black(), None, Black(), None, Black()],
                [Black(), None, White(), None, Black(), None, Black(), None, Black(), None],
                [None, Black(), None, Black(), None, Black(), None, Black(), None, Black()],
                [Black(), None, Black(), None, Black(), None, Black(), None, Black(), None],
                [None, None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None, None],
                [None, White(), None, White(), None, White(), None, White(), None, White()],
                [White(), None, White(), None, White(), None, White(), None, White(), None],
                [None, Black(), None, White(), None, White(), None, White(), None, White()],
                [White(), None, White(), None, White(), None, White(), None, White(), None]
            ]
    rows = len(positions)
    columns = len(positions[0])
    button_size = (75, 75)
    icon_size = (50,50)

    app = PySide6.QtWidgets.QApplication(sys.argv)
    win = PySide6.QtWidgets.QWidget()
    grid = PySide6.QtWidgets.QGridLayout()
    win.setLayout(grid)
    win.setWindowTitle("Warcaby")
    win.setGeometry(0,0,820,640)
    turn = "white"
    multiple_attacks = False
    white_amount = 20
    black_amount = 20

    def __init__(self):
        self.generate_squares()

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
            button.setIcon(PySide6.QtGui.QIcon(self.positions[position[0]][position[1]].image))
        else:
            button.setIcon(PySide6.QtGui.QIcon())

    def basic_connector(self, position, button):
        button.disconnect(button)
        if (self.positions[position[0]][position[1]] != None):
            button.clicked.connect(partial(self.selectPiece, (position[0], position[1])))

    def generate_button(self, position):
        button = PySide6.QtWidgets.QPushButton()
        button.setFixedSize(*self.button_size)
        button.setIconSize(PySide6.QtCore.QSize(*self.icon_size))
        self.background_color(position, button)
        self.basic_connector(position, button)
        return button

    def generate_squares(self):
        for i in range(self.rows):
            for j in range(self.columns):
                button = self.generate_button((i, j))
                self.grid.addWidget(button, i, j)

    def default_background_color_n_connectors(self):
        for i in range(self.rows):
            for j in range(self.columns):
                button = self.grid.itemAtPosition(i, j).widget()
                self.background_color((i, j), button)
                self.basic_connector((i, j), button)

    def color_arena(self, pawn, position, moves = [], attacks = [], jumps = []):
        def generate_move_color(move_place, position, move):
            if not self.positions[move[0]][move[1]]:
                move_place.setStyleSheet("background-color: green")
                move_place.disconnect(move_place)
                move_place.clicked.connect(partial(self.move, position, move, position))

        def generate_attack_color(attack_place, attack):
            if(self.positions[attack[0]][attack[1]]):
                attack_place.setStyleSheet("background-color: red")
                attack_place.disconnect(attack_place)
        
        def generate_jumps_color(jump_place, position, jump, attack):
            if not self.positions[jump[0]][jump[1]]:
                jump_place.setStyleSheet("background-color: yellow")
                jump_place.disconnect(jump_place)
                jump_place.clicked.connect(partial(self.move, position, jump, attack))
    
        NoneType = type(None)
        for move in moves:
            move_place = self.grid.itemAtPosition(*move).widget()
            generate_move_color(move_place, position, move)

        for attack, jump in zip(attacks, jumps):
            attack_place = self.grid.itemAtPosition(*attack).widget()
            jump_place = self.grid.itemAtPosition(*jump).widget()
            generate_attack_color(attack_place, attack)
            generate_jumps_color(jump_place, position, jump, attack)
        
                   
    def selectPiece(self, position):
        if(self.positions[position[0]][position[1]]):
            if(self.positions[position[0]][position[1]].color == self.turn):
                self.default_background_color_n_connectors()
                button = self.grid.itemAtPosition(*position).widget()
                button.setStyleSheet("background-color: blue")
                button.disconnect(button)
                attacks, jumps = self.positions[position[0]][position[1]].attack(
                    position[0], position[1], self.positions)
                moves = self.positions[position[0]][position[1]].move(
                    position[0], position[1],self.positions)
                if len(attacks) != 0:
                    moves = []
                self.color_arena(button, position, moves, attacks, jumps)

    def upgrade_to_queen(self, position):
        pawn = self.positions[position[0]][position[1]]
        queen = Queen()
        queen.color = pawn.color
        queen.image = f"img/queen{pawn.color.capitalize()}"
        self.positions[position[0]][position[1]] = queen
        del pawn

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
        """
        if self.white_amount == 0:
            self.ending("white")
        elif self.black_amount == 0:
            self.ending("black")
        """
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.default_background_color_n_connectors()
        print(f"{self.turn} turn\nwhite: {self.white_amount}\nblack: {self.black_amount}")

if __name__ == "__main__":
    app = Window()
    app.win.show()
    exit(app.app.exec())