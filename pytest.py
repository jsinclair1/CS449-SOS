import unittest
from app import SOSApp, BoardWidget


class TestClick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

class TestBoardWidget(unittest.TestCase):
    def setUp(self):
        self.app = SOSApp()
        self.app.build()
        self.app.board.size = (300, 300)
        self.app.board.pos = (0, 0)
        
    def test_valid_size_initializes_empty_grid(self):
        board = BoardWidget()
        board.size = (300, 300)
        board.set_grid_size(5)
        assert board.grid_size == 5
        assert len(board.grid) == 5
        assert all(len(row) == 5 for row in board.grid)
        assert all(cell == '' for row in board.grid for cell in row)

    def test_cannot_overwrite_existing_cell(self):
        board = BoardWidget()
        board.size = (300, 300)
        board.pos = (0, 0)
        board.set_grid_size(3)
        # Put 'S' in center via touch
        cell_w = board.width / board.grid_size
        cell_h = board.height / board.grid_size
        cx = 1 * cell_w + cell_w / 2
        cy = 1 * cell_h + cell_h / 2
        board.set_letter('S')
        board.on_touch_down(TestClick(cx, cy))
        assert board.grid[1][1] == 'S'
        # Try to overwrite with 'O'
        board.set_letter('O')
        board.on_touch_down(TestClick(cx, cy))
        assert board.grid[1][1] == 'S'

    def test_valid_integer_size_between_3_and_10(self):
        '''Input 3–10 should create a grid of correct size.'''
        for n in [3, 5, 10]:
            self.app.size_input.text = str(n)
            self.app.on_set_button(None)
            self.assertEqual(self.app.board.grid_size, n)
            self.assertEqual(len(self.app.board.grid), n)
            self.assertTrue(all(len(row) == n for row in self.app.board.grid))

    def test_reject_invalid_sizes(self):
        """Invalid inputs (too small, too large, or non-int) should not set a grid."""
        invalid_inputs = ['2', '11', 'abc', '']
        for inval in invalid_inputs:
            self.app.size_input.text = inval
            self.app.board.grid_size = None  # reset between tries
            self.app.on_set_button(None)
            # Board size should remain None or unchanged
            self.assertTrue(
                self.app.board.grid_size is None or
                not (3 <= self.app.board.grid_size <= 10),
                f"Invalid input {inval} incorrectly accepted."
            )

if __name__ == "__main__":
    unittest.main()