import socket
import threading
import time

# CLIENT
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SETTING
HOST = "192.168.100.5"
PORT = 8080
ADDR = (HOST, PORT)
BUFFER_SIZE = 4096
FORMAT = "utf-8"

# PROTOCOL MESSAGE
DISCONNECT_MESSAGE = "$DISCONNECT"
ZOMBIE_MESSAGE = "$ZOMBIE"
GREETING_MESSAGE = "$GREETING"

# def disconnect():
#     print(f"({time.ctime()}) [DISCONNECTED] {self._addr} has disconnected")
#         self._conn.close()

def send(msg):
    try:
        client.send(msg.encode(FORMAT))
        return client.recv(BUFFER_SIZE).decode()

    except Exception as e:
        print(e)


data = "data "

if __name__ == '__main__':
    try:
        print(f"({time.ctime()}) [CONNECTING] connecting to server...")
        client.connect(ADDR)
        response = send("$GREETING")
        if response == "$GREETING":
            print(f"({time.ctime()}) [CONNECTED] successfully connected to server")
        else:
            print(f"({time.ctime()}) [ABORTION] connection attempt has been aborted")
            client.close()

    except Exception as e:
        print(e)
        print(f"({time.ctime()}) [ABORTION] connection attempt has been aborted")
        client.close()

    count = 0
    while count < 100:
        time.sleep(1)
        response = send(data + str(count))
        print(response)
        count += 1

# TODO: if recieving win message then send DISCONNECT_MESSAGE
# TODO: first recive consisting of Nones