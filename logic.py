class SOSGame():
    #Parent class for Simple and General Game (both separate  checkforwinner and gameOver function) 
    def __init__(self):
        self.scores = {'Red Player': 0, 'Blue Player': 0}
        self.total_moves = 0 
        #self.game_over = False

    
    def checkFullBoard(self,board):
        print("Checking for full board...")
        #If reached, the game is over
        if self.total_moves >= board.grid_size * board.grid_size:
            return True
        return False

    

class SimpleGame(SOSGame):
    def __init__(self):
        super().__init__()

    def checkForSOS(self, board, board_size):
        print("Checking for SOS...")
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
    
    def SOSFound(self, current_player):
       #self.game_over = True
       winner = current_player
       print(f"Game Over! {winner} wins!")
       return winner


class GeneralGame(SOSGame):
    def __init__(self):
        super().__init__()
    
    def checkForSOS(self, board, board_size):
        #Needs to be modified to account for previous SOS found
        found_sos = [[]]
        print("Checking for SOS...")
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
    
    def SOSFound(self, board):
        self.board.current_player += 1
        #print(f"{current_player} found an SOS! Current Scores: {self.scores}")


    
