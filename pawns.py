from abc import ABC

class Pawn(ABC):
    """
    General class for pawns
    """
    color = ""
    image = ""
    possibleMoves = []

    def move_n_attacks(self, row, column, board):
        """
        Returns possible attacks and moves based on pawn position
        """
        moves = []
        enemies = []
        for move in self.possibleMoves:
            move_added = [row, column]
            move_added[0] += move[0]
            move_added[1] += move[1]
            if (move_added[0] >= 0 and
                    move_added[0] <= 9 and
                    move_added[1] >= 0 and
                    move_added[1] <= 9):
                if not board[move_added[0]][move_added[1]][0]:
                    moves.append(move_added)
                else:
                    if self.color != board[move_added[0]][move_added[1]][0].color:
                        move_next = [move_added[0], move_added[1]]
                        move_next[0] += move[0]
                        move_next[1] += move[1]
                        if (move_next[0] >= 0 and
                                move_next[0] <= 9 and
                                move_next[1] >= 0 and
                                move_next[1] <= 9):
                            if not board[move_next[0]][move_next[1]][0]:
                                enemies.append([[move_added[0], move_added[1]],
                                                [move_next[0], move_next[1]]])
                                continue
        return moves, enemies


class Queen(Pawn):
    """
    General class for queens upgraded from pawns
    """
    possible_moves = [
        [-1, -1], [-1, 1],
        [1, -1], [1, 1]
        ]

    def move_n_attacks(self, row, column, board):
        """
        Returns possible attacks and moves based on queen position
        """
        moves = []
        enemies = []
        for move in self.possible_moves:
            enemy_found = False
            move_added = [row, column]
            for _ in range(9):
                move_added[0] += move[0]
                move_added[1] += move[1]
                if(move_added[0] >= 0 and
                        move_added[0] <= 9 and
                        move_added[1] >= 0 and
                        move_added[1] <= 9):
                    if(not board[move_added[0]][move_added[1]][0] and not enemy_found):
                        moves.append([move_added[0], move_added[1]])
                    else:
                        if self.color != board[move_added[0]][move_added[1]][0].color:
                            enemy_found = True
                            move_next = [move_added[0], move_added[1]]
                            move_next[0] += move[0]
                            move_next[1] += move[1]
                            if(move_next[0] >= 0 and
                                    move_next[0] <= 9 and
                                    move_next[1] >= 0 and
                                    move_next[1] <= 9):
                                if not board[move_next[0]][move_next[1]][0]:
                                    enemies.append([[move_added[0], move_added[1]],
                                                    [move_next[0], move_next[1]]])
                                    break
                        break
        return moves, enemies

class White(Pawn):
    """
    Class with arguments for white pawn
    """
    color = "white"
    image = 'img/pawnWhite.png'
    possibleMoves = [[-1, -1], [-1, 1]]

    def __init__(self):
        super().__init__()

class Black(Pawn):
    """
    Class with arguments for black pawn
    """
    color = "black"
    image = 'img/pawnBlack.png'
    possibleMoves = [[1, -1], [1, 1]]

    def __init__(self):
        super().__init__()
