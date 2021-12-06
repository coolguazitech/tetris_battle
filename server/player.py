import time

# SETTING
HOST = "192.168.100.5"
PORT = 8080
ADDR = (HOST, PORT)
BUFFER_SIZE = 4096
FORMAT = "utf-8"

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"

class Player:
    def __init__(self, conn):
        self._conn = conn
        self.connected = False

    def greeting(self):
        try:
            self._conn.send(MESSAGE_GREETING.encode(FORMAT))
            response = self._conn.recv(BUFFER_SIZE).decode(FORMAT)
            if response == MESSAGE_GREETING:
                self.connected = True

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def receive(self):
        try:
            data = self._conn.recv(BUFFER_SIZE).decode(FORMAT)
            if data == MESSAGE_DISCONNECT:
                self._disconnected()
                return MESSAGE_ZOMBIE
            if data == MESSAGE_GREETING:
                self.response(MESSAGE_GREETING)
                self.connected = True
            return data
            
        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()
            return MESSAGE_ZOMBIE

    def response(self, msg):
        try:
            self._conn.send(msg.encode(FORMAT))

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def _disconnected(self):
        print(f"({time.ctime()}) [DISCONNECTED] {ADDR} has disconnected")
        self.connected = False
        self._conn.close()