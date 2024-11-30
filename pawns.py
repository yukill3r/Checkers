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
            [row - 1, column - 1], [row - 1, column], [row - 1, column + 1],
            [row, column - 1], [row, column + 1],
            [row + 1, column - 1], [row + 1, column], [row + 1, column + 1]
        ]
        jump_point = [
            [row - 2, column - 2], [row - 2, column], [row - 2, column + 2],
            [row, column - 2], [row, column + 2],
            [row + 2, column - 2], [row + 2, column], [row + 2, column + 2]
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
            [row - 1, column], [row - 1, column - 1], [row - 1, column + 1],
            [row, column - 1], [row, column + 1],
            [row + 1, column], [row + 1, column - 1], [row + 1, column + 1]
        ]
        
        for move in possibleMoves:
            if(move[0] >= 0 and move[0] <= 9 and move[1] >= 0 and move[1] <= 9):
                if(not board[move[0]][move[1]]):
                    moves.append(move)
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
        possibleMoves = [[row - 1, column]]
        
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
        possibleMoves = [[row + 1, column]]
        
        for move in possibleMoves:
            if(move[0] >= 0 and move[0] <= len(board)-1 and move[1] >= 0 and move[1] <= len(board)-1):
                if(not board[move[0]][move[1]]):
                    moves.append(move)
        return moves
