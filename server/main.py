import socket
import threading
import time
from network import Avatar
from game_platform import Platform

# VERSION
VERSION = "1.0.0"

# SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# ADDRESS
HOST = "127.0.0.1"
PORT = 8080
ADDR = (HOST, PORT)

# GAME SETTING

MAX_AVATARS_IN_QUEUE = 2
MAX_PLATFORMS = MAX_AVATARS_IN_QUEUE // 2

# WAITING QUEUE
queue = []

# GAME FIELD
field = []


def detect_and_eradicate_zombies(queue):
    for avatar in queue[:]:
        avatar.greeting()
        if not avatar:
            queue.remove(avatar)

def thread_platform(avatar1, avatar2):
    print(f"Game {len(field) + 1} start!")
    platform = Platform(avatar1, avatar2)
    field.append(platform)

    # to make room in games
    field.remove(platform)
    
def wait_for_match(queue, field):
    detect_and_eradicate_zombies(queue)
    if len(queue) >= 2 and len(field) < MAX_PLATFORMS:
        candidates = queue[:2]
        avatar1 = candidates[0]
        avatar2 = candidates[1]
        queue.remove(avatar1)
        queue.remove(avatar2)
        threading.Thread(target=thread_platform, args=(avatar1, avatar2)).start()

def wait_for_connection(queue, field):
    try:
        while True:
            print(f"there are {len(queue)} avatars in queue, {len(field)} platforms in field")
            if len(queue) < MAX_AVATARS_IN_QUEUE:
                conn, addr = server.accept()
                conn.settimeout(7.0)  
                print(f"({time.ctime()}) [CONNECTED] {addr} connected")
                queue.append(Avatar(conn, addr, VERSION))
            wait_for_match(queue, field)

    except KeyboardInterrupt:
        print("[SHUTDOWN] gracefully disconnected")

    except socket.error as e: 
        print("[FAILURE] ", e)




if __name__ == '__main__':
    print(f"({time.ctime()}) [START] server is starting...")
    server.bind(ADDR)

    print(f"({time.ctime()}) [LISTENING] server is listening on {HOST}")
    server.listen(MAX_AVATARS_IN_QUEUE)

    print(f"({time.ctime()}) [WAITING] server is waiting for connections...")
    wait_for_connection(queue, field)

    print(f"({time.ctime()}) [SUSPEND] server has been suspended")
    server.close()
