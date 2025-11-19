from abc import ABC, abstractmethod

class SOSGame(ABC):
    #Parent class for Simple and General Game (both separate  checkforwinner and gameOver function) 
    def __init__(self):
        self.scores = {'Red Player': 0, 'Blue Player': 0}
        self.total_moves = 0 
        #self.game_over = False

    def checkFullBoard(self,board):
        #If reached, the game is over
        if self.total_moves >= board.grid_size * board.grid_size:
            return True
        return False
    
    def checkForSOS(self, board, board_size):
        # Check rows
        for row in range(board_size):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
                    return True
    
        # Check columns
        for col in range(board_size):
            for row in range(board_size - 2):
                if board[row][col] == 'S' and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
                    return True
                
        # Check diagonals (top-left to bottom-right)
        for row in range(board_size - 2):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row + 1][col + 1] == 'O' and board[row + 2][col + 2] == 'S':
                    return True
                
        # Check diagonals (bottom-left to top-right)
        for row in range(2, board_size):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row - 1][col + 1] == 'O' and board[row - 2][col + 2] == 'S':
                    return True
                
        return False
        '''
    def checkForSOS(self, grid, last_move):
        #size = board.size
        #last_move = row, col
        row,col = last_move

        
        from the move location, 
            if letter == S, 
                search 8 touching boxes for an O, 
                if O save direction, and go one more
            if letter == O:
                search 8 touching boxed for an S in direct opposite directions
        '''

class SimpleGame(SOSGame):
    def __init__(self):
        super().__init__()
    
    def SOSFound(self, current_player):
       #self.game_over = True
       winner = current_player
       print(f"Game Over! {winner} wins!")
       return winner


class GeneralGame(SOSGame):
    def __init__(self):
        super().__init__()
    
    def SOSFound(self):
        self.board.current_player += 1
        


    
