from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from logic import SOSGame, SimpleGame, GeneralGame


class BoardWidget(Widget):
    #Handles grid functionality
    def __init__(self, game, app):
        super().__init__()
        self.grid_size = 0
        self.game = game
        self.app = app
        self.grid = []
        self.current_letter = 'S'  # Default letter
        self.current_player = 'Red'  # Default starting player
        self.bind(size=self.create_grid, pos=self.create_grid)

    def set_grid_size(self, n):
        self.grid_size = n
        self.grid = [['' for _ in range(n)] for _ in range(n)]
        

    def toggle_letter(self, letter):
        self.current_letter = letter

    def switch_player(self):
        self.current_player = 'Blue' if self.current_player == 'Red' else 'Red'
        self.turn_indicator.text = f"Current Turn: {self.current_player}"
        
    def create_grid(self, *args):
        self.canvas.clear()
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        with self.canvas:
            Color(1, 0, 0, 1)
            # Draw grid lines
            for i in range(1, self.grid_size):
                Line(points=[i * cell_w, 0, i * cell_w, h])
                Line(points=[0, i * cell_h, w, i * cell_h])
    
    def make_move(self, row, col):
        letter = self.grid[row][col]
        if letter:
            cell_w, cell_h = self.width / self.grid_size, self.height / self.grid_size
            label = CoreLabel(text=letter, font_size=min(cell_w, cell_h) * 0.7)
            label.refresh()
            texture = label.texture
            x = col * cell_w + (cell_w - texture.width) / 2
            y = row * cell_h + (cell_h - texture.height) / 2
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(texture=texture, pos=(x, y), size=texture.size)
            self.game.total_moves += 1
            self.check_game_status(self.game)


    def check_game_status(self, game):
        if self.game.checkForSOS(self.grid, self.grid_size):
            self.game.SOSFound(self)
            self.app.announce_win(self.current_player)
        elif self.game.checkFullBoard(self):
            self.app.announce_draw()
        else:
            self.switch_player()
            

    def on_touch_down(self, touch):
        if getattr(self, 'game_over', False):
            return
        if not self.collide_point(*touch.pos):
            return
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        col = int((touch.x - self.x) // cell_w)
        row = int((touch.y - self.y) // cell_h)

        #print(f"Touch at ({touch.x}, {touch.y}) maps to row {row}, col {col}")
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.grid[row][col] == '':
                self.grid[row][col] = self.current_letter
                self.make_move(row, col)



class SOSApp(App):
    #App Layout (buttons, scoreboard, turn indicator)
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        

        button_layout = BoxLayout(size_hint_y=None, height=50)
        # Board Size Input
        self.size_input_field = TextInput(hint_text='Enter board size', input_filter='int', multiline=False, height = 50, size_hint_y=None)
        button_layout.add_widget(self.size_input_field)
    
        # Simple Mode Button
        simple_mode = Button(text='Simple', size_hint_x=None, size_hint_y=None, height=100, width=150)
        simple_mode.bind(on_press=self.set_simple_game)
        button_layout.add_widget(simple_mode)

        # General Mode Button
        general_mode = Button(text='General', size_hint_x=None, size_hint_y=None, height=100, width=150)
        general_mode.bind(on_press=self.set_general_game)
        button_layout.add_widget(general_mode)
        
        #New Game Button
        new_game = Button(text='New Game', size_hint_x=None, size_hint_y=None, height=100, width=150)
        new_game.bind(on_press=self.start_game)
        button_layout.add_widget(new_game)
        self.layout.add_widget(button_layout)

        return self.layout

    def set_simple_game(self, _):
        self.game = SimpleGame()
        
    def set_general_game(self, _):
        self.game = GeneralGame()

    def start_game(self, _):
        #Check for existing board and remove it
        if hasattr(self, 'board') and self.board is not None:
            self.layout.remove_widget(self.board)
            self.board = None

        self.board = BoardWidget(self.game, app=self)
        try:
            n = int(self.size_input_field.text)
            if 3 <= n <= 10:
                self.board.set_grid_size(n)
                self.layout.add_widget(self.board)
                self.board.size_hint_y = 0.7
                #self.layout.remove_widget(self.size_input_field)
                self.add_letter_buttons(_)
                self.add_scoreboard(_)
            
        except ValueError:
            print("Invalid board size. Please enter an integer between 3 and 10.")
            return
        
    def add_letter_buttons(self,_):
        letter_layout = BoxLayout(size_hint_y=None, height=50)
        s_button = Button(text='S')
        o_button = Button(text='O')
        s_button.bind(on_press=lambda x: self.board.toggle_letter('S'))
        o_button.bind(on_press=lambda x: self.board.toggle_letter('O'))
        letter_layout.add_widget(s_button)
        letter_layout.add_widget(o_button)
        self.layout.add_widget(letter_layout)

    def add_scoreboard(self,_):
        info_layout = BoxLayout(size_hint_y=None, height=100, spacing=5)
        red_score = self.game.scores['Red Player']
        blue_score2 = self.game.scores['Blue Player']

        red_scoreboard = Label(text=f"Player 1 score: {red_score}", size_hint_y=None, height=50, font_size=24, color=(1,1,1,1), bold=True)
        blue_scoreboard = Label(text=f"Player 2 score: {blue_score2}", size_hint_y=None, height=50, font_size=24, color=(1,1,1,1), bold=True)
        
        info_layout.add_widget(red_scoreboard)
        info_layout.add_widget(blue_scoreboard)

        # Turn Indicator
        self.turn_indicator = Label(text=f"Current Turn: {self.board.current_player}", size_hint_y=None, height=50, font_size=24, color=(1,1,1,1), bold=True)
        info_layout.add_widget(self.turn_indicator)
        self.board.turn_indicator = self.turn_indicator
        self.layout.add_widget(info_layout)


    def announce_win(self, current_player):
        if hasattr(self, 'turn_indicator'):
            self.turn_indicator.text = f"Game Over! {current_player} wins!"
        if hasattr(self, 'board'):
            self.board.game_over = True
        return
    
    def announce_draw(self):
        if hasattr(self, 'turn_indicator'):
            self.turn_indicator.text = f"Game Over! It's a draw!"
        if hasattr(self, 'board'):
            self.board.game_over = True
        return

        

if __name__ == '__main__': 
    app = SOSApp()
    app.run()

