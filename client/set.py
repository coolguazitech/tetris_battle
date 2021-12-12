import pygame as pg
import db_utils

# WINDOW
WIN_HEIGHT = 600
WIN_WIDTH = 900

# GAME 
GAME_FPS = 60
GAME_NAME = "Tetris Battle"

# POOL
POOL_HEIGHT = 20
POOL_WIDTH = 10

# BRICK
BRICK_SIZE = 20

class Set:
    # INITIALIZATION
    pg.init()
    pg.font.init()

    # WINDOW
    window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pg.display.set_caption(GAME_NAME)

    def __init__(self, version):
        self._scenes = {}
        self._name_current_scene = None
        self._run = True
        self._clock = pg.time.Clock()
        self._version = version
        self._equipment = {
            "images": {
                "BG_SCENE_Main_screen": pg.image.load('images/BG_SCENE_Main_screen.png').convert(),
                "BG_SCENE_Game_room": pg.image.load('images/BG_SCENE_Game_room.png').convert(),
                "DIALOGUE_queue": pg.image.load('images/DIALOGUE_queue.png').convert(),
                "DIALOGUE_error_version": pg.image.load('images/DIALOGUE_error_version.png').convert(),
                "DIALOGUE_error_timeout": pg.image.load('images/DIALOGUE_error_timeout.png').convert(),
                "badge_D_0": pg.image.load('images/badge_D_0.png').convert(),
                "badge_D_1": pg.image.load('images/badge_D_1.png').convert(),
                "badge_D_2": pg.image.load('images/badge_D_2.png').convert(),
                "badge_D_3": pg.image.load('images/badge_D_3.png').convert(),
                "badge_C_0": pg.image.load('images/badge_C_0.png').convert(),
                "badge_C_1": pg.image.load('images/badge_C_1.png').convert(),
                "badge_C_2": pg.image.load('images/badge_C_2.png').convert(),
                "badge_C_3": pg.image.load('images/badge_C_3.png').convert(),
                "badge_B_0": pg.image.load('images/badge_B_0.png').convert(),
                "badge_B_1": pg.image.load('images/badge_B_1.png').convert(),
                "badge_B_2": pg.image.load('images/badge_B_2.png').convert(),
                "badge_B_3": pg.image.load('images/badge_B_3.png').convert(),
                "badge_A_0": pg.image.load('images/badge_A_0.png').convert(),
                "badge_A_1": pg.image.load('images/badge_A_1.png').convert(),
                "badge_A_2": pg.image.load('images/badge_A_2.png').convert(),
                "badge_A_3": pg.image.load('images/badge_A_3.png').convert(),
                "badge_S_0": pg.image.load('images/badge_S_0.png').convert(),
                "badge_S_1": pg.image.load('images/badge_S_1.png').convert(),
                "badge_S_2": pg.image.load('images/badge_S_2.png').convert(),
                "badge_S_3": pg.image.load('images/badge_S_3.png').convert(),
                "minibadge_D_0": pg.image.load('images/minibadge_D_0.png').convert(),
                "minibadge_D_1": pg.image.load('images/minibadge_D_1.png').convert(),
                "minibadge_D_2": pg.image.load('images/minibadge_D_2.png').convert(),
                "minibadge_D_3": pg.image.load('images/minibadge_D_3.png').convert(),
                "minibadge_C_0": pg.image.load('images/minibadge_C_0.png').convert(),
                "minibadge_C_1": pg.image.load('images/minibadge_C_1.png').convert(),
                "minibadge_C_2": pg.image.load('images/minibadge_C_2.png').convert(),
                "minibadge_C_3": pg.image.load('images/minibadge_C_3.png').convert(),
                "minibadge_B_0": pg.image.load('images/minibadge_B_0.png').convert(),
                "minibadge_B_1": pg.image.load('images/minibadge_B_1.png').convert(),
                "minibadge_B_2": pg.image.load('images/minibadge_B_2.png').convert(),
                "minibadge_B_3": pg.image.load('images/minibadge_B_3.png').convert(),
                "minibadge_A_0": pg.image.load('images/minibadge_A_0.png').convert(),
                "minibadge_A_1": pg.image.load('images/minibadge_A_1.png').convert(),
                "minibadge_A_2": pg.image.load('images/minibadge_A_2.png').convert(),
                "minibadge_A_3": pg.image.load('images/minibadge_A_3.png').convert(),
                "minibadge_S_0": pg.image.load('images/minibadge_S_0.png').convert(),
                "minibadge_S_1": pg.image.load('images/minibadge_S_1.png').convert(),
                "minibadge_S_2": pg.image.load('images/minibadge_S_2.png').convert(),
                "minibadge_S_3": pg.image.load('images/minibadge_S_3.png').convert(),
            },
            "network": None,
            "public_info": {
                "score": 0,
                "badge": "D0",
                "tags": []
            },
            "collection_input": {
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "q" : 0
            },
            "game_property": {
                "queue_bricks1": None,
                "cur_brick1": None,
                "pool1": None,
                "motion_eliminate1": None,
                "speed1": None,
                "score1": 0,
                "badge1": "D0",
                "trace_code1": 0,
                "queue_bricks2": None,
                "cur_brick2": None,
                "pool2": None,
                "motion_eliminate2": None,
                "speed2": None, 
                "score2": 0,
                "badge2": "D0",
                "trace_code2": None,
                "tags": []
            }
        }
        
    def _switch_to_scene(self, name_scene):
        self._name_current_scene = name_scene

    def register_scene(self, scene):
        new_scene = {scene.name: scene}
        if not self._scenes:
            self._name_current_scene = scene.name
        self._scenes.update(new_scene)

    @staticmethod
    def blit(surface, position, mode="top_left"):
        if mode == "top_left":
            pg.Surface.blit(Set.window, surface, position)
        if mode == "center":
            rect = surface.get_rect()
            rect.center = position
            pg.Surface.blit(Set.window, surface, rect.topleft)

    @staticmethod
    def get_text(text, size, color, bg_color=(255, 255, 255), font="Arial Black"):
        my_font = pg.font.SysFont(font, size)
        return my_font.render(text, True, color, bg_color)


    def _collect_input(self):
        data = self._equipment["collection_input"]
        data.update({
                "LEFT": 0,
                "RIGHT": 0,
                "DOWN": 0,
                "SPACE": 0,
                "q" : 0
            })

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._run = False 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    data["q"] = 1
                if event.key == pg.K_SPACE:
                    data["SPACE"] = 1

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            data["LEFT"] = 1
        if keys[pg.K_RIGHT]:
            data["RIGHT"] = 1
        if keys[pg.K_DOWN]:
            data["DOWN"] = 1

    def _update_rank(self):
        dict_info = db_utils.fetch(1)
        self._equipment["public_info"]["score"] = dict_info["SCORE"]
        self._equipment["public_info"]["badge"] = dict_info["RANK"]

    def _drop_into_mailbox(self):
        if self._equipment["network"]:
            if self._equipment["network"].connected:
                for direction in ["LEFT", "RIGHT", "DOWN", "SPACE"]:
                    self._equipment["network"].mailbox[1][direction] = self._equipment["collection_input"][direction]
                self._equipment["network"].mailbox[1]["score"] = self._equipment["public_info"]["score"]
                self._equipment["network"].mailbox[1]["badge"] = self._equipment["public_info"]["badge"]
                self._equipment["network"].mailbox[1]["tags"].extend(self._equipment["public_info"]["tags"])

    def _pick_up_from_mailbox(self):
        if self._equipment["network"]:
            if self._equipment["network"].connected:
                self._equipment["game_property"].update(self._equipment["network"].mailbox[2])

    def _check_network(self):
        if self._equipment["network"]:
            if not self._equipment["network"].connected:
                self._equipment["game_property"].update(
                    {
                        "queue_bricks1": None,
                        "cur_brick1": None,
                        "pool1": None,
                        "motion_eliminate1": None,
                        "speed1": None,
                        "score1": 0,
                        "badge1": "D0",
                        "trace_code1": 0,
                        "queue_bricks2": None,
                        "cur_brick2": None,
                        "pool2": None,
                        "motion_eliminate2": None,
                        "speed2": None, 
                        "score2": 0,
                        "badge2": "D0",
                        "trace_code2": None,
                        "tags": []
                    }
                )

    def run(self):
        while self._run:
            self._clock.tick(GAME_FPS)

            self._check_network()
            self._collect_input()
            self._drop_into_mailbox()
            self._pick_up_from_mailbox()

            name_next_scene = self._scenes[self._name_current_scene](self._equipment)

            self._switch_to_scene(name_next_scene)

            pg.display.flip()
        
        if self._equipment["network"]:
            if self._equipment["network"].connected:
                self._equipment["network"].disconnect()
        pg.quit()

