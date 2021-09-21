import pygame
import numpy as np
import time

pygame.init()

"""
CONSTANTS:
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
SIDE = 3
SQUARE_SIDE = SCREEN_WIDTH // SIDE
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
    global SCREEN, board, player, game_over
    boardy = np.zeros((SIDE, SIDE), dtype=int)
    player = 1
    game_over = False
    pygame.display.set_caption("Tic Tac Toe")
    SCREEN.fill(WHITE)
    draw_grid()


def draw_grid():
    global SCREEN
    for x in range(1, SIDE):
        # vertical borders
        pygame.draw.line(
            SCREEN,
            BLACK,
            (SCREEN_WIDTH // SIDE * x - BORDER_WIDTH // 2, 0),
            (SCREEN_WIDTH // SIDE * x - BORDER_WIDTH // 2, SCREEN_WIDTH),
            BORDER_WIDTH,
        )
        # horizontal borders
        pygame.draw.line(
            SCREEN,
            BLACK,
            (0, SCREEN_HEIGHT // SIDE * x - BORDER_WIDTH // 2),
            (SCREEN_HEIGHT, SCREEN_HEIGHT // SIDE * x - BORDER_WIDTH // 2),
            BORDER_WIDTH,
        )
    pygame.display.update()


def draw_figures(player: int, x_index: int, y_index: int):
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


def check_winner(board: np.array) -> str:
    sum_cols = np.sum(board, axis=0)
    sum_rows = np.sum(board, axis=1)
    winning_sum = len(board)
    winning_col = None
    winning_row = None
    winner = None

    # check & draw vertical winning lines
    if winning_sum in sum_cols:
        winning_col = int(list(np.where(sum_cols == winning_sum))[0])
        pygame.draw.line(
            SCREEN,
            BLUE,
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, 0),
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        winner = "O"
    elif -winning_sum in sum_cols:
        winning_col = int(list(np.where(sum_cols == -winning_sum))[0])
        pygame.draw.line(
            SCREEN,
            RED,
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, 0),
            (MIDDLE_POINT + winning_col * SQUARE_SIDE, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        winner = "X"

    # check & draw horizontal winning lines
    elif winning_sum in sum_rows:
        winning_row = int(list(np.where(sum_rows == winning_sum))[0])
        pygame.draw.line(
            SCREEN,
            BLUE,
            (0, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            (SCREEN_WIDTH, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            LINE_WIDTH,
        )
        winner = "O"
    elif -winning_sum in sum_rows:
        winning_row = int(list(np.where(sum_rows == -winning_sum))[0])
        pygame.draw.line(
            SCREEN,
            RED,
            (0, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            (SCREEN_WIDTH, MIDDLE_POINT + winning_row * SQUARE_SIDE),
            LINE_WIDTH,
        )
        winner = "X"

    # check & draw diagonal winning lines:
    elif sum(np.diagonal(board)) == winning_sum:
        pygame.draw.line(
            SCREEN,
            BLUE,
            (MARGIN, MARGIN),
            (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "O"
    elif sum(np.diagonal(board)) == -winning_sum:
        pygame.draw.line(
            SCREEN,
            RED,
            (MARGIN, MARGIN),
            (SCREEN_WIDTH - MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "X"
    elif sum(np.rot90(board).diagonal()) == winning_sum:
        pygame.draw.line(
            SCREEN,
            BLUE,
            (SCREEN_WIDTH - MARGIN, MARGIN),
            (MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "O"
    elif sum(np.rot90(board).diagonal()) == -winning_sum:
        pygame.draw.line(
            SCREEN,
            RED,
            (SCREEN_WIDTH - MARGIN, MARGIN),
            (MARGIN, SCREEN_WIDTH - MARGIN),
            LINE_WIDTH,
        )
        winner = "X"

    return winner


def check_board_full(board: np.array) -> bool:
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return False
    return True


def display_winner(winner: str):
    if winner != None:
        result = winner + " WON!"
    else:
        result = "It's a draw!"

    winner_text = font.render(result, True, YELLOW, BLACK)
    winner_text_rect = winner_text.get_rect()
    winner_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(winner_text, winner_text_rect)
    pygame.display.update()


def check_game_over(winner: str, board: np.array):
    global game_over
    if winner != None or check_board_full(board):
        display_winner(winner)
        game_over = True


def click_board(x: int, y: int, board: np.array, player: int):
    x_index, y_index = x // SQUARE_SIDE, y // SQUARE_SIDE
    if board[y_index][x_index] == 0:
        board[y_index][x_index] = player
        draw_figures(player, x_index, y_index)
        winner = check_winner(board)
        check_game_over(winner, board)
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


def reset_game() -> bool:
    reset_text = font.render("NEW GAME", True, WHITE, BLACK)
    reset_text_rect = reset_text.get_rect()
    reset_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
    SCREEN.blit(reset_text, reset_text_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_text_rect.collidepoint(event.pos):
                    initialize_window()
                    return True


"""
MAIN LOOP:
"""


def main():
    initialize_window()
    while True:
        run_game()
        if game_over:
            reset_game()


if __name__ == "__main__":
    main()
