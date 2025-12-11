
class Player():
    #Will be parent class for human and robot player
    def __init__(self, color):
        self.color = color
        self.score = 0
        #{Move Number: (Row, Col)}
        self.moves = {}



class Human(Player):
    def __init__(self, color):
        super().__init__(color)

class Computer(Player):
    def __init__(self, color):
        super().__init__(color)

    def calculate_move(board):
        instructions = f'''
        The game board is a grid of n*n (n>2) squares. The two players take turns to add either an "S" or
    an "O" to an unoccupied square, with no requirement to use the same letter each turn. Each
    player competes to create a straight sequence S-O-S among connected squares (diagonally,
    horizontally, or vertically). 
    You are acting as a computer opponent: The n*n board is represented by an array of n arrays of n lengths. 
    This is the current game board represented in an array {board}. 

    It is your turn. Choose a position on the board (row, col) and letter ('S') or ('O') . 
    '''
        #(Row,col)
        position = ()
        return position
        