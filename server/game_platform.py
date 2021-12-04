import time
import threading
from game import Game
import json

# PROTOCOL MESSAGE
MESSAGE_DELIVERY = "$DELIVERY"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"


class Game_platform:
    def __init__(self, player1, player2, cycle_per_second):
        self.player1 = player1
        self.player2 = player2
        self.mailbox = {
            1: json.dumps({
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
            }),
            2: json.dumps({
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
            }),
            3: json.dumps({
                "queue_bricks1": None,
                "cur_brick1": None,
                "pool1": None,
                "queue_bricks2": None,
                "cur_brick2": None,
                "pool2": None
            })
        }
        self._cycle_per_second = cycle_per_second
        # TODO: send a start message, if responsed, go onto the next
        threading.Thread(target=self._postman1_work).start()
        threading.Thread(target=self._postman2_work).start()
        threading.Thread(target=self._postman3_work).start()

    def start(self):
        game = Game(self._cycle_per_second, self.mailbox)
        game.main_loop()

    def _postman1_work(self):
        while self.player1.connected:
            self.mailbox[1] = self.player1.receive()

    def _postman2_work(self):
        while self.player2.connected:
            self.mailbox[2] = self.player2.receive()

    def _postman3_work(self):
        time.sleep(1.0 / self._cycle_per_second)
        while self.player1.connected or self.player2.connected:
            if self.player1.connected:
                self.player1.response(self.mailbox[3])
            if self.player2.connected:
                self.player2.response(self.mailbox[3])