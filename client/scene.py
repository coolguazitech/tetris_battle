import pygame as pg
from set import Set
import db_utils
from network import Network

# PROTOCOL MESSAGE
MESSAGE_ENDSCENE = "$ENDSCENE"
MESSAGE_STARTGAME = "$STARTGAME"
MESSAGES = [
    MESSAGE_ENDSCENE,
    MESSAGE_STARTGAME
    ]

# WINDOW
WIN_HEIGHT = 600
WIN_WIDTH = 900

# ATTRIBUTES OF SCENE
SIZE_SCORE = int(0.167 * WIN_HEIGHT)
POSITION_SCORE = (int(0.305 * WIN_WIDTH), int(0.577 * WIN_HEIGHT))
COLOR_SCORE = (0, 0, 242)
POSITION_BADGE = (int(0.150 * WIN_WIDTH), int(0.330 * WIN_WIDTH))
POSITION_DIALOGUE = (int(0.500 * WIN_WIDTH), int(0.500 * WIN_HEIGHT))
SIZE_BRICK = 20

# COLORS
COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]
COLOR_BLUE = [0, 0, 255]
COLOR_YELLOW = [255, 255, 0]
COLOR_PURPLE = [255, 0, 255]
COLOR_CYAN = [0, 255, 255]
COLOR_WHITE = [255, 255, 255]
COLORS = [
    COLOR_RED, 
    COLOR_GREEN, 
    COLOR_BLUE, 
    COLOR_YELLOW, 
    COLOR_PURPLE, 
    COLOR_CYAN, 
    COLOR_WHITE
    ]

class Scene:
    def __init__(self):
        self.name = type(self).__name__
        self._rundown = {}
        # {"part1": self.part1, "part2": self.part2}
        self._name_entrance = ""
        self._name_current_part = self._name_entrance
        self._run = True
        self._name_next_scene = ""
        self.events = []
        self._equipment = {}

    def _switch_to_part(self, name_part):
        self._name_current_part = name_part

    # def part1(self):
    #     print("hello1")
    #     name_next_part = "part2"
    #     return name_next_part

    # def part2(self):
    #     print("hello2")
    #     name_next_part = MESSAGE_ENDSCENE
    #     return name_next_part

    def _action(self):
        while self._run:
            name_next_part = self._rundown[self._name_current_part]()
            if name_next_part == MESSAGE_ENDSCENE:
                self._run = False
            else:
                self._switch_to_part(name_next_part)

        # reset
        self._name_current_part = self._name_entrance
        self._run = True
        return self._name_next_scene

    def __call__(self, equipment):
        self._equipment = equipment
        return self._action()
      

