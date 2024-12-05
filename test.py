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
    white_amount = 20
    black_amount = 20

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
        """
                moves, enemies = self.positions[position[0]][position[1]].move_n_attacks(
                    position[0], position[1], self.positions)
                self.color_arena(button, position, moves, enemies)
        """
                
    def __init__(self):
        super(Main_Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.default_background_color_n_connectors()
            




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())