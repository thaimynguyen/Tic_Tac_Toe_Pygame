# tic_tac_toe.py is a 2-player tic-tac-toe game
# that works for different board size (3,3) or (5,5) etc

import numpy as np

BOARD_SIZE = (5, 5)

def print_board(board: np.ndarray):
    for i in board:
        for j in i:
            if j == 0:
                print('-', end=' ')
            elif j == 1:
                print('O', end=' ')
            elif j == -1:
                print('X', end=' ')
        print()

def print_player_turn(player: int):
    if player == 1:
        print("'O' turn:")
    elif player == -1:
        print("'X' turn:")

def is_cell_empty(board: np.ndarray, move: int):
    NUM_COL = np.shape(board)[1]
    if board[(move-1)//NUM_COL][(move%NUM_COL)-1] == 0:
        return True
    return False

def is_board_full(board: np.ndarray):
    for i in board:
        for j in i:
            if j == 0:
                return False
    return True

def check_winner(board: np.ndarray):
    NUM_COL = np.shape(board)[1]
    sum_cols = np.sum(board, axis=0)
    sum_rows = np.sum(board, axis=1)
    winner = None
    if NUM_COL in sum_cols or NUM_COL in sum_rows or sum(np.diagonal(board)) == NUM_COL or sum(np.rot90(board).diagonal()) == NUM_COL:
        winner = 'O'
    elif -NUM_COL in sum_cols or -NUM_COL in sum_rows or sum(np.diagonal(board)) == -NUM_COL or sum(np.rot90(board).diagonal()) == -NUM_COL:
        winner = 'X'
    return winner

def play_game(board: np.ndarray, player: int):
    NUM_COL = np.shape(board)[1]
    while not is_board_full(board):
        print_player_turn(player)
        move = input(f'Please enter a position from 1 to {BOARD_SIZE[0]*BOARD_SIZE[1]} or enter "q" to quit: \n')
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
    print_board(board)
    player = 1
    play_game(board, player)
    if is_board_full(board) and not check_winner(board):
        print("It's a tie!")

if __name__ == "__main__":
    main()
