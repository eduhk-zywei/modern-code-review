"""Tests for ../src/tictactoe_v2.py.

Run from lecture10-code-inspection/:
    python3 -m unittest discover -s tests -v

The tests use only the standard library, so no pip install is needed.
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from tictactoe_v2 import is_win, main, read_move  # noqa: E402


def board(rows):
    """Build a 3x3 board from three strings such as 'XOX'."""
    return [list(row) for row in rows]


def run_game(moves):
    """Run main() with scripted answers; return everything it printed."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=moves), redirect_stdout(output):
        main()
    return output.getvalue()


def board_lines(output):
    """The last three printed lines are the final board; return them rstripped."""
    return [line.rstrip() for line in output.splitlines()[-3:]]


class TestIsWin(unittest.TestCase):
    def test_empty_board_has_no_winner(self):
        self.assertFalse(is_win(board(["   ", "   ", "   "])))

    def test_top_row_wins(self):
        self.assertTrue(is_win(board(["XXX", "OO ", "   "])))

    def test_middle_row_wins(self):
        self.assertTrue(is_win(board(["X  ", "OOO", "  X"])))

    def test_bottom_row_wins(self):
        self.assertTrue(is_win(board(["O X", "X O", "XXX"])))

    def test_left_column_wins(self):
        self.assertTrue(is_win(board(["X O", "X O", "X  "])))

    def test_middle_column_wins(self):
        self.assertTrue(is_win(board(["O X", "  X", "O X"])))

    def test_right_column_wins(self):
        self.assertTrue(is_win(board(["X O", "  O", "X O"])))

    def test_main_diagonal_wins(self):
        self.assertTrue(is_win(board(["X O", " X ", "O X"])))

    def test_anti_diagonal_wins(self):
        self.assertTrue(is_win(board(["X O", " O ", "O X"])))

    def test_two_in_a_row_is_not_a_win(self):
        self.assertFalse(is_win(board(["XX ", "O  ", "  O"])))

    def test_full_board_without_a_line_is_not_a_win(self):
        self.assertFalse(is_win(board(["XOX", "XOO", "OXX"])))


class TestMain(unittest.TestCase):
    def test_player_1_wins_on_move_five(self):
        # X takes the main diagonal: (1,1), (2,2), (3,3).
        output = run_game(["1 1", "1 2", "2 2", "2 3", "3 3"])
        self.assertIn("Win!", output)
        self.assertIn("Player 1 (X) wins.", output)
        self.assertNotIn("Tie!", output)

    def test_win_on_the_last_move_does_not_also_print_tie(self):
        # X completes row 2 on the 9th move; v1 printed Win! and Tie! (F-02).
        output = run_game(
            ["2 1", "1 1", "2 2", "3 1", "1 3", "1 2", "3 3", "3 2", "2 3"]
        )
        self.assertIn("Win!", output)
        self.assertNotIn("Tie!", output)

    def test_full_board_without_a_winner_prints_tie(self):
        output = run_game(
            ["1 1", "1 2", "1 3", "2 2", "2 1", "2 3", "3 2", "3 1", "3 3"]
        )
        self.assertIn("Tie!", output)
        self.assertNotIn("Win!", output)

    def test_one_based_coordinates_reach_the_expected_cell(self):
        # "1 1" must mean the top-left cell; v1 marked the centre (F-01).
        game = [[" "] * 3 for _ in range(3)]
        with patch("builtins.input", return_value="1 1"):
            self.assertEqual(read_move(game, ""), (0, 0))

    def test_coordinates_are_not_used_as_raw_indices(self):
        # v1 used "3 3" as a list index and raised IndexError (F-01 / F-04).
        game = [[" "] * 3 for _ in range(3)]
        with patch("builtins.input", return_value="3 3"):
            self.assertEqual(read_move(game, ""), (2, 2))

    def test_corner_three_three_is_a_legal_move(self):
        # v1 raised IndexError for "3 3" (F-04).
        output = run_game(["3 3", "1 1", "3 1", "1 2", "3 2"])
        self.assertIn("Win!", output)
        self.assertNotIn("Traceback", output)

    def test_bad_input_is_rejected_then_accepted(self):
        output = run_game(
            ["a b", "1 2 3", "4 4", "1 1", "1 2", "2 2", "2 3", "3 3"]
        )
        self.assertIn("two integers", output)
        self.assertIn("between 1 and 3", output)
        self.assertIn("whole numbers", output)
        self.assertIn("Win!", output)

    def test_occupied_cell_is_rejected(self):
        # Player 2 tries to take (1,1) from Player 1, then plays (1,2).
        output = run_game(["1 1", "1 1", "1 2", "2 2", "2 3", "3 3"])
        self.assertIn("already taken", output)
        self.assertIn("Win!", output)
        # (1,1) must still be X, not overwritten by O.
        self.assertEqual(board_lines(output)[0], "X O")

    def test_negative_numbers_are_rejected(self):
        # -1 would silently mean "last row" in Python if unchecked (F-04).
        output = run_game(["-1 -1", "1 1", "1 2", "2 2", "2 3", "3 3"])
        self.assertIn("between 1 and 3", output)
        self.assertIn("Win!", output)

    def test_end_of_input_stops_the_game_without_a_traceback(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), redirect_stdout(output):
            with self.assertRaises(SystemExit):
                main()
        self.assertIn("Input closed", output.getvalue())


if __name__ == "__main__":
    unittest.main()
