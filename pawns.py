from abc import ABC, abstractmethod

class Pawn(ABC):
    color = ""
    image = ""
    attacks = []
    jumps = []
    possibleAttacks = []
    jump_point = []
    possibleMoves = []

    @abstractmethod
    def attack(self, row, column, board):
        pass

    @abstractmethod
    def move(self, row, column, board):
        pass

class Queen(Pawn):
    def attack(self, row, column, board):
        attacks = []
        jumps = []
        possibleAttacks = [
            [row - 1, column - 1], [row - 1, column + 1],
            [row + 1, column - 1], [row + 1, column + 1]
        ]
        jump_point = [
            [row - 2, column - 2], [row - 2, column + 2],
            [row + 2, column - 2], [row + 2, column + 2]
        ]
        
        for attack, jump in zip(possibleAttacks, jump_point):
            if(attack[0] >= 0 and attack[0] <= len(board)-1 and attack[1] >= 0 and attack[1] <= len(board)-1):
                if (jump[0] >= 0 and jump[0] <= len(board)-1 and jump[1] >= 0 and jump[1] <= len(board)-1):
                    if(board[attack[0]][attack[1]] and not board[jump[0]][jump[1]]):
                        if(board[attack[0]][attack[1]].color != self.color):
                            attacks.append(attack)
                            jumps.append(jump)
        return attacks, jumps

    def move(self, row, column, board):
        moves = []
        possibleMoves = [
            [row - 1, column - 1], [row - 1, column + 1],
            [row + 1, column - 1], [row + 1, column + 1]
        ]
        corner_cancer = [
            [-1, -1], [-1, 1],
            [1, -1], [1, 1]
        ]

        move_cornored = [0, 0]
        for move, corner in zip(possibleMoves, corner_cancer):
            if(move[0] >= 0 and move[0] <= 9 and move[1] >= 0 and move[1] <= 9):        
                if (not board[move[0]][move[1]]):
                    moves.append(move)
            move_cornored[0] = move[0]
            move_cornored[1] = move[1]
            for _ in range(9):
                move_cornored[0] += corner[0]
                move_cornored[1] += corner[1]
                if(move_cornored[0] >= 0 and move_cornored[0] <= 9 and move_cornored[1] >= 0 and move_cornored[1] <= 9):
                    moves.append(move_cornored)
                    print(move_cornored)
            """
                    if (not board[move_cornored[0]][move_cornored[1]]):
            """
        print(moves)
        return moves

class White(Pawn):
    color = "white"
    image = 'img/pawnWhite.png'

    def __init__(self):
        super().__init__()

    def attack(self, row, column, board):
        attacks = []
        jumps = []
        possibleAttacks = [[row - 1, column - 1], [row - 1, column + 1] ]
        jump_point = [[row - 2, column - 2], [row - 2, column + 2]]
        
        for attack, jump in zip(possibleAttacks, jump_point):
            if(attack[0] >= 0 and attack[0] <= len(board)-1 and attack[1] >= 0 and attack[1] <= len(board)-1):
                if (jump[0] >= 0 and jump[0] <= len(board)-1 and jump[1] >= 0 and jump[1] <= len(board)-1):
                    if(board[attack[0]][attack[1]] and not board[jump[0]][jump[1]]):
                        if(board[attack[0]][attack[1]].color != self.color):
                            attacks.append(attack)
                            jumps.append(jump)
        return attacks, jumps

    def move(self, row, column, board):
        moves = []
        possibleMoves = [[row - 1, column - 1], [row - 1, column + 1]]
        
        for move in possibleMoves:
            if(move[0] >= 0 and move[0] <= 9 and move[1] >= 0 and move[1] <= 9):
                if(not board[move[0]][move[1]]):
                    moves.append(move)
        return moves

class Black(Pawn):
    color = "black"
    image = 'img/pawnBlack.png'

    def __init__(self):
        super().__init__()

    def attack(self, row, column, board):
        attacks = []
        jumps = []
        possibleAttacks = [[row + 1, column - 1], [row + 1, column + 1] ]
        jump_point = [[row + 2, column - 2], [row + 2, column + 2]]
        
        for attack, jump in zip(possibleAttacks, jump_point):
            if(attack[0] >= 0 and attack[0] <= len(board)-1 and attack[1] >= 0 and attack[1] <= len(board)-1):
                if (jump[0] >= 0 and jump[0] <= len(board)-1 and jump[1] >= 0 and jump[1] <= len(board)-1):
                    if(board[attack[0]][attack[1]] and not board[jump[0]][jump[1]]):
                        if(board[attack[0]][attack[1]].color != self.color):
                            attacks.append(attack)
                            jumps.append(jump)
        return attacks, jumps

    def move(self, row, column, board):
        moves = []
        possibleMoves = [[row + 1, column - 1], [row + 1, column + 1]]
        
        for move in possibleMoves:
            if(move[0] >= 0 and move[0] <= len(board)-1 and move[1] >= 0 and move[1] <= len(board)-1):
                if(not board[move[0]][move[1]]):
                    moves.append(move)
        return moves
