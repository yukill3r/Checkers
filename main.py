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
    white_amount = 10
    black_amount = 10

    def __init__(self):
        #self.upgrade_to_queen((0, 1))
        self.generate_squares()

    def upgrade_to_queen(self, position: (int, int)) -> Queen:
        pawn = self.positions[position[0]][position[1]]
        queen = Queen()
        queen.color = pawn.color
        queen.image = f"img/queen{pawn.color.capitalize()}"
        self.positions[position[0]][position[1]] = queen
        del pawn
        self.generate_squares()

    def generate_button(self, position):
        button = PySide6.QtWidgets.QPushButton()
        button.setFixedSize(*self.button_size)
        button.setIconSize(PySide6.QtCore.QSize(*self.icon_size))
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
        return button

    def generate_squares(self):
        for i in range(self.rows):
            for j in range(self.columns):
                button = self.generate_button((i, j))
                if (self.positions[i][j] != None):
                    button.clicked.connect(partial(self.selectPiece, (i, j)))
                self.grid.addWidget(button, i, j)

    def color_arena(self, piece, moves = [], attacks = [], jumps = []):
        def regen_button(grid, button, position):
            if not isinstance(grid.itemAtPosition(*position), NoneType):
                grid.removeWidget(grid.itemAtPosition(*position).widget())
                grid.addWidget(button, *position)

        def generate_move_color(grid, piece, move):
            if not self.positions[move[0]][move[1]]:
                button  = self.generate_button(move)
                button.setStyleSheet("background-color: green")
                button.clicked.connect(partial(self.move, piece, move, piece))
                regen_button(grid, button, move)

        def generate_attack_color(grid, attack):
            if(self.positions[attack[0]][attack[1]]):
                button  = self.generate_button(attack)
                button.setStyleSheet("background-color: red")
                regen_button(grid, button, attack)
        
        def generate_jumps_color(grid, piece, jump):
            if not self.positions[jump[0]][jump[1]]:
                button  = self.generate_button(jump)
                button.setStyleSheet("background-color: yellow")
                button.clicked.connect(partial(self.move, piece, jump, attack))
                regen_button(grid, button, jump)
    
        def generate_choosen_piece(grid, piece):
            button  = self.generate_button(piece)
            button.setStyleSheet("background-color: blue")
            button.clicked.connect(partial(self.selectPiece, piece))
            regen_button(grid, button, piece)

        NoneType = type(None)
        for move in moves:
            generate_move_color(self.grid, piece, move)

        for attack, jump in zip(attacks, jumps):
            generate_attack_color(self.grid, attack)
            generate_jumps_color(self.grid, piece, jump)
        
        generate_choosen_piece(self.grid, piece)
                    
    def selectPiece(self, position):
        self.generate_squares()
        if(self.positions[position[0]][position[1]]):
            if(self.positions[position[0]][position[1]].color == self.turn):
                attacks, jumps = self.positions[position[0]][position[1]].attack(
                    position[0], position[1], self.positions)
                moves = self.positions[position[0]][position[1]].move(
                    position[0], position[1],self.positions)
                if len(attacks) != 0:
                    moves = []
                self.color_arena([position[0], position[1]], moves, attacks, jumps)

    def move(self, current, next, target):
        self.positions[next[0]][next[1]] = self.positions[current[0]][current[1]]
        if current != target:
            if isinstance(self.positions[target[0]][target[1]], Black) and not self.positions[target[0]][target[1]] == None:
                self.black_amount -= 1
            elif isinstance(self.positions[target[0]][target[1]], White) and not self.positions[target[0]][target[1]] == None:
                self.white_amount -= 1
        self.positions[current[0]][current[1]] = None
        self.positions[target[0]][target[1]] = None
        
        if not isinstance(self.positions[next[0]][next[1]], Queen):
            if self.positions[next[0]][next[1]].color == "white" and next[0] == 0:
                self.upgrade_to_queen(next)
            elif self.positions[next[0]][next[1]].color == "black" and next[0] == self.rows-1:
                self.upgrade_to_queen(next)

        #print(self.grid.itemAtPosition(*target).widget())
        """
        attacks, jumps = self.positions[next[0]][next[1]].attack(
                    next[0], next[1], self.positions)
        if (len(attacks) != 0):
            self.selectPiece(next)
        """
        
        
        if self.white_amount == 0:
            self.ending("white")
        elif self.black_amount == 0:
            self.ending("black")

        else:
            if self.turn == "white":
                self.turn = "black"
            else:
                self.turn = "white"

            self.generate_squares()
            print(f"{self.turn} turn\nwhite: {self.white_amount}\nblack: {self.black_amount}")
    
    def ending(self, color):
        pass

if __name__ == "__main__":
    app = Window()
    app.win.show()
    exit(app.app.exec())