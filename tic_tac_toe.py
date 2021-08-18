# tic_tac_toe.py is a 2-player tic-tac-toe game
# that works for different board size (3,3) or (5,5) etc

import numpy as np

BOARD_SIZE = (3, 3)

def print_board(board):
    for i in board:
        for j in i:
            if j == 0:
                print('-', end=' ')
            elif j == 1:
                print('O', end=' ')
            elif j == -1:
                print('X', end=' ')
        print()

def print_player_turn(player):
    if player == 1:
        print("'O' turn:")
    elif player == -1:
        print("'X' turn:")

def is_cell_empty(board, move: int):
    NUM_COL = np.shape(board)[1]
    if board[(move-1)//NUM_COL][(move%NUM_COL)-1] == 0:
        return True
    return False

def is_board_full(board):
    for i in board:
        for j in i:
            if j == 0:
                return False
    return True

def check_winner(board):
    NUM_COL = np.shape(board)[1]
    sum_cols = np.sum(board, axis=0)
    sum_rows = np.sum(board, axis=1)
    winner = None
    if NUM_COL in sum_cols or NUM_COL in sum_rows or sum(np.diagonal(board)) == NUM_COL or sum(np.rot90(board).diagonal()) == NUM_COL:
        winner = 'O'
    elif -NUM_COL in sum_cols or -NUM_COL in sum_rows or sum(np.diagonal(board)) == -NUM_COL or sum(np.rot90(board).diagonal()) == -NUM_COL:
        winner = 'X'
    return winner

def play_game(board, player):
    NUM_COL = np.shape(board)[1]
    print('O will play first.')
    while not is_board_full(board):
        move = input(f'Please enter a position 1 through 9 or enter "q" to quit: \n')
        if move == 'q':
            break
        try:
            move = int(move)
            if move in range(1, NUM_COL**2+1) and is_cell_empty(board, move):
                board[(move-1)//NUM_COL][(move%NUM_COL)-1] = player
                print_board(board)
                player *= -1
                winner = check_winner(board)
                if winner:
                    print(f'{winner} wins!')
                    break
                print_player_turn(player)
            elif move not in range(1, NUM_COL**2+1):
                print('Invalid Input')
            elif not is_cell_empty(board, move):
                print(f'Cell {move} has been taken. Please choose another cell!')
        except:
            print('Invalid Input')


"""
MAIN LOOP:
"""

def main():
    board = np.zeros(BOARD_SIZE)
    print(board)
    print_board(board)
    player = 1
    play_game(board, player)


if __name__ == "__main__":
    main()
