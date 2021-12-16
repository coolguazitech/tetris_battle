from scene import *
import pygame as pg

class Intro(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._rundown = {
            "init": self.init,
            "blit_background": self.blit_background,
            "fork_1": self.fork_1,
            }
        self._name_entrance = "blit_background"
        self._name_current_part = self._name_entrance
        self._count_motion = 1 # 1 ~ 1950
        self._delay = 900

    def blit_background(self):
        if self._delay > 0:
            intro = self._equipment["images"]["intro_1"]
            self._delay -= 1
            self._count_motion = 1
            Set.blit(intro, (0, 0))
            name_next_part = "fork_1"
            return name_next_part
        if self._count_motion <= 1641:
            pg.time.wait(10)
            intro = self._equipment["images"][f"intro_{self._count_motion}"]
            Set.blit(intro, (0, 0))
            name_next_part = "fork_1"
            return name_next_part
        if self._count_motion > 1641:
            intro = self._equipment["images"]["intro_1641"]
            Set.blit(intro, (0, 0))
            name_next_part = "fork_1"
            return name_next_part

    def fork_1(self):    
        if self._count_motion <= 12000:
            self._count_motion += 20
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part
        if self._count_motion > 12000:
            self.events.append(EVENT_CHANGESCENE)
            self._count_motion = 1
            self._name_next_scene = "Main_screen"
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part
