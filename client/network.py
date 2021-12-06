import socket
import time


# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"
MESSAGES = [MESSAGE_DISCONNECT, MESSAGE_ZOMBIE, MESSAGE_GREETING, MESSAGE_PLAYER1WIN, MESSAGE_PLAYER2WIN]

# SETTING
HOST = "192.168.100.5"
PORT = 8080
ADDR = (HOST, PORT)
BUFFER_SIZE = 4096
FORMAT = "utf-8"

class Network:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.trace_code = 0
        self.connected = False
        self._client.connect(ADDR)
        self.greeting()
        
    
    def greeting(self):
        self.request(MESSAGE_GREETING)
        try:
            data = self._client.recv(BUFFER_SIZE).decode(FORMAT)
            if data == MESSAGE_GREETING:
                print(f"({time.ctime()}) [CONNECTED] successfully connected to server")
                self.connected = True

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            print(f"({time.ctime()}) [ABORTION] connection attempt has been aborted")
            self._disconnected()

    def disconnect(self):
        self._disconnected()
        
    def request(self, msg):
        try:
            self._client.send(msg.encode(FORMAT))

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def receive(self):
        try:
            data = self._client.recv(BUFFER_SIZE).decode(FORMAT)
            if data == MESSAGE_PLAYER1WIN or data == MESSAGE_PLAYER2WIN:
                self.request(MESSAGE_DISCONNECT)
                self._disconnected()
            elif data == MESSAGE_GREETING:
                self.request(MESSAGE_GREETING)
            return data

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()
            return data
 
    def _disconnected(self):
        print(f"({time.ctime()}) [DISCONNECTED] you have disconnected")
        self.connected = False
        self._client.close()
