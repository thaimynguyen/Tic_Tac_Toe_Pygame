import pygame
import numpy as np
import time

pygame.init()

"""
CONSTANTS:
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
NUM_COL = 3
NUM_ROW = NUM_COL
SQUARE_SIDE = SCREEN_WIDTH // NUM_COL
MIDDLE_POINT = SQUARE_SIDE // 2
MARGIN = SQUARE_SIDE // 5


BORDER_WIDTH = 10
LINE_WIDTH = 5
CIRCLE_RADIUS = SQUARE_SIDE // 3

font = pygame.font.SysFont("comicsans", SCREEN_WIDTH // 5)

# Define colours using RGB:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up Pygame window:
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

"""
FUNCTIONS:
"""


def initialize_window():
    global SCREEN, board, player, game_over, running
    board = np.zeros((NUM_ROW, NUM_COL), dtype=int)
    player = 1
    game_over = False
    running = True
    pygame.display.set_caption("Tic Tac Toe")
    SCREEN.fill(WHITE)
    draw_grid()


def draw_grid():
    global SCREEN
    for x in range(1, NUM_COL):
        # vertical borders
        pygame.draw.line(
            SCREEN,
            BLACK,
            (SCREEN_WIDTH // NUM_COL * x - BORDER_WIDTH // 2, 0),
            (SCREEN_WIDTH // NUM_COL * x - BORDER_WIDTH // 2, SCREEN_WIDTH),
            BORDER_WIDTH,
        )
        # horizontal borders
        pygame.draw.line(
            SCREEN,
            BLACK,
            (0, SCREEN_HEIGHT // NUM_ROW * x - BORDER_WIDTH // 2),
            (SCREEN_HEIGHT, SCREEN_HEIGHT // NUM_ROW * x - BORDER_WIDTH // 2),
            BORDER_WIDTH,
        )
    pygame.display.update()


def draw_figures(player, x_index, y_index):
    if player == 1:  # Player O
        pygame.draw.circle(
            SCREEN,
            BLUE,
            (
                MIDDLE_POINT + x_index * SQUARE_SIDE,
                MIDDLE_POINT + y_index * SQUARE_SIDE,
            ),
            CIRCLE_RADIUS,
            LINE_WIDTH,
        )
    if player == -1:  # Player X
        pygame.draw.line(
            SCREEN,
            RED,
            (MARGIN + x_index * SQUARE_SIDE, MARGIN + y_index * SQUARE_SIDE),
            (
                (x_index + 1) * SQUARE_SIDE - MARGIN,
                (y_index + 1) * SQUARE_SIDE - MARGIN,
            ),
            LINE_WIDTH,
        )
        pygame.draw.line(
            SCREEN,
            RED,
            ((x_index + 1) * SQUARE_SIDE - MARGIN, MARGIN + y_index * SQUARE_SIDE),
            (MARGIN + x_index * SQUARE_SIDE, (y_index + 1) * SQUARE_SIDE - MARGIN),
            LINE_WIDTH,
        )


def check_winner(board):
    sum_cols = np.sum(board, axis=0)
    sum_rows = np.sum(board, axis=1)
    winning_col = None
    winning_row = None
    winner = None

    # check & draw vertical winning lines
    if NUM_COL in sum_cols:
        winning_col = int(list(np.where(sum_cols == NUM_COL))[0])
        pygame.draw.line(
            SCREEN,
            BLUE,
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, 0),
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        winner = "O"
    elif -NUM_COL in sum_cols:
        winning_col = int(list(np.where(sum_cols == -NUM_COL))[0])
        pygame.draw.line(
            SCREEN,
            RED,
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, 0),
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        winner = "X"

    # check & draw horizontal winning lines
    elif NUM_COL in sum_rows:
        winning_row = int(list(np.where(sum_rows == NUM_COL))[0])
        pygame.draw.line(
            SCREEN,
            BLUE,
            (0, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            (SCREEN_WIDTH, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            LINE_WIDTH,
        )
        winner = "O"
    elif -NUM_COL in sum_rows:
        winning_row = int(list(np.where(sum_rows == -NUM_COL))[0])
        pygame.draw.line(
            SCREEN,
            RED,
            (0, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            (SCREEN_WIDTH, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            LINE_WIDTH,
        )
        winner = "X"

    # check & draw diagonal winning lines:
    elif sum(np.diagonal(board)) == NUM_COL:
        pygame.draw.line(
            SCREEN,
            BLUE,
            (MARGIN, MARGIN),
            (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "O"
    elif sum(np.diagonal(board)) == -NUM_COL:
        pygame.draw.line(
            SCREEN,
            RED,
            (MARGIN, MARGIN),
            (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "X"
    elif sum(np.rot90(board).diagonal()) == NUM_COL:
        pygame.draw.line(
            SCREEN,
            BLUE,
            (SCREEN_WIDTH - MARGIN, MARGIN),
            (MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "O"
    elif sum(np.rot90(board).diagonal()) == -NUM_COL:
        pygame.draw.line(
            SCREEN,
            RED,
            (SCREEN_WIDTH - MARGIN, MARGIN),
            (MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "X"

    return winner


def check_board_full(board):
    for row in range(NUM_ROW):
        for col in range(NUM_COL):
            if board[row][col] == 0:
                return False
    return True


def display_winner(winner):
    if winner != None:
        result = winner + " WON!"
    else:
        result = "It's a draw!"

    text = font.render(result, True, YELLOW, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, text_rect)
    pygame.display.update()


def check_gameover(winner, board):
    if winner != None or check_board_full(board):
        display_winner(winner)
        game_over = True
        return game_over


def click_board(x, y, board, player):
    global game_over
    x_index, y_index = x // SQUARE_SIDE, y // SQUARE_SIDE
    if board[y_index][x_index] == 0:
        board[y_index][x_index] = player
        draw_figures(player, x_index, y_index)
        winner = check_winner(board)
        game_over = check_gameover(winner, board)
    pygame.display.update()


def run_game():
    global board, player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            pygame.mixer.Sound("click_sound.mp3").play()
            click_board(x, y, board, player)
            player *= -1


def reset_game():
    time.sleep(3)
    initialize_window()

    text = font.render("NEW GAME", True, WHITE, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    running = True
                    time.sleep(1)
                    initialize_window()
                    return running


"""
MAIN LOOP:
"""


def main():
    initialize_window()
    while running:
        run_game()

        if game_over:
            reset_game()


if __name__ == "__main__":
    main()
