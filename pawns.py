from abc import ABC

class Pawn(ABC):
    color = ""
    image = ""
    possibleMoves = []

    def move_n_attacks(self, row, column, board):
        moves = []
        enemies = []
        for move in self.possibleMoves:
            move_added = [row, column]
            move_added[0] += move[0]
            move_added[1] += move[1]
            if(move_added[0] >= 0 and move_added[0] <= 9 and move_added[1] >= 0 and move_added[1] <= 9):
                if(not board[move_added[0]][move_added[1]]):
                    moves.append(move_added)
                else:
                    move_next = [move_added[0], move_added[1]]
                    move_next[0] += move[0]
                    move_next[1] += move[1]
                    enemies.append([[move_added[0], move_added[1]], [move_next[0], move_next[1]]])
                    continue
            else:
                break
        return moves, enemies


class Queen(Pawn):
    possible_moves = [
        [-1, -1], [-1, 1],
        [1, -1], [1, 1]
        ]

    def move_n_attacks(self, row, column, board):
        moves = []
        enemies = []
        for move in self.possible_moves:
            enemy_found = False
            move_added = [row, column]
            for _ in range(9):
                move_added[0] += move[0]
                move_added[1] += move[1]
                if(move_added[0] >= 0 and move_added[0] <= 9 and move_added[1] >= 0 and move_added[1] <= 9):
                    if(not board[move_added[0]][move_added[1]] and not enemy_found):
                        moves.append([move_added[0], move_added[1]])
                    else:
                        enemy_found = True
                        move_next = [move_added[0], move_added[1]]
                        move_next[0] += move[0]
                        move_next[1] += move[1]
                        enemies.append([[move_added[0], move_added[1]], [move_next[0], move_next[1]]])
                        continue
                else:
                    break
        return moves, enemies

class White(Pawn):
    color = "white"
    image = 'img/pawnWhite.png'
    possibleMoves = [[-1, -1], [-1, 1]]

    def __init__(self):
        super().__init__()

class Black(Pawn):
    color = "black"
    image = 'img/pawnBlack.png'
    possibleMoves = [[1, -1], [1, 1]]

    def __init__(self):
        super().__init__()
