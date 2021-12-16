from scene import *
from network import Network

# ATTRIBUTES 
SIZE_SCORE = int(0.167 * WIN_HEIGHT)
POSITION_SCORE = (int(0.305 * WIN_WIDTH), int(0.577 * WIN_HEIGHT))
COLOR_THEME_BLUE = (0, 0, 242)
POSITION_BADGE = (int(0.150 * WIN_WIDTH), int(0.330 * WIN_WIDTH))
POSITION_DIALOGUE = (int(0.500 * WIN_WIDTH), int(0.500 * WIN_HEIGHT))
SIZE_VERSION = int(0.0275 * WIN_HEIGHT)
POSITION_VERSION = (int(0.925 * WIN_WIDTH), int(0.950 * WIN_HEIGHT))

class Main_screen(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._rundown = {
            "init": self.init,
            "blit_background": self.blit_background,
            "blit_version": self.blit_version,
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

    def blit_background(self):
        Set.blit(self._equipment["images"]["BG_SCENE_Main_screen"], (0, 0))
        name_next_part = "blit_version"
        return name_next_part

    def blit_version(self):
        version = "version " + Set.version
        text_version = Set.get_text(version, SIZE_VERSION, COLOR_WHITE, COLOR_BLACK)
        text_version.set_colorkey(COLOR_BLACK)
        Set.blit(text_version, POSITION_VERSION, mode="center")
        name_next_part = "blit_score"
        return name_next_part

    def blit_score(self):
        score = self._equipment["public_info"]["score"]
        text_score = Set.get_text(str(score), SIZE_SCORE, COLOR_THEME_BLUE, COLOR_WHITE)
        text_score.set_colorkey(COLOR_WHITE)
        Set.blit(text_score, POSITION_SCORE, mode="center")
        name_next_part = "blit_badge"
        return name_next_part

    def blit_badge(self):
        badge = self._equipment["public_info"]["badge"]
        rank, level = badge[0], badge[1]
        name_badge = "badge_" + rank + "_" + level
        image_badge = self._equipment["images"][name_badge]
        image_badge.set_colorkey(COLOR_WHITE)
        Set.blit(image_badge, POSITION_BADGE, mode="center")
        name_next_part = "fork_1"
        return name_next_part

    def fork_1(self):
        # TODO: all exceptions raised in game will lead the footage here
        # check network
        if self._equipment["network"]:
            if not self._equipment["network"].connected:
                self.events = list(filter((EVENT_QUEUE).__ne__, self.events))
            if ERROR_TIMEOUT in self._equipment["network"].events:
                self._equipment["network"].events = []
                self.events.append(ERROR_TIMEOUT)
        elif not self._equipment["network"]:
            self.events = list(filter((EVENT_QUEUE).__ne__, self.events))
        # fork        
        if len(self.events) == 0 and self._equipment["collection_input"]["SPACE"]:
            network = Network() 
            if network.connected:
                self._equipment["network"] = network
                self.events.append(EVENT_QUEUE)
                name_next_part = MESSAGE_ENDSCENE
            elif ERROR_VERSION in network.events:
                self.events.append(ERROR_VERSION)
                name_next_part = MESSAGE_ENDSCENE
            else:
                name_next_part = MESSAGE_ENDSCENE
        elif ERROR_TIMEOUT in self.events:
            name_next_part = "blit_dialogue_error_timeout"
        elif ERROR_VERSION in self.events:
            name_next_part = "blit_dialogue_error_version"
        elif EVENT_QUEUE in self.events:
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
        if MESSAGE_STARTGAME1 in self._equipment["network"].events or \
            MESSAGE_STARTGAME2 in self._equipment["network"].events:
            self.events = list(filter((EVENT_QUEUE).__ne__, self.events))
            name_next_part = MESSAGE_ENDSCENE
            for i in range(1, 3):
                self._equipment["network"].events = list(filter(
                    (eval(f"MESSAGE_STARTGAME{i}")).__ne__, 
                    self._equipment["network"].events
                    ))
            self._name_next_scene = "Game_room"
            self.events.append(EVENT_CHANGESCENE)
            return name_next_part
        elif EVENT_QUEUE in self.events and self._equipment["collection_input"]["q"]:
            self.events = list(filter((EVENT_QUEUE).__ne__, self.events))
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
        if ERROR_VERSION in self.events and self._equipment["collection_input"]["SPACE"]:
            self.events = list(filter((ERROR_VERSION).__ne__, self.events))
            name_next_part = MESSAGE_ENDSCENE
        else:
            name_next_part = MESSAGE_ENDSCENE
        return name_next_part

    def blit_dialogue_error_timeout(self):
        image_dialogue_error_timeout = self._equipment["images"]["DIALOGUE_error_timeout"]
        image_dialogue_error_timeout.set_colorkey(COLOR_WHITE)
        Set.blit(image_dialogue_error_timeout, POSITION_DIALOGUE, mode="center")

        name_next_part = "fork_4"
        return name_next_part

    def fork_4(self):
        if ERROR_TIMEOUT in self.events and self._equipment["collection_input"]["SPACE"]:
            self.events = list(filter((ERROR_TIMEOUT).__ne__, self.events))
            name_next_part = MESSAGE_ENDSCENE
        else:
            name_next_part = MESSAGE_ENDSCENE
        return name_next_part