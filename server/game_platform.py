import time
import threading
from game import Game
import json

# GAME SETTING
GAME_FPS = 60

class Platform:
    def __init__(self, avatar1, avatar2):
        self.avatar1 = avatar1
        self.avatar2 = avatar2
        self.mailbox = {
            1: json.dumps({
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "trace_code": 0
            }),
            2: json.dumps({
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "trace_code": 0
            }),
            3: json.dumps({
                "queue_bricks1": None,
                "cur_brick1": None,
                "pool1": None,
                "motion_eliminate1": None,
                "speed1": None,
                "trace_code1": 0,
                "queue_bricks2": None,
                "cur_brick2": None,
                "pool2": None,
                "motion_eliminate2": None,
                "speed2": None,
                "trace_code2": None
            })
        }
        threading.Thread(target=self._postman1_work).start()
        threading.Thread(target=self._postman2_work).start()
        threading.Thread(target=self._postman3_work).start()
        Game(self.mailbox).main_loop()

    def _postman1_work(self):
        while self.avatar1.connected:
            self.mailbox[1] = self.avatar1.receive()

    def _postman2_work(self):
        while self.avatar2.connected:
            self.mailbox[2] = self.avatar2.receive()

    def _postman3_work(self):
        time.sleep(1.0 / GAME_FPS)
        while self.avatar1.connected or self.avatar2.connected:
            if self.avatar1.connected:
                data = self._attach_signature(self.mailbox[3], "1")
                self.avatar1.response(data)
            if self.avatar2.connected:
                data = self._attach_signature(self.mailbox[3], "2")
                self.avatar2.response(data)

    def _attach_signature(self, data, signature):
        """attach signature to data to proclaim who will receive"""
        data += signature
        return data