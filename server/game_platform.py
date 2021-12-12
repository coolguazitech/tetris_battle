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
            2: {
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "score": 0,
                "badge": "D0",
                "trace_code": 0,
                "tags": []
            },
            3: {
                "queue_bricks1": None,
                "cur_brick1": None,
                "pool1": None,
                "motion_eliminate1": None,
                "speed1": 1,
                "score1": 1,
                "badge1": "D0",
                "trace_code1": 0,
                "queue_bricks2": None,
                "cur_brick2": None,
                "pool2": None,
                "motion_eliminate2": None,
                "speed2": 1, 
                "score2": 1,
                "badge2": "D0",
                "trace_code2": None,
                "tags": []
            }
        }
        threading.Thread(target=self._postman1_work).start()
        threading.Thread(target=self._postman2_work).start()
        threading.Thread(target=self._postman3_work).start()
        Game(self.mailbox).main_loop()

    def _postman1_work(self):
        while self.avatar1:
            self.mailbox[1].update(json.loads(self.avatar1.receive()))

    def _postman2_work(self):
        while self.avatar2:
            self.mailbox[2].update(json.loads(self.avatar2.receive()))

    def _postman3_work(self):
        time.sleep(1.0 / GAME_FPS)
        while self.avatar1 or self.avatar2:
            if self.avatar1:
                data = self._attach_signature(json.dumps(self.mailbox[3]), "1")
                self.avatar1.response(data)
            if self.avatar2:
                data = self._attach_signature(json.dumps(self.mailbox[3]), "2")
                self.avatar2.response(data)

    def _attach_signature(self, data, signature):
        """attach signature to data to proclaim who will receive"""
        data += signature
        return data