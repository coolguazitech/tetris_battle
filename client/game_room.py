from scene import *
import pygame as pg
import random
import time
import db_utils

# ATTRIBUTES 
COLOR_THEME_BLUE = (0, 0, 242)
SIZE_BRICK = int(0.0334 * WIN_HEIGHT)

SIZE_MINISCORE = int(0.070 * WIN_HEIGHT)
POSITION_SCORE1 = (int(0.393 * WIN_WIDTH), int(0.620 * WIN_HEIGHT))
POSITION_SCORE2 = (int(0.894 * WIN_WIDTH), int(0.620 * WIN_HEIGHT))

POSITION_MINIBADGE1 = (int(0.393 * WIN_WIDTH), int(0.767 * WIN_HEIGHT))
POSITION_MINIBADGE2 = (int(0.894 * WIN_WIDTH), int(0.767 * WIN_HEIGHT))

SIZE_SPEED = int(0.080 * WIN_HEIGHT)
POSITION_SPEED1 = (int(0.180 * WIN_WIDTH), int(0.058 * WIN_HEIGHT))
POSITION_SPEED2 = (int(0.700 * WIN_WIDTH), int(0.058 * WIN_HEIGHT))

POOL_TOPLEFT1 = (int(0.0545 * WIN_WIDTH), int(0.238 * WIN_HEIGHT))
POOL_TOPLEFT2 = (int(0.5535 * WIN_WIDTH), int(0.238 * WIN_HEIGHT))
NEXT_TOPLEFT1 = (int(0.360 * WIN_WIDTH), int(0.282 * WIN_HEIGHT))
NEXT_TOPLEFT2 = (int(0.860 * WIN_WIDTH), int(0.282 * WIN_HEIGHT))

COLOR_FONT_DIALOGUE = (225, 225, 225)
SIZE_FONT_DIALOGUE = int(0.0420 * WIN_HEIGHT)

POSITION_OLD_BADGE = (int(0.465 * WIN_WIDTH), int(0.470 * WIN_HEIGHT))
POSITION_NEW_BADGE = (int(0.615 * WIN_WIDTH), int(0.470 * WIN_HEIGHT))

POSITION_OLD_SCORE = (int(0.465 * WIN_WIDTH), int(0.530 * WIN_HEIGHT))
POSITION_NEW_SCORE = (int(0.615 * WIN_WIDTH), int(0.530 * WIN_HEIGHT))


# GAME SETTING
PERIOD_MOTION_ELIMINATE = 1 # seconds
COUNT_MOTION_ELIMINATE = PERIOD_MOTION_ELIMINATE * Set.fps_server

