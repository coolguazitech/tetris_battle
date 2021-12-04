import time

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"

class Player:
    def __init__(self, conn, addr, buffer_size, format):
        self._conn = conn
        self._addr = addr
        self._buffer_size = buffer_size
        self._format = format
        self.connected = False
        if self.receive() == MESSAGE_GREETING:
            self.response(MESSAGE_GREETING)
            self.connected = True

    def receive(self):
        try:
            data = self._conn.recv(self._buffer_size).decode(self._format)
            if data == MESSAGE_DISCONNECT:
                self._disconnected()
                return MESSAGE_ZOMBIE
            return data
            
        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()
            return MESSAGE_ZOMBIE

    def response(self, msg):
        try:
            self._conn.send(msg.encode(self._format))

        except Exception as e:
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def _disconnected(self):
        print(f"({time.ctime()}) [DISCONNECTED] {self._addr} has disconnected")
        self.connected = False
        self._conn.close()
