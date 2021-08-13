import pygame
import numpy as np

pygame.init()

"""
CONSTANTS:
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
NUM_COL = 3
NUM_ROW = NUM_COL
SQUARE_SIDE = SCREEN_WIDTH // NUM_COL

BORDER_WIDTH = 10
LINE_WIDTH = 5
CIRCLE_RADIUS = SQUARE_SIDE//3

font = pygame.font.SysFont('comicsans', SCREEN_WIDTH//5)

# Define colours using RGB:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up Pygame window:
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

"""
FUNCTIONS:
"""

# background color
SCREEN.fill(WHITE)

def draw_grid():

    for x in range(1, NUM_COL):
        # vertical borders
        pygame.draw.line(SCREEN, BLACK, (SCREEN_WIDTH//NUM_COL*x - BORDER_WIDTH//2, 0),
                         (SCREEN_WIDTH//NUM_COL*x - BORDER_WIDTH//2, SCREEN_WIDTH), BORDER_WIDTH)
        # horizontal borders
        pygame.draw.line(SCREEN, BLACK, (0, SCREEN_HEIGHT//NUM_ROW*x - BORDER_WIDTH//2),
                         (SCREEN_HEIGHT, SCREEN_HEIGHT//NUM_ROW*x - BORDER_WIDTH//2), BORDER_WIDTH)
    pygame.display.update()


def draw_board(num_col, num_row):
    board = []
    for col in range(0, num_col):
        for row in range(0, num_row):
            board[col][row] = 0
    return board


def draw_figures(player, x_index, y_index):
    if player == 1:
        pygame.draw.circle(SCREEN, BLUE, (SQUARE_SIDE//2 + x_index*SQUARE_SIDE,
                                                  SQUARE_SIDE//2 + y_index*SQUARE_SIDE), CIRCLE_RADIUS, LINE_WIDTH)
    if player == -1:
        pygame.draw.line(SCREEN, RED, (SQUARE_SIDE//5 + x_index*SQUARE_SIDE, SQUARE_SIDE//5 + y_index*SQUARE_SIDE),
                         ((x_index+1)*SQUARE_SIDE-SQUARE_SIDE//5, (y_index+1)*SQUARE_SIDE-SQUARE_SIDE//5), LINE_WIDTH)
        pygame.draw.line(SCREEN, RED, ((x_index+1)*SQUARE_SIDE - SQUARE_SIDE//5, SQUARE_SIDE//5 + y_index *
                                               SQUARE_SIDE), (SQUARE_SIDE//5 + x_index*SQUARE_SIDE, (y_index+1)*SQUARE_SIDE-SQUARE_SIDE//5), LINE_WIDTH)
    
def check_winner(board):
    sum_cols = np.sum(board, axis=0)
    sum_rows = np.sum(board, axis=1)

    winning_col = None
    winning_row = None
    
    winner = None

    # check & draw vertical winning line
    if NUM_COL in sum_cols:
        winning_col = int(list(np.where(sum_cols == NUM_COL))[0])
        pygame.draw.line(SCREEN, BLUE, (SQUARE_SIDE//2 + winning_col*SQUARE_SIDE, 0),
                         (SQUARE_SIDE//2 + winning_col*SQUARE_SIDE, SCREEN_HEIGHT), LINE_WIDTH)
        winner = 'O'
    elif -NUM_COL in sum_cols:
        winning_col = int(list(np.where(sum_cols == -NUM_COL))[0])
        pygame.draw.line(SCREEN, RED, (SQUARE_SIDE//2 + winning_col*SQUARE_SIDE, 0),
                         (SQUARE_SIDE//2 + winning_col*SQUARE_SIDE, SCREEN_HEIGHT), LINE_WIDTH)
        winner = 'X'

    # check & draw horizontal winning line
    elif NUM_COL in sum_rows:
        winning_row = int(list(np.where(sum_rows == NUM_COL))[0])
        pygame.draw.line(SCREEN, BLUE, (0, SQUARE_SIDE//2 + winning_row*SQUARE_SIDE),
                         (SCREEN_WIDTH, SQUARE_SIDE//2 + winning_row*SQUARE_SIDE), LINE_WIDTH)
        winner = 'O'
    elif -NUM_COL in sum_rows:
        winning_row = int(list(np.where(sum_rows == -NUM_COL))[0])
        pygame.draw.line(SCREEN, RED, (0, SQUARE_SIDE//2 + winning_row*SQUARE_SIDE),
                         (SCREEN_WIDTH, SQUARE_SIDE//2 + winning_row*SQUARE_SIDE), LINE_WIDTH)
        winner = 'X'

    # check & draw diagonal winning lines:
    elif sum(np.diagonal(board)) == NUM_COL:
        pygame.draw.line(SCREEN, BLUE, (SQUARE_SIDE//5, SQUARE_SIDE//5),
                         (SCREEN_WIDTH-SQUARE_SIDE//5, SCREEN_WIDTH-SQUARE_SIDE//5), LINE_WIDTH)
        winner = 'O'
    elif sum(np.diagonal(board)) == -NUM_COL:
        pygame.draw.line(SCREEN, RED, (SQUARE_SIDE//5, SQUARE_SIDE//5),
                         (SCREEN_WIDTH-SQUARE_SIDE//5, SCREEN_WIDTH-SQUARE_SIDE//5), LINE_WIDTH)
        winner = 'X'
    elif sum(np.rot90(board).diagonal()) == NUM_COL:
        pygame.draw.line(SCREEN, BLUE, (SCREEN_WIDTH-SQUARE_SIDE//5,
                                                SQUARE_SIDE//5), (SQUARE_SIDE//5, SCREEN_WIDTH-SQUARE_SIDE//5), LINE_WIDTH)
        winner = 'O'
    elif sum(np.rot90(board).diagonal()) == -NUM_COL:
        pygame.draw.line(SCREEN, RED, (SCREEN_WIDTH-SQUARE_SIDE//5,
                                               SQUARE_SIDE//5), (SQUARE_SIDE//5, SCREEN_WIDTH-SQUARE_SIDE//5), LINE_WIDTH)
        winner = 'X'

    return winner


def check_board_full(board):
    for row in range(NUM_ROW):
        for col in range(NUM_COL):
            if board[row][col] == 0:
                return False
    return True

def display_winner(winner):
    if winner != None:
        result = winner + ' WON!'
    else:
        result = "It's a draw!"

    text = font.render(result, True, YELLOW, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, text_rect)
    pygame.display.update()


"""
MAIN LOOP:
"""


def main():
    # variables:
    board = np.zeros((NUM_ROW, NUM_COL), dtype=int)
    player = 1
    game_over = False

    draw_grid()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x_index, y_index = x//SQUARE_SIDE, y//SQUARE_SIDE
                if board[y_index][x_index] == 0 and game_over == False:
                    board[y_index][x_index] = player
                    draw_figures(player, x_index, y_index)
                    winner = check_winner(board)
                    if winner != None:
                        game_over = True
                        display_winner(winner)
                    elif check_board_full(board):
                        display_winner(None)

                    player *= -1
                pygame.display.update()


if __name__ == "__main__":
    main()