class Game_room(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._rundown = {
            "init": self.init,
            "blit_background": self.blit_background,
            "blit_score": self.blit_score,
            "blit_badge": self.blit_badge,
            "blit_speed": self.blit_speed,
            "blit_dialogue_summary_and_get_reward": self.blit_dialogue_summary_and_get_reward,
            "blit_dialogue_confirm_leave": self.blit_dialogue_confirm_leave,
            "fork_1": self.fork_1,
            "fork_2": self.fork_2,
            "fork_3": self.fork_3
            }
        self._name_entrance = "blit_background"
        self._name_current_part = self._name_entrance
        self.__particales = [[random.randint(0, 9), random.randint(0, 19)] for _ in range(30)]

    def blit_background(self):
        BG_copy = self._equipment["images"]["BG_SCENE_Game_room"].copy()
        this_number = self._equipment["number"]

        # skip first data or skip if game is over
        if not self._equipment["game_property"]["pool1"] or not self._equipment["game_property"]["pool2"]:
            Set.blit(BG_copy, (0, 0))
            name_next_part = "blit_score"
            return name_next_part

        # draw elimination's motion  
        if this_number == 1:
            count1 = self._equipment["game_property"]["motion_eliminate1"][1]
            count2 = self._equipment["game_property"]["motion_eliminate2"][1]
        elif this_number == 2:
            count1 = self._equipment["game_property"]["motion_eliminate2"][1]
            count2 = self._equipment["game_property"]["motion_eliminate1"][1]
     
        if count1 >= 0:
            for i in range(10):
                if i == 0 or i == 9:
                    pos_x = POOL_TOPLEFT2[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + (count1 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK
                    if pos_y > POOL_TOPLEFT2[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 1 or i == 8:
                    pos_x = POOL_TOPLEFT2[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + (count1 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 1
                    if pos_y > POOL_TOPLEFT2[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 2 or i == 7:
                    pos_x = POOL_TOPLEFT2[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + (count1 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 2
                    if pos_y > POOL_TOPLEFT2[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 3 or i == 6:
                    pos_x = POOL_TOPLEFT2[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + (count1 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 3
                    if pos_y > POOL_TOPLEFT2[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 4 or i == 5:
                    pos_x = POOL_TOPLEFT2[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + (count1 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 3
                    if pos_y > POOL_TOPLEFT2[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)

            for particle in self.__particales:
                x, y = particle[0], particle[1]
                noise = random.randint(0, 20)
                possible_horizontal_motions = [1, -1] + [1] * max(int(4.5 - x), 0) + [-1] * max(int(x - 4.5), 0) \
                    + [1] * noise + [-1] * (20 - noise)
                noise = random.randint(0, 40)
                possible_vertical_motions = [1, -1] + [1] * max(int(9.5 - y), 0) + [-1] * max(int(y - 9.5), 0) \
                    + [1] * noise + [-1] * (40 - noise)
                next_x = particle[0] + random.choice(possible_horizontal_motions)
                next_y = particle[1] + random.choice(possible_vertical_motions)
                particle[0] = next_x
                particle[1] = next_y

            color = (
                255 * count1 // COUNT_MOTION_ELIMINATE,
                255 * count1 // COUNT_MOTION_ELIMINATE,
                225 * count1 // COUNT_MOTION_ELIMINATE
                )

            for x, y in self.__particales:
                if 0 <= x <= 9 and 0 <= y <= 19:
                    pos_x = POOL_TOPLEFT1[0] + x * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + y * SIZE_BRICK
                    pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)

        elif count2 >= 0:
            for i in range(10):
                if i == 0 or i == 9:
                    pos_x = POOL_TOPLEFT1[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + (count2 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK
                    if pos_y > POOL_TOPLEFT1[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 1 or i == 8:
                    pos_x = POOL_TOPLEFT1[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + (count2 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 1
                    if pos_y > POOL_TOPLEFT1[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 2 or i == 7:
                    pos_x = POOL_TOPLEFT1[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + (count2 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 2
                    if pos_y > POOL_TOPLEFT1[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 3 or i == 6:
                    pos_x = POOL_TOPLEFT1[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + (count2 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 3
                    if pos_y > POOL_TOPLEFT1[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)
                if i == 4 or i == 5:
                    pos_x = POOL_TOPLEFT1[0] + i * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + (count2 ** 6 * 20 // COUNT_MOTION_ELIMINATE ** 6) * SIZE_BRICK \
                        - SIZE_BRICK * 3
                    if pos_y > POOL_TOPLEFT1[1]:
                        pg.draw.rect(BG_copy, (255, 50, 50), [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)

            for particle in self.__particales:
                x, y = particle[0], particle[1]
                noise = random.randint(0, 20)
                possible_horizontal_motions = [1, -1] + [1] * max(int(4.5 - x), 0) + [-1] * max(int(x - 4.5), 0) \
                    + [1] * noise + [-1] * (20 - noise)
                noise = random.randint(0, 40)
                possible_vertical_motions = [1, -1] + [1] * max(int(9.5 - y), 0) + [-1] * max(int(y - 9.5), 0) \
                    + [1] * noise + [-1] * (40 - noise)
                next_x = particle[0] + random.choice(possible_horizontal_motions)
                next_y = particle[1] + random.choice(possible_vertical_motions)
                particle[0] = next_x
                particle[1] = next_y

            color = (
                255 * count2 // COUNT_MOTION_ELIMINATE,
                255 * count2 // COUNT_MOTION_ELIMINATE,
                225 * count2 // COUNT_MOTION_ELIMINATE
                )
            for x, y in self.__particales:
                if 0 <= x <= 9 and 0 <= y <= 19:
                    pos_x = POOL_TOPLEFT2[0] + x * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + y * SIZE_BRICK
                    pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK, SIZE_BRICK], 0)

        # draw pool's background
        for i in range(20):
            for j in range(10):
                color = (50 + i ** 2 // 8, 50 + i ** 2 // 8, 50 + i ** 2 // 8)
                pos_x = POOL_TOPLEFT1[0] + SIZE_BRICK // 10 + j * SIZE_BRICK
                pos_y = POOL_TOPLEFT1[1] + SIZE_BRICK // 10 + i * SIZE_BRICK
                pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)
                pos_x = POOL_TOPLEFT2[0] + SIZE_BRICK // 10 + j * SIZE_BRICK
                pos_y = POOL_TOPLEFT2[1] + SIZE_BRICK // 10 + i * SIZE_BRICK
                pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        # draw pool
        if this_number == 1:
            pool1 = self._equipment["game_property"]["pool1"]
            pool2 = self._equipment["game_property"]["pool2"]
        if this_number == 2:
            pool1 = self._equipment["game_property"]["pool2"]
            pool2 = self._equipment["game_property"]["pool1"]

        for i in range(20):
            for j in range(10):
                if pool1[i][j] != [0, 0, 0]:
                    color = tuple(pool1[i][j])
                    pos_x = POOL_TOPLEFT1[0] + SIZE_BRICK // 10 + j * SIZE_BRICK
                    pos_y = POOL_TOPLEFT1[1] + SIZE_BRICK // 10 + i * SIZE_BRICK
                    pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)
                if pool2[i][j] != [0, 0, 0]:
                    color = tuple(pool2[i][j])
                    pos_x = POOL_TOPLEFT2[0] + SIZE_BRICK // 10 + j * SIZE_BRICK
                    pos_y = POOL_TOPLEFT2[1] + SIZE_BRICK // 10 + i * SIZE_BRICK
                    pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        # draw cur_brick
        if this_number == 1:
            cur_brick1 = self._equipment["game_property"]["cur_brick1"]
            cur_brick2 = self._equipment["game_property"]["cur_brick2"]
        elif this_number == 2:
            cur_brick1 = self._equipment["game_property"]["cur_brick2"]
            cur_brick2 = self._equipment["game_property"]["cur_brick1"]

        for x, y in cur_brick1["position"]:
            if y >= 0:
                pos_x = POOL_TOPLEFT1[0] + SIZE_BRICK // 10 + x * SIZE_BRICK
                pos_y = POOL_TOPLEFT1[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
                color = tuple(cur_brick1["color"])
                pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        for x, y in cur_brick2["position"]:
            if y >= 0:
                pos_x = POOL_TOPLEFT2[0] + SIZE_BRICK // 10 + x * SIZE_BRICK
                pos_y = POOL_TOPLEFT2[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
                color = tuple(cur_brick2["color"])
                pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        # draw next
        if this_number == 1:
            position1 = self._equipment["game_property"]["queue_bricks1"][1]["position"]
            color1 = self._equipment["game_property"]["queue_bricks1"][1]["color"]
            type1 = self._equipment["game_property"]["queue_bricks1"][1]["type"]
            position2 = self._equipment["game_property"]["queue_bricks2"][1]["position"]
            color2 = self._equipment["game_property"]["queue_bricks2"][1]["color"]
            type2 = self._equipment["game_property"]["queue_bricks2"][1]["type"]
        elif this_number == 2:
            position1 = self._equipment["game_property"]["queue_bricks2"][1]["position"]
            color1 = self._equipment["game_property"]["queue_bricks2"][1]["color"]
            type1 = self._equipment["game_property"]["queue_bricks2"][1]["type"]
            position2 = self._equipment["game_property"]["queue_bricks1"][1]["position"]
            color2 = self._equipment["game_property"]["queue_bricks1"][1]["color"]
            type2 = self._equipment["game_property"]["queue_bricks1"][1]["type"]

        for x, y in position1:
            x -= 3
            y += 2
            if type1 == 3:
                pos_x = NEXT_TOPLEFT1[0] + SIZE_BRICK // 10 + x * SIZE_BRICK - SIZE_BRICK // 2
                pos_y = NEXT_TOPLEFT1[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
            elif type1 == 4:
                pos_x = NEXT_TOPLEFT1[0] + SIZE_BRICK // 10 + x * SIZE_BRICK - SIZE_BRICK // 2
                pos_y = NEXT_TOPLEFT1[1] + SIZE_BRICK // 10 + y * SIZE_BRICK - SIZE_BRICK // 2
            else:
                pos_x = NEXT_TOPLEFT1[0] + SIZE_BRICK // 10 + x * SIZE_BRICK
                pos_y = NEXT_TOPLEFT1[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
            color = tuple(color1)
            pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        for x, y in position2:
            x -= 3
            y += 2
            if type2 == 3:
                pos_x = NEXT_TOPLEFT2[0] + SIZE_BRICK // 10 + x * SIZE_BRICK - SIZE_BRICK // 2
                pos_y = NEXT_TOPLEFT2[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
            elif type2 == 4:
                pos_x = NEXT_TOPLEFT2[0] + SIZE_BRICK // 10 + x * SIZE_BRICK - SIZE_BRICK // 2
                pos_y = NEXT_TOPLEFT2[1] + SIZE_BRICK // 10 + y * SIZE_BRICK - SIZE_BRICK // 2
            else:
                pos_x = NEXT_TOPLEFT2[0] + SIZE_BRICK // 10 + x * SIZE_BRICK
                pos_y = NEXT_TOPLEFT2[1] + SIZE_BRICK // 10 + y * SIZE_BRICK
            color = tuple(color2)
            pg.draw.rect(BG_copy, color, [pos_x, pos_y, SIZE_BRICK * 8 // 10, SIZE_BRICK * 8 // 10], 0)

        Set.blit(BG_copy, (0, 0))
        name_next_part = "blit_score"
        return name_next_part

    def blit_score(self):
        my_number = self._equipment["number"]
        if my_number == 1:
            score1 = self._equipment["game_property"]["score1"]
            text_score1 = Set.get_text(str(score1), SIZE_MINISCORE, COLOR_THEME_BLUE, COLOR_WHITE)
            text_score1.set_colorkey(COLOR_WHITE)
            Set.blit(text_score1, POSITION_SCORE1, mode="center")
            score2 = self._equipment["game_property"]["score2"]
            text_score2 = Set.get_text(str(score2), SIZE_MINISCORE, COLOR_WHITE, bg_color=(1, 0, 0))
            text_score2.set_colorkey((1, 0, 0))
            Set.blit(text_score2, POSITION_SCORE2, mode="center")
        else:
            score1 = self._equipment["game_property"]["score2"]
            text_score1 = Set.get_text(str(score1), SIZE_MINISCORE, COLOR_THEME_BLUE, COLOR_WHITE)
            text_score1.set_colorkey(COLOR_WHITE)
            Set.blit(text_score1, POSITION_SCORE1, mode="center")
            score2 = self._equipment["game_property"]["score1"]
            text_score2 = Set.get_text(str(score2), SIZE_MINISCORE, COLOR_WHITE, bg_color=(1, 0, 0))
            text_score2.set_colorkey((1, 0, 0))
            Set.blit(text_score2, POSITION_SCORE2, mode="center")
        name_next_part = "blit_badge"
        return name_next_part

    def blit_badge(self):
        my_number = self._equipment["number"]
        if my_number == 1:
            badge1 = self._equipment["game_property"]["badge1"]
            rank1, level1 = badge1[0], badge1[1]
            name_badge1 = "minibadge_" + rank1 + "_" + level1
            image_badge1 = self._equipment["images"][name_badge1]
            image_badge1.set_colorkey(COLOR_WHITE)
            Set.blit(image_badge1, POSITION_MINIBADGE1, mode="center")
            badge2 = self._equipment["game_property"]["badge2"]
            rank2, level2 = badge2[0], badge2[1]
            name_badge2 = "minibadge_" + rank2 + "_" + level2
            image_badge2 = self._equipment["images"][name_badge2]
            image_badge2.set_colorkey(COLOR_WHITE)
            Set.blit(image_badge2, POSITION_MINIBADGE2, mode="center")
        else:
            badge1 = self._equipment["game_property"]["badge2"]
            rank1, level1 = badge1[0], badge1[1]
            name_badge1 = "minibadge_" + rank1 + "_" + level1
            image_badge1 = self._equipment["images"][name_badge1]
            image_badge1.set_colorkey(COLOR_WHITE)
            Set.blit(image_badge1, POSITION_MINIBADGE1, mode="center")
            badge2 = self._equipment["game_property"]["badge1"]
            rank2, level2 = badge2[0], badge2[1]
            name_badge2 = "minibadge_" + rank2 + "_" + level2
            image_badge2 = self._equipment["images"][name_badge2]
            image_badge2.set_colorkey(COLOR_WHITE)
            Set.blit(image_badge2, POSITION_MINIBADGE2, mode="center")      
        name_next_part = "blit_speed"
        return name_next_part

    def blit_speed(self):
        my_number = self._equipment["number"]
        if my_number == 1:
            speed1 = self._equipment["game_property"]["speed1"]
            speed1 = int(0.2 * speed1)
            text_speed1 = Set.get_text(str(speed1), SIZE_SPEED, COLOR_THEME_BLUE)
            text_speed1.set_colorkey(COLOR_WHITE)
            Set.blit(text_speed1, POSITION_SPEED1)        
            speed2 = self._equipment["game_property"]["speed2"]
            speed2 = int(0.2 * speed2)
            text_speed2 = Set.get_text(str(speed2), SIZE_SPEED, COLOR_WHITE, bg_color=(1, 0, 0))
            text_speed2.set_colorkey((1, 0, 0))
            Set.blit(text_speed2, POSITION_SPEED2)
        else:
            speed1 = self._equipment["game_property"]["speed2"]
            speed1 = int(0.2 * speed1)
            text_speed1 = Set.get_text(str(speed1), SIZE_SPEED, COLOR_THEME_BLUE)
            text_speed1.set_colorkey(COLOR_WHITE)
            Set.blit(text_speed1, POSITION_SPEED1)        
            speed2 = self._equipment["game_property"]["speed1"]
            speed2 = int(0.2 * speed2)
            text_speed2 = Set.get_text(str(speed2), SIZE_SPEED, COLOR_WHITE, bg_color=(1, 0, 0))
            text_speed2.set_colorkey((1, 0, 0))
            Set.blit(text_speed2, POSITION_SPEED2)
        name_next_part = "fork_1"
        return name_next_part

    def fork_1(self):
        if self._equipment["network"]:
            if ERROR_TIMEOUT in self._equipment["network"].events:
                self.events.append(EVENT_CHANGESCENE)
                self._name_next_scene = "Main_screen"
                name_next_part = MESSAGE_ENDSCENE
                return name_next_part

        if MESSAGE_PLAYER1WIN in self._equipment["network"].events \
            or MESSAGE_PLAYER2WIN in self._equipment["network"].events:
            if MESSAGE_PLAYER1WIN in self._equipment["network"].events:
                self.events.append(MESSAGE_PLAYER1WIN)
            else:
                self.events.append(MESSAGE_PLAYER2WIN) 
            for i in range(1, 3):
                self._equipment["network"].events = list(filter(
                    (eval(f"MESSAGE_PLAYER{i}WIN")).__ne__, 
                    self._equipment["network"].events
                    ))
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part

        if MESSAGE_PLAYER1WIN in self.events or MESSAGE_PLAYER2WIN in self.events:
            name_next_part = "blit_dialogue_summary_and_get_reward"
            return name_next_part

        if len(self.events) == 0 and self._equipment["collection_input"]["q"]:
            self.events.append(EVENT_CONFIRMLEAVE)
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part

        if EVENT_CONFIRMLEAVE in self.events:
            name_next_part = "blit_dialogue_confirm_leave"
            return name_next_part

        # unexpected error
        if self._equipment["network"]:
            if not self._equipment['network'].connected:
                self.events.append(EVENT_CHANGESCENE)
                self._name_next_scene = "Main_screen"
                name_next_part = MESSAGE_ENDSCENE
                return name_next_part

        name_next_part = MESSAGE_ENDSCENE
        return name_next_part

    def blit_dialogue_summary_and_get_reward(self):
        this_number = self._equipment["number"]
        this_win = True if eval(f"MESSAGE_PLAYER{this_number}WIN") in self.events else False
        enemy_number = 1 if this_number == 2 else 2
        this_rank = self._equipment["game_property"][f"badge{this_number}"][0]
        this_level = int(self._equipment["game_property"][f"badge{this_number}"][1])
        old_score = this_score = self._equipment["game_property"][f"score{this_number}"]
        old_badge = this_rank + str(this_level)
        enemy_rank = self._equipment["game_property"][f"badge{enemy_number}"][0]
        enemy_level = int(self._equipment["game_property"][f"badge{enemy_number}"][1])
        rank_map = {'D': 1, 'C': 2, 'B': 3, 'A': 4, 'S': 5}
        inv_rank_map = {v: k for k, v in rank_map.items()}
        reward_points = (rank_map[enemy_rank] * 4 + enemy_level) - (rank_map[this_rank] * 4 + this_level) + 19 # 0 ~ 38
        new_score = raw_score = this_score if this_rank == 'S' and this_level == 3 else this_score + reward_points
        new_badge = this_rank + str(this_level) 

        if raw_score >= 100:
            if this_rank == 'S' and this_level == 2:
                new_rank = 'S'
                new_level = 3
                new_score = 0
            else:
                new_score = raw_score - 100
                raw_lavel = this_level + 1
                if raw_lavel == 4:
                    new_level = 0
                    new_rank = inv_rank_map[rank_map[this_rank] + 1]
                else:
                    new_level = raw_lavel
                    new_rank = this_rank
            new_badge = new_rank + str(new_level)

        if this_win:
            # update database
            new_dict_info = {
                "BADGE": new_badge,
                "SCORE": new_score,  
                "DATE": time.ctime(),
            }   
            db_utils.update(1, new_dict_info)

            # blit summary
            image_dialogue_summary_win = self._equipment["images"]["DIALOGUE_summary_win"]
            image_dialogue_summary_win.set_colorkey(COLOR_WHITE)
            Set.blit(image_dialogue_summary_win, POSITION_DIALOGUE, mode="center")
            old_badge = " ".join(old_badge)
            new_badge = " ".join(new_badge)
            text_old_badge = Set.get_text(old_badge, SIZE_FONT_DIALOGUE, COLOR_FONT_DIALOGUE, COLOR_WHITE)
            text_old_badge.set_colorkey(COLOR_WHITE)
            Set.blit(text_old_badge, POSITION_OLD_BADGE, mode="center")
            text_old_score = Set.get_text(str(old_score), SIZE_FONT_DIALOGUE, COLOR_FONT_DIALOGUE, COLOR_WHITE)
            text_old_score.set_colorkey(COLOR_WHITE)
            Set.blit(text_old_score, POSITION_OLD_SCORE, mode="center")
            text_new_badge = Set.get_text(new_badge, SIZE_FONT_DIALOGUE, COLOR_FONT_DIALOGUE, COLOR_WHITE)
            text_new_badge.set_colorkey(COLOR_WHITE)
            Set.blit(text_new_badge, POSITION_NEW_BADGE, mode="center")
            text_new_score = Set.get_text(str(new_score), SIZE_FONT_DIALOGUE, COLOR_FONT_DIALOGUE, COLOR_WHITE)
            text_new_score.set_colorkey(COLOR_WHITE)
            Set.blit(text_new_score, POSITION_NEW_SCORE, mode="center")
        else:
            # blit summary
            image_dialogue_summary_lose = self._equipment["images"]["DIALOGUE_summary_lose"]
            image_dialogue_summary_lose.set_colorkey(COLOR_WHITE)
            Set.blit(image_dialogue_summary_lose, POSITION_DIALOGUE, mode="center")

        name_next_part = "fork_3"
        return name_next_part

    def fork_3(self):
        if self._equipment["collection_input"]["SPACE"]:
            self._name_next_scene = "Main_screen"
            self.events.append(EVENT_CHANGESCENE)
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part
        name_next_part = MESSAGE_ENDSCENE
        return name_next_part

    def blit_dialogue_confirm_leave(self):
        image_dialogue_confirm_leave = self._equipment["images"]["DIALOGUE_confirm_leave"]
        image_dialogue_confirm_leave.set_colorkey(COLOR_WHITE)
        Set.blit(image_dialogue_confirm_leave, POSITION_DIALOGUE, mode="center")
        name_next_part = "fork_2"
        return name_next_part

    def fork_2(self):
        if EVENT_CONFIRMLEAVE in self.events and self._equipment["collection_input"]["b"]:
            self.events = list(filter((EVENT_CONFIRMLEAVE).__ne__, self.events))
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part

        if EVENT_CONFIRMLEAVE in self.events and self._equipment["collection_input"]["q"]:
            self.events = list(filter((EVENT_CONFIRMLEAVE).__ne__, self.events))
            self._equipment["network"].disconnect()
            self.events.append(EVENT_CHANGESCENE)
            self._name_next_scene = "Main_screen"
            name_next_part = MESSAGE_ENDSCENE
            return name_next_part

        name_next_part = MESSAGE_ENDSCENE
        return name_next_part

