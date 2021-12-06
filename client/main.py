import socket
import threading
import time
import pygame as pg


# VERSION
VERSION = "1.0.0"

# INITIALIZATION
pg.init()
pg.font.init()

# WINDOW
WIN_HEIGHT = 600
WIN_WIDTH = 900
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption('Tetris Battle')

# CLOCK
CLOCK = pg.time.Clock()

# PROCEDURE CONTROLLER
GAME_FPS = 60
RUN = True
STAGE = 0

# CONSTANTS
COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]
COLOR_BLUE = [0, 0, 255]
COLOR_YELLOW = [255, 255, 0]
COLOR_PURPLE = [255, 0, 255]
COLOR_CYAN = [0, 255, 255]
COLOR_WHITE = [255, 255, 255]
BRICK_SIZE = 30
BRICK_COLORS = [COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_PURPLE, COLOR_CYAN, COLOR_WHITE]
POOL_HEIGHT = 20
POOL_WIDTH = 10

# GAME VARIABLES
BG_STAGE_1 = pg.Surface(WIN.get_size()).convert()

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"
MESSAGES = [MESSAGE_DISCONNECT, MESSAGE_ZOMBIE, MESSAGE_GREETING, MESSAGE_PLAYER1WIN, MESSAGE_PLAYER2WIN]


while RUN:
    CLOCK.tick(GAME_FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            RUN = False

pg.quit()



# TODO: first recive consisting of Nones
# TODO: if receive fails, except back to stage 1