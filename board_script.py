class Board():
    #Used to communicate UI interactions and game variables (player turn, score, board_size?, new game presets)
    def __init__(self):
        #self.board_size = BoardWidget.size?
        #self.current_player = 'Blue'
        #self.game_mode = SOSApp.mode_selected or something

    #def start_game()?
        #Reset Game,

    def update_score(self, points):
        self.scores[self.current_player] += points
        if self.game_mode == 'simple' and points > 0:
            self.game_over = True
        elif self.game_mode == 'general':
            # Check for game over condition in general mode
            pass
        
    def switch_player(self):
        self.current_player = 'Player 2' if self.current_player == 'Player 1' else 'Player 1'
    
    def reset_board():
        return
    def reset_score():
        return

    def announce_winner(player):
        pass
    def announce_draw():
        pass