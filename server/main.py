import socket
import threading
import time
from player import Player
from game_platform import Game_platform

# SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SETTING
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (HOST, PORT)
MAX_PLAYERS_IN_QUEUE = 4
MAX_GAMES = MAX_PLAYERS_IN_QUEUE // 2
BUFFER_SIZE = 4096
FORMAT = "utf-8"

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"

# WAITING QUEUE
players = []

# CURRENT GAMES
games = []

# GAME SETTING
GAME_FPS = 60

def thread_game(player1, player2):
    print(f"Game {len(games)} start!")
    game = Game_platform(player1, player2, GAME_FPS)
    games.append(game)

    # start game 
    game.start()

    # to make room in games
    games.remove(game)
    
def wait_for_match():
    if len(players) >= 2 and len(games) < MAX_GAMES:
        player1 = players.pop()
        player2 = players.pop()
        new_game = threading.Thread(target=thread_game, args=(player1, player2))
        new_game.start()

def wait_for_connection():
    try:
        while True:
            if len(players) < MAX_PLAYERS_IN_QUEUE:
                conn, addr = server.accept()
                print(f"({time.ctime()}) [CONNECTED] {addr} connected")
                players.append(Player(conn, addr, BUFFER_SIZE, FORMAT, MESSAGE_DISCONNECT))
            wait_for_match()

    except Exception as e: 
        print("[FAILURE] ", e)


if __name__ == '__main__':
    print(f"({time.ctime()}) [START] server is starting...")
    server.bind(ADDR)

    print(f"({time.ctime()}) [LISTENING] server is listening on {HOST}")
    server.listen(MAX_PLAYERS_IN_QUEUE)

    print(f"({time.ctime()}) [WAITING] server is waiting for connections...")
    wait_for_connection()

    print(f"({time.ctime()}) [SUSPEND] server has been suspended")
    server.close()