class Main_screen(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._rundown = {
            "blit_background": self.blit_background,
            "blit_score": self.blit_score,
            "blit_badge": self.blit_badge,
            "fork_1": self.fork_1,
            "blit_dialogue_queue": self.blit_dialogue_queue,
            "blit_dialogue_error_version": self.blit_dialogue_error_version,
            "blit_dialogue_error_timeout": self.blit_dialogue_error_timeout,
            "fork_2": self.fork_2,
            "fork_3": self.fork_3,
            "fork_4": self.fork_4,
            }
        self._name_entrance = "blit_background"
        self._name_current_part = self._name_entrance
        self._name_next_scene = "Main_screen"

    def blit_background(self):
        Set.blit(self._equipment["images"]["BG_SCENE_Main_screen"], (0, 0))
        name_next_part = "blit_score"
        return name_next_part

    def blit_score(self):
        dict_info = db_utils.fetch(1)
        score = dict_info["SCORE"]
        text_score = Set.get_text(str(score), SIZE_SCORE, COLOR_SCORE, COLOR_WHITE)
        text_score.set_colorkey(COLOR_WHITE)
        Set.blit(text_score, POSITION_SCORE, mode="center")
        name_next_part = "blit_badge"
        return name_next_part

    def blit_badge(self):
        dict_info = db_utils.fetch(1)
        rank, level = dict_info["RANK"][0], dict_info["RANK"][1]
        name_badge = "badge_" + rank + "_" + level
        image_badge = self._equipment["images"][name_badge]
        image_badge.set_colorkey(COLOR_WHITE)
        Set.blit(image_badge, POSITION_BADGE, mode="center")

        name_next_part = "fork_1"
        return name_next_part

    def fork_1(self):
        # TODO: ERROR_TIMEOUT
        # TODO: all exceptions raised in game will lead the footage here
        # check network
        if self._equipment["network"]:
            if not self._equipment["network"].connected:
                if "QUEUE" in self.events:
                    self.events.remove("QUEUE")
            if "ERROR_TIMEOUT" in self._equipment["network"].events:
                self._equipment["network"].events.remove("ERROR_TIMEOUT")
                self.events.append("ERROR_TIMEOUT")
        elif not self._equipment["network"]:
            if "QUEUE" in self.events:
                self.events.remove("QUEUE")
        # fork        
        if len(self.events) == 0 and self._equipment["collection_input"]["SPACE"]:
            network = Network() 
            if network.connected:
                self._equipment["network"] = network
                self.events.append("QUEUE")
                name_next_part = MESSAGE_ENDSCENE
            elif "ERROR_VERSION" in network.events:
                self.events.append("ERROR_VERSION")
                name_next_part = MESSAGE_ENDSCENE
            else:
                name_next_part = MESSAGE_ENDSCENE
        elif "ERROR_TIMEOUT" in self.events:
            name_next_part = "blit_dialogue_error_timeout"
        elif "ERROR_VERSION" in self.events:
            name_next_part = "blit_dialogue_error_version"
        elif "QUEUE" in self.events:
            name_next_part = "blit_dialogue_queue"
        else:
            name_next_part = MESSAGE_ENDSCENE

        return name_next_part

    def blit_dialogue_queue(self):
        image_dialogue_queue = self._equipment["images"]["DIALOGUE_queue"]
        image_dialogue_queue.set_colorkey(COLOR_WHITE)
        Set.blit(image_dialogue_queue, POSITION_DIALOGUE, mode="center")

        name_next_part = "fork_2"
        return name_next_part

    def fork_2(self):
        if "QUEUE" in self.events and MESSAGE_STARTGAME in self._equipment["network"].events:
            self.events.remove("QUEUE")
            name_next_part = MESSAGE_ENDSCENE
            self._name_next_scene = "Game_room"
        elif "QUEUE" in self.events and self._equipment["collection_input"]["q"]:
            self.events.remove("QUEUE")
            self._equipment["network"].disconnect()
            name_next_part = MESSAGE_ENDSCENE
        else:
            name_next_part = MESSAGE_ENDSCENE
        
        return name_next_part


    def blit_dialogue_error_version(self):
        image_dialogue_error_version = self._equipment["images"]["DIALOGUE_error_version"]
        image_dialogue_error_version.set_colorkey(COLOR_WHITE)
        Set.blit(image_dialogue_error_version, POSITION_DIALOGUE, mode="center")

        name_next_part = "fork_3"
        return name_next_part

    def fork_3(self):
        if "ERROR_VERSION" in self.events and self._equipment["collection_input"]["SPACE"]:
            self.events.remove("ERROR_VERSION")
            name_next_part = MESSAGE_ENDSCENE
        else:
            name_next_part = MESSAGE_ENDSCENE
        return name_next_part

    def blit_dialogue_error_timeout(self):
        # image_dialogue_error_version = self._equipment["images"]["DIALOGUE_error_version"]
        # image_dialogue_error_version.set_colorkey(COLOR_WHITE)
        # Set.blit(image_dialogue_error_version, POSITION_DIALOGUE, mode="center")

        name_next_part = "fork_4"
        return name_next_part

    def fork_4(self):
        if "ERROR_TIMEOUT" in self.events and self._equipment["collection_input"]["SPACE"]:
            self.events.remove("ERROR_TIMEOUT")
            name_next_part = MESSAGE_ENDSCENE
        else:
            name_next_part = MESSAGE_ENDSCENE
        return name_next_part
        
class Game_room(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._rundown = {
            "blit_background": self.blit_background,
            }
        self._name_entrance = "blit_background"
        self._name_current_part = self._name_entrance
        self._name_next_scene = "Game_room"

    def blit_background(self):
        Set.blit(self._equipment["images"]["BG_SCENE_Game_room"], (0, 0))
        name_next_part = MESSAGE_ENDSCENE
        return name_next_part