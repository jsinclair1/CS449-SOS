import unittest
from app import SOSApp, BoardWidget
from unittest.mock import patch, MagicMock
import random
import time

class FakeBoard:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        self.current_letter = None
        self.make_move = MagicMock()  # we'll assert on this

    def computer_move(self):
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
    
class TestComputerMove(unittest.TestCase):
    @patch('time.sleep', return_value=None)   # avoid 1-second pause
    @patch('random.randrange')
    def test_computer_move_places_letter_and_calls_make_move(self, mock_randrange, mock_sleep):
        board = FakeBoard(grid_size=3)

        # We want row=1, col=2, letter index=4 -> 'S'
        mock_randrange.side_effect = [1, 2, 4]

        board.computer_move()

        # Check grid was updated
        self.assertEqual(board.grid[1][2], 'S')
        self.assertEqual(board.current_letter, 'S')

        # Check make_move was called exactly once with (1, 2)
        board.make_move.assert_called_once_with(1, 2)

    @patch('time.sleep', return_value=None)
    @patch('random.randrange')
    def test_computer_move_skips_filled_cells(self, mock_randrange, mock_sleep):
        board = FakeBoard(grid_size=3)
        board.grid[0][0] = 'S'   # mark first pick as already occupied
        mock_randrange.side_effect = [0, 0, 1, 2, 1, 3]
        board.computer_move()

        # First cell unchanged
        self.assertEqual(board.grid[0][0], 'S')

        # Second chosen cell got the letter 'O'
        self.assertEqual(board.grid[2][1], 'O')
        self.assertEqual(board.current_letter, 'O')

        # make_move called exactly once with the successful cell
        board.make_move.assert_called_once_with(2, 1)
