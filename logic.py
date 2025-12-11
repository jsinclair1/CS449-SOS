from abc import ABC, abstractmethod

class SOSGame(ABC):
    #Parent class for Simple and General Game (both separate checkforSOS and gameOver function) 
    def __init__(self):
        self.scores = {'Red Player': 0, 'Blue Player': 0}
        self.total_moves = 0 
        self.counted_sos = set()

    
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
    

class SimpleGame(SOSGame):
    def __init__(self):
        super().__init__()
    
    def SOSFound(self, current_player):
       winner = current_player
       print(f"Game Over! {current_player.color} wins!")
       return winner
    
    def checkFullBoard(self,board):
        #If reached, the game is over
        if self.total_moves >= board.grid_size**2:
            return True
        return False


class GeneralGame(SOSGame):
    def __init__(self):
        super().__init__()

        #Assisted by ChatGPT
    def checkForSOS(self, board, board_size):
        new_scores = 0
        # Rows
        for row in range(board_size):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
                    key = tuple(sorted([(row, col), (row, col + 1), (row, col + 2)]))
                    if key not in self.counted_sos:
                        self.counted_sos.add(key)
                        new_scores += 1

        # Colums
        for col in range(board_size):
            for row in range(board_size - 2):
                if board[row][col] == 'S' and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
                    key = tuple(sorted([(row, col), (row + 1, col), (row + 2, col)]))
                    if key not in self.counted_sos:
                        self.counted_sos.add(key)
                        new_scores += 1

        #(top-left -->bottom-right)
        for row in range(board_size - 2):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row + 1][col + 1] == 'O' and board[row + 2][col + 2] == 'S':
                    key = tuple(sorted([
                        (row, col),
                        (row + 1, col + 1),
                        (row + 2, col + 2)
                    ]))
                    if key not in self.counted_sos:
                        self.counted_sos.add(key)
                        new_scores += 1

        # (bottom-left --> top-right)
        for row in range(2, board_size):
            for col in range(board_size - 2):
                if board[row][col] == 'S' and board[row - 1][col + 1] == 'O' and board[row - 2][col + 2] == 'S':
                    key = tuple(sorted([
                        (row, col),
                        (row - 1, col + 1),
                        (row - 2, col + 2)
                    ]))
                    if key not in self.counted_sos:
                        self.counted_sos.add(key)
                        new_scores += 1

        return new_scores

    def checkFullBoard(self,board):
        #If reached, the game is over
        if self.total_moves >= board.grid_size**2:
            winning_score = max(board.players[0].score, board.players[1].score)
            return winning_score
        return False
        
    def SOSFound(self, current_player):
        current_player.score += 1
        print(f'{current_player.color} score = {current_player.score}')
        


    
