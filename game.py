def is_win(game):
    win = False
    # rows
    if game[0][0] == game[0][1] == game[0][2] and (game[0][0] == 'X' or game[0][0] == 'O'):
        win = True
    if game[1][0] == game[1][1] == game[1][2] and (game[1][0] == 'X' or game[1][0] == 'O'):
        win = True
    if game[2][0] == game[2][1] == game[2][2] and (game[2][0] == 'X' or game[2][0] == 'O'):
        win = True
    # columns
    if game[0][0] == game[1][0] == game[2][0] and (game[0][0] == 'X' or game[0][0] == 'O'):
        win = True
    if game[0][1] == game[1][1] == game[2][1] and (game[0][1] == 'X' or game[0][1] == 'O'):
        win = True
    if game[0][2] == game[1][2] == game[2][2] and (game[0][2] == 'X' or game[0][2] == 'O'):
        win = True
    # diagonals
    if game[0][0] == game[1][1] == game[2][2] and (game[0][0] == 'X' or game[0][0] == 'O'):
        win = True
    if game[0][2] == game[1][1] == game[2][0] and (game[0][2] == 'X' or game[0][2] == 'O'):
        win = True
    return win


def main():
    # Initialize the game board
    game = [[' ' for _ in range(3)] for _ in range(3)]
    player1 = 'X'
    player2 = 'O'
    turn = True  # False for player 1's turn, True for player 2's turn. Player 1 first.
    
    print("X = Player 1")
    print("O = Player 2")
    
    for n in range(9):
        turn = not turn  # Toggle turn
        
        if turn == False:
            print("Player 1: ", end="")
        else:
            print("Player 2: ", end="")
        
        print("Which cell to mark? i:[1..3], j:[1..3]: ", end="")
        i, j = map(int, input().split())
        
        if turn == False:
            game[i][j] = 'X'
        else:
            game[i][j] = 'O'
        
        if is_win(game):
            print("Win!")
            break
    
    if n == 8:  # All 9 cells have been filled (n goes 0 to 8)
        print("Tie!")
    
    # Show the game to console
    print(game[0][0] + " " + game[0][1] + " " + game[0][2])
    print(game[1][0] + " " + game[1][1] + " " + game[1][2])
    print(game[2][0] + " " + game[2][1] + " " + game[2][2])


if __name__ == "__main__":
    main()
