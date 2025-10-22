from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label


class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = None
        self.grid = []
        self.current_letter = 'S'
        self.bind(size=self.redraw, pos=self.redraw)

    def set_grid_size(self, n):
        self.grid_size = n
        self.grid = [['' for _ in range(n)] for _ in range(n)]
        self.redraw()

    def set_letter(self, letter):
        self.current_letter = letter

    def on_touch_down(self, touch):
        if self.grid_size is None:
            return
        if not self.collide_point(*touch.pos):
            return
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        col = int((touch.x - self.x) // cell_w)
        row = int((touch.y - self.y) // cell_h)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.grid[row][col] == '':
                self.grid[row][col] = self.current_letter
                self.redraw()
                #Switch player after a successful move

    def redraw(self, *args):
        self.canvas.clear()
        if self.grid_size is None:
            return
        w, h = self.width, self.height
        cell_w, cell_h = w / self.grid_size, h / self.grid_size
        with self.canvas:
            Color(1, 0, 0, 1)
            # Draw grid lines
            for i in range(1, self.grid_size):
                Line(points=[i * cell_w, 0, i * cell_w, h])
                Line(points=[0, i * cell_h, w, i * cell_h])
            # Draw letters
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    letter = self.grid[row][col]
                    if letter:
                        label = CoreLabel(text=letter, font_size=min(cell_w, cell_h) * 0.7)
                        label.refresh()
                        texture = label.texture
                        x = col * cell_w + (cell_w - texture.width) / 2
                        y = row * cell_h + (cell_h - texture.height) / 2
                        Rectangle(texture=texture, pos=(x, y), size=texture.size)

class SOSApp(App):
    def build(self):
        self.grid_size = None  # Don't draw grid until user input
        self.selected_mode = None
        self.root = BoxLayout(orientation='vertical')
        self.input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        self.size_input = TextInput(hint_text='Enter board size', input_filter='int', multiline=False)
        self.input_box.add_widget(self.size_input)

        # Game Mode Buttons
        self.simple_mode = Button(text='Simple', size_hint_x=None, size_hint_y=None, height=100, width=150)
        self.general_mode = Button(text='General', size_hint_x=None, size_hint_y=None, height=100, width=150)
        self.input_box.add_widget(self.simple_mode)
        self.input_box.add_widget(self.general_mode)

        # Set button
        self.set_button = Button(text='New Game', size_hint_x=None, size_hint_y=None, height=100, width=100)
        self.input_box.add_widget(self.set_button)

        # Letter selection
        self.letterS_input = Button(text='S', size_hint_x=None, size_hint_y=None, height=100, width=150)
        self.letterO_input = Button(text='O', size_hint_x=None, size_hint_y=None, height=100, width=150)
        self.input_box.add_widget(self.letterS_input)
        self.input_box.add_widget(self.letterO_input)
        # Bind the actual letter buttons and ignore the unused event parameter with _
        self.letterS_input.bind(on_press=lambda _=None: self.board.set_letter('S'))
        self.letterO_input.bind(on_press=lambda _=None: self.board.set_letter('O'))

        # Board widget
        self.board = BoardWidget(size_hint_y=1, height=400)
        self.root.add_widget(self.input_box)
        self.root.add_widget(self.board)

        # Game mode indicator (visible with default text)
        self.game_mode_label = Label(text="Game Mode: None", size_hint_y=None, height=50, font_size=24, color=(1,1,1,1), bold=True)
        self.root.add_widget(self.game_mode_label)

        # Bindings
        self.simple_mode.bind(on_press=self.on_mode_selected)
        self.general_mode.bind(on_press=self.on_mode_selected)
        self.set_button.bind(on_press=self.on_set_button)

        return self.root


        # When a game mode is selected (after a valid board size was set), remove the input widgets
    def on_mode_selected(self, instance):
        if self.board.grid_size is None:
            return
        self.selected_mode = instance.text
        # Show selected game mode below the grid
        self.game_mode_label.text = f"Game Mode: {self.selected_mode}"


    def on_set_button(self, instance):
        try:
            n = int(self.size_input.text)
            if 3 <= n <= 10:
                self.board.set_grid_size(n)
                # Remove only size input and new game button; keep mode buttons until user selects one
                for w in (self.size_input, self.set_button):
                    if w in self.input_box.children:
                        self.input_box.remove_widget(w)
                # Update label to reflect current state if mode not chosen yet
                if not self.selected_mode:
                    self.game_mode_label.text = "Game Mode: (select above)"
                else:
                    self.game_mode_label.text = f"Game Mode: {self.selected_mode}"
        except ValueError:
            pass


if __name__ == '__main__': 
    app = SOSApp()
    app.run()
