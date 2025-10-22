from app import SOSApp
from app import BoardWidget

class SOSGame:
    def __init__(self):
        self.current_player = 'Player 1'
        self.scores = {'Player 1': 0, 'Player 2': 0}
        self.game_over = False
        self.board = BoardWidget()
        #Get game mode from app
        self.game_mode = SOSApp().selected_mode
        

    def switch_player(self):
        self.current_player = 'Player 2' if self.current_player == 'Player 1' else 'Player 1'
    
    def update_score(self, points):
        self.scores[self.current_player] += points
        if self.game_mode == 'simple' and points > 0:
            self.game_over = True
        elif self.game_mode == 'general':
            # Check for game over condition in general mode
            pass
