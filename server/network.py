import time
import socket

# METADATA
SIZE_HEADER = 8
SIZE_BUFFER = 64
FORMAT = "utf-8"

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"
MESSAGES = [
    MESSAGE_DISCONNECT,
    MESSAGE_ZOMBIE, 
    MESSAGE_GREETING, 
    ]

class Avatar:
    def __init__(self, conn, addr, version):
        self.conn = conn
        self.addr = addr
        self._version = version
        self.connected = False
        self.receive()

    def greeting(self):
        try:
            msg = f"{len(MESSAGE_GREETING):<{SIZE_HEADER}}" + MESSAGE_GREETING
            self.conn.send(msg.encode(FORMAT))

            response = self._get_all_data()
            if response == MESSAGE_GREETING:
                self.connected = True

        except socket.error as e: 
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def receive(self):
        try:
            data = self._get_all_data()
            if data[:9] == MESSAGE_GREETING:
                data, version = data[:9], data[9:]
                self.response(data + str(version == self._version))
                self.connected = version == self._version
                if version != self._version:
                    self._disconnected()

            elif data == MESSAGE_DISCONNECT:
                self._disconnected()
                return MESSAGE_ZOMBIE

            return data
            
        except socket.error as e: 
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()
            return MESSAGE_ZOMBIE

    def response(self, msg):
        try:
            msg = f"{len(msg):<{SIZE_HEADER}}" + msg
            self.conn.send(msg.encode(FORMAT))

        except socket.error as e: 
            print(f"({time.ctime()}) [EXCEPTION] ", e)
            self._disconnected()

    def _disconnected(self):
        print(f"({time.ctime()}) [DISCONNECTED] {self.addr} has disconnected")
        self.connected = False
        self.conn.close()

    def _get_all_data(self):
        full_msg = ''
        msglen = int(self.conn.recv(SIZE_HEADER))
        while msglen > 0:
            if SIZE_BUFFER > msglen - SIZE_BUFFER:
                msg = self.conn.recv(msglen)
                full_msg += msg.decode(FORMAT)
                return full_msg
            if msglen - SIZE_BUFFER >= SIZE_BUFFER:
                msg = self.conn.recv(SIZE_BUFFER)
                full_msg += msg.decode(FORMAT)
                msglen -= SIZE_BUFFER
        return full_msg

