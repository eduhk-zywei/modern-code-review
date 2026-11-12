"""Tic-tac-toe (noughts and crosses) - version 2, corrected after the inspection.

Two players share one keyboard.  Player 1 is 'X' and always moves first,
Player 2 is 'O'.  A move is typed as "row column", both numbers in 1..3.
The program prints "Win!" as soon as a row, a column or a diagonal is
complete, or "Tie!" when all nine cells are full and nobody has won.

Run:  python3 tictactoe_v2.py
"""

EMPTY = " "
PLAYER_1 = "X"
PLAYER_2 = "O"

# F-07: the eight winning lines are data, not eight copied if-statements.
WIN_LINES = (
    ((0, 0), (0, 1), (0, 2)),  # row 0
    ((1, 0), (1, 1), (1, 2)),  # row 1
    ((2, 0), (2, 1), (2, 2)),  # row 2
    ((0, 0), (1, 0), (2, 0)),  # column 0
    ((0, 1), (1, 1), (2, 1)),  # column 1
    ((0, 2), (1, 2), (2, 2)),  # column 2
    ((0, 0), (1, 1), (2, 2)),  # main diagonal
    ((0, 2), (1, 1), (2, 0)),  # anti-diagonal
)


def is_win(board):
    """Return True if a row, a column or a diagonal has three equal marks."""
    for line in WIN_LINES:
        a, b, c = (board[r][c] for r, c in line)
        if a != EMPTY and a == b == c:
            return True
    return False


def read_move(board, prompt):
    """Read one legal move and return it as zero-based (row, column).

    Re-asks until the input is two whole numbers in 1..3 and the chosen
    cell is still empty.
    """
    while True:
        try:
            parts = input(prompt).split()
        except EOFError:  # F-04: Ctrl-D ends the session, it does not crash it.
            print("\nInput closed - stopping the game.")
            raise SystemExit(0)

        if len(parts) != 2:
            print("Please enter two integers, for example: 2 3")
            continue

        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            print("Row and column must be whole numbers.")
            continue

        # F-04: reject anything outside 1..3 before touching the board.
        if not (1 <= row <= 3 and 1 <= col <= 3):
            print("Row and column must be between 1 and 3.")
            continue

        # F-01: humans count 1..3, Python lists count 0..2.
        row, col = row - 1, col - 1

        # F-03: a marked cell may not be played again.
        if board[row][col] != EMPTY:
            print("That cell is already taken. Choose another one.")
            continue

        return row, col


def print_board(board):
    """Print the 3x3 board, one row per line."""  # F-10
    for row in board:
        print(" ".join(row))


def main():
    # F-11: the module docstring states the coordinate convention.
    board = [[EMPTY] * 3 for _ in range(3)]

    print("X = Player 1")
    print("O = Player 2")

    for move in range(9):
        # F-09: no "turn == False"; the player follows from the move number.
        if move % 2 == 0:
            mark, player = PLAYER_1, "Player 1"
        else:
            mark, player = PLAYER_2, "Player 2"

        # F-08: no unused player1 / player2 variables are left behind.
        row, col = read_move(board, f"{player} ({mark}) - row col [1..3]: ")
        board[row][col] = mark

        if is_win(board):
            print("Win!")  # the message required by the specification
            print(f"{player} ({mark}) wins.")  # F-10: and who won
            print_board(board)
            return

    # F-02: only reached when all nine moves were played without a win.
    # F-05: nothing depends on the loop variable after the loop.
    print("Tie!")
    print_board(board)


if __name__ == "__main__":
    main()
