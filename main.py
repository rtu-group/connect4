import pygame
import numpy as np

# initialize Pygame
pygame.init()

# create the game window
WIDTH = 700
HEIGHT = 600
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
FONT_SIZE = 50
ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# create the board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# drop a piece onto the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# check if a location is valid
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# get the next open row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# check if the game is over
def winning_move(board, piece):
    # check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# draw the board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

# initialize the game
def initialize_game():
    game_over = False
    turn = 0
    board = create_board()

    pygame.font.init()
    font = pygame.font.SysFont(None, FONT_SIZE)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                # ask for player 1 input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(np.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = font.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

                # ask for player 2 input
                else:
                    posx = event.pos[0]
                    col = int(np.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = font.render("Player 2 wins!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True

                turn += 1
                turn = turn % 2

                draw_board(board)

                if game_over:
                    pygame.time.wait(3000)

# start the game
initialize_game()
