from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from logic import SOSGame, SimpleGame, GeneralGame
from player import Computer, Human
import random, time


class BoardWidget(Widget):
    #Handles grid functionality
    def __init__(self, game, app):
        super().__init__()
        self.grid_size = 0
        self.game = game
        self.app = app
        self.grid = []
        self.current_letter = 'S'  # Default letter
        self.players = [Human("Red"), Human("Blue")]
        self.bind(size=self.create_grid, pos=self.create_grid)

    def set_grid_size(self, n):
        self.grid_size = n
        self.grid = [['' for _ in range(n)] for _ in range(n)]
        
    def toggle_letter(self, letter):
        if self.current_letter in ['S', 'O']:
            self.current_letter = letter
        else:
            self.current_letter = 'S'
        

    def initialize_ai_opponent(self, color):
        for player in self.players:
            if player.color == color:
                self.players.remove(player)

        computer_opponent = Computer(color)
        self.players.append(computer_opponent)
        self.switch_player()
        print("CPU has joined")

    def switch_player(self):
        self.current_player = self.players[(self.game.total_moves + 1) % 2]
        turn_indicator = self.app.root.ids.turn_indicator
        turn_indicator.text = f"Current Turn: {self.current_player.color}"
        if isinstance(self.current_player, Computer):
            self.computer_move()


    def create_grid(self, *args):
        self.canvas.clear()
        if not self.grid_size:
            return
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        with self.canvas:
            Color(1, 0, 0, 1)
            # Vertical lines (including borders)
            for i in range(self.grid_size + 1):
                x = self.x + i * cell_w
                Line(points=[x, self.y, x, self.y + h])

            # Horizontal lines (including borders)
            for j in range(self.grid_size + 1):
                y = self.y + j * cell_h
                Line(points=[self.x, y, self.x + w, y])

    def make_move(self, row, col):
        location = (row,col)
        cell_w = self.width / self.grid_size
        cell_h = self.height / self.grid_size

        label = CoreLabel(text=self.current_letter, font_size=min(cell_w, cell_h) * 0.7)
        label.refresh()
        texture = label.texture

        # Column: left edge of the cell
        cell_left = self.x + col * cell_w

        # Row 0 = top, so convert to "row from bottom"
        row_from_bottom = self.grid_size - 1 - row
        cell_bottom = self.y + row_from_bottom * cell_h

        # Center the texture inside that cell
        x = cell_left + (cell_w - texture.width) / 2
        y = cell_bottom + (cell_h - texture.height) / 2

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(texture=texture, pos=(x, y), size=texture.size)

        self.game.total_moves += 1
        self.check_game_status(location)

    def check_game_status(self, last_move):
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
            return super().on_touch_down(touch)
        
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        
        col = int((touch.x - self.x) // cell_w)
        row_from_bottom = int((touch.y - self.y) // cell_h)
        row = self.grid_size - 1 - row_from_bottom

       
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.grid[row][col] == '':
                self.grid[row][col] = self.current_letter
                self.make_move(row, col)
    
    def computer_move(self):
        #next_move = calculate_move(self, self.grid)
        time.sleep(1)
        letters = ['S', 'O']
        while True:
            row = random.randrange(self.grid_size)
            col = random.randrange(self.grid_size)
            self.current_letter = letters[random.randrange(5) % 2]
            if self.grid[row][col] == '':
                self.grid[row][col] = self.current_letter
                self.make_move(row, col)
                break
        return
    

class RootWidget(BoxLayout):
    pass

class SOSApp(App):
    def build(self):
        root = RootWidget()
        self.layout = root
        self.size_input_field = root.ids.size_input_field
        self.board_container = root.ids.board_container
        self.bottom_layout = root.ids.bottom_layout
        return root
        
    def set_simple_game(self, *args):
        self.game = SimpleGame()
        
    def set_general_game(self, *args):
        self.game = GeneralGame()

    def start_game(self, *args):
        #Check for existing board and remove it
        if hasattr(self, 'board') and self.board is not None:
            self.board_container.remove_widget(self.board)
            self.board = None
            self.game.total_moves = 0

        self.board = BoardWidget(self.game, app=self)
        try:
            n = int(self.size_input_field.text)
        except ValueError:
            print("Invalid board size. Please enter an integer between 3 and 10.")
            return

        if not (3 <= n <= 10):
            print("Invalid board size. Please enter an integer between 3 and 10.")
            return

        self.board.set_grid_size(n)
        self.board.size_hint = (1, 1)
        self.board_container.add_widget(self.board)
        self.board.current_player = self.board.players[0]
        buttons = self.root.ids.bottom_layout
        buttons.disabled = False
        blue_cpu_selection = self.root.ids.blue_computer_button
        #blue_cpu_selection.disabled = True
        red_cpu_selection = self.root.ids.red_computer_button
        #red_cpu_selection.disabled = True
        turn_indicator = self.root.ids.turn_indicator
        turn_indicator.text = f"Current Turn: {self.board.current_player.color}"
        
    def announce_win(self, current_player):
        if hasattr(self, 'turn_indicator'):
            self.turn_indicator.text = f"Game Over! {self.board.current_player.color} wins!"
        if hasattr(self, 'board'):
            self.board.game_over = True
        return
    
    def announce_draw(self):
        if hasattr(self, 'turn_indicator'):
            self.turn_indicator.text = f"Game Over! It's a draw!"
        if hasattr(self, 'board'):
            self.board.game_over = True
        return
    
    def game_over():
        '''
        Reset all UI, move count, game settings, player settings
        '''
        pass

        

if __name__ == '__main__': 
    app = SOSApp()
    app.run()

