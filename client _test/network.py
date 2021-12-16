import socket
import threading
import time
import json
from distutils.util import strtobool 

VERSION = "1.0.0"

# PROTOCOL TAGS
ERROR_TIMEOUT = "$ERROR_TIMEOUT"
ERROR_VERSION = "$ERROR_VERSION"
MESSAGE_GREETING = "$GREETING"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"
MESSAGE_STARTGAME1 = "$STARTGAME1"
MESSAGE_STARTGAME2 = "$STARTGAME2"

# SERVER ADDRESS
HOST = "127.0.0.1"
PORT = 8080
ADDR = (HOST, PORT)

# METADAT
SIZE_HEADER = 4
SIZE_BUFFER = 1500
FORMAT = "utf-8"

class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.trace_code = 0
        self.connected = False
        self.number = 1
        self.in_match = False
        self.mailbox = {
            1: {
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "score": 0,
                "badge": "D0",
                "trace_code": 0,
                "tags": []
            },
            2: { # read-only
                "queue_bricks1": None,
                "cur_brick1": None,
                "pool1": None,
                "motion_eliminate1": [1, -1],
                "speed1": 1,
                "score1": 1,
                "badge1": "D0",
                "trace_code1": 0,
                "queue_bricks2": None,
                "cur_brick2": None,
                "pool2": None,
                "motion_eliminate2": [1, -1],
                "speed2": 1, 
                "score2": 1,
                "badge2": "D0",
                "trace_code2": 0,
                "tags": []
            }
        }
        self.events = []
        try:
            self._client.settimeout(20.0)
            self._client.connect(ADDR)
            if self.greeting():
                threading.Thread(target=self._wait_for_match).start()
        except socket.error:
            self._disconnected()
    
    def greeting(self):
        try:
            self.request(MESSAGE_GREETING + VERSION)
            data = self._get_all_data()
            data, is_valid = data[:9], bool(strtobool(data[9:]))
            if data == MESSAGE_GREETING and is_valid:
                print(f"({time.ctime()}) [CONNECTED] successfully connected to server")
                self.connected = True
                return True
            elif not is_valid:
                self.events.append(ERROR_VERSION)
                return False
            else:
                return False

        except socket.timeout:
            self._disconnected()
            self.events.append(ERROR_TIMEOUT)

        except socket.error as e: 
            print(f"({time.ctime()}) [ABORTION] connection attempt has been aborted since ", e)
            self._disconnected()
            return False

    def disconnect(self):
        # cancle queue
        self._disconnected()
        
    def request(self, msg):
        try:
            msg = f"{len(msg):<{SIZE_HEADER}}" + msg
            self._client.sendall(msg.encode(FORMAT))

        except socket.timeout:
            self._disconnected()
            self.events.append(ERROR_TIMEOUT)

        except socket.error as e: 
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def receive(self):
        try:
            data = self._get_all_data()
            if data == MESSAGE_GREETING:
                self.request(MESSAGE_GREETING)
                return -1, None
            elif data[-1].isdigit():
                id_player, data = self._split_signature(data)
                game_property = json.loads(data)

            if MESSAGE_PLAYER1WIN in game_property["tags"] or \
                MESSAGE_PLAYER2WIN in game_property["tags"]:
                if MESSAGE_PLAYER1WIN in game_property["tags"]:
                    self.events.append(MESSAGE_PLAYER1WIN)
                    self._disconnected()
                else:
                    self.events.append(MESSAGE_PLAYER2WIN)
                    self._disconnected()
                return -1, None
            else:
                return int(id_player), data

        except socket.timeout as e:
            self._disconnected()
            self.events.append(ERROR_TIMEOUT)

        except socket.error as e: 
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def _disconnected(self):
        print(f"({time.ctime()}) [DISCONNECTED] you have disconnected")
        self.connected = False
        self._client.close()

    def _wait_for_match(self):
        while self.connected:
            if not self.receive()[1]:
                continue
            else:
                self.in_match = True
                break
                

    def postman_work(self):
        while True:
            if self.connected:
                id_player, game_property = self.receive()
                if id_player == -1:
                    break
                self.number = id_player
                dict_data = json.loads(game_property)
                if MESSAGE_STARTGAME1 in dict_data["tags"] or \
                    MESSAGE_STARTGAME2 in dict_data["tags"]: 
                    if id_player == 1 and MESSAGE_STARTGAME1 in dict_data["tags"]:
                        self.events.append(MESSAGE_STARTGAME1)
                    elif id_player == 2 and MESSAGE_STARTGAME2 in dict_data["tags"]:
                        self.events.append(MESSAGE_STARTGAME2)

                if dict_data["trace_code" + str(id_player)] == self.trace_code:
                    self.mailbox[2].update(dict_data)
                    self.trace_code += 1
                    self.mailbox[1]["trace_code"] = self.trace_code
                    self.request(json.dumps(self.mailbox[1]))
                    break
       

    def _split_signature(self, data):
        return data[-1], data[:-1]

    def _get_all_data(self):
        full_msg = ''
        msglen = int(self._client.recv(SIZE_HEADER))
        while msglen > 0:
            if SIZE_BUFFER > msglen - SIZE_BUFFER:
                msg = self._client.recv(msglen)
                full_msg += msg.decode(FORMAT)
                return full_msg
            if msglen - SIZE_BUFFER >= SIZE_BUFFER:
                msg = self._client.recv(SIZE_BUFFER)
                full_msg += msg.decode(FORMAT)
                msglen -= SIZE_BUFFER
        return full_msg
