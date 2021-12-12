import time
from brick import Brick
import json
import copy

# PROTOCOL MESSAGE
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"
MESSAGE_STARTGAME = "$STARTGAME"
MESSAGE_STARTGAME1 = "$STARTGAME1"
MESSAGE_STARTGAME2 = "$STARTGAME2"
MESSAGES = [
    MESSAGE_ZOMBIE,
    MESSAGE_PLAYER1WIN, 
    MESSAGE_PLAYER2WIN,
    MESSAGE_STARTGAME1,
    MESSAGE_STARTGAME2
    ]

# POOL SIZE
POOL_HEIGHT = 20
POOL_WIDTH = 10

# PROCEDURE TIME
PERIOD_SPEED_1_PER_MOVE = 3 # seconds
PERIOD_PER_SPEED = 30 # seconds

# COUNT MOTION
COUNT_MOTION_ELIMINATE = 3 # seconds

# GAME SETTING
GAME_FPS = 60

class Game:
    def __init__(self, mailbox):
        self._game_property = mailbox
        self._queue_bricks1 = None
        self._cur_brick1 = None
        self._pool1 = None
        self._queue_bricks2 = None
        self._cur_brick2 = None
        self._pool2 = None
        self._count_game = 0
        self._count_move1 = 0
        self._count_move2 = 0
        self._motion_eliminate1 = None
        self._motion_eliminate2 = None
        self._speed1 = 1
        self._speed2 = 1
        self._score1 = 0
        self._score2 = 0
        self._badge1 = "D0"
        self._badge2 = "D0"
        self._trace_code1 = 0
        self._trace_code2 = 0
        self._tags = []
        self._run = False
        self._init_game()

    def _member_selector(*obj_names):
        """
        select objects from whoever you want, input which player is in the kwargs of decorated
        function when invoking.
        """
        def decorator(func):
            def wrapper(*func_args, **func_kwargs):
                for name in obj_names:
                    func_kwargs[name] = f"self._{name}{func_kwargs['player']}"
                func(*func_args, **func_kwargs)
            return wrapper
        return decorator

    def main_loop(self):
        while self._run:
            time.sleep(1.0 / GAME_FPS)

            self._check_state()
            if MESSAGE_PLAYER1WIN in self._tags or MESSAGE_PLAYER2WIN in self._tags:
                continue

            data_players = self._pick_up_from_mailbox()

            for i, data in enumerate(data_players):
                if self._count_game % 3 == 0:
                    if data["LEFT"] > data["RIGHT"] and self._check_can_move_to("LEFT", player=(i + 1)):
                        exec(f"self._cur_brick{i + 1}.move('LEFT')")
                    elif data["LEFT"] < data["RIGHT"] and self._check_can_move_to("RIGHT", player=(i + 1)):
                        exec(f"self._cur_brick{i + 1}.move('RIGHT')")
                if data["DOWN"]:
                    exec(f"self._count_move{i + 1} -= (GAME_FPS * PERIOD_SPEED_1_PER_MOVE) * (0.95 ** self._speed{i + 1}) * 0.3")
                if data["SPACE"]:
                    if self._check_can_rotate(player=(i + 1))[0]:
                        exec(f"self._cur_brick{i + 1}.rotate(self._check_can_rotate(player=(i + 1))[1])")
                exec(f"self._trace_code{i + 1} = data['trace_code']")
                exec(f"self._score{i + 1} = data['score']")
                exec(f"self._badge{i + 1} = data['badge']")

            for i in range(1, 3):
                if eval(f"self._trace_code{i}") != 0:
                    self._tags = list(filter(
                        (eval(f"MESSAGE_STARTGAME{i}")).__ne__, 
                        self._tags
                        ))

            for i in range(1, 3):
                self._check_eliminate(player=i)
                self._check_count_move(player=i)

            self._update_counters()
            self._update_motions()
            self._check_speed_up()
            self._drop_into_mailbox()

    def _init_game(self):
        for i in range(1, 3):
            exec(f"self._queue_bricks{i} = [Brick() for _ in range(4)]")
            exec(f"self._cur_brick{i} = self._queue_bricks{i}[0]")
            exec(f"self._pool{i} = [[[0, 0, 0] for _ in range(POOL_WIDTH)] for _ in range(POOL_HEIGHT)]")
            exec(f"self._motion_eliminate{i} = [0, 0]")
            exec(f"self._speed{i} = 1")
            exec(f"self._trace_code{i} = 0")
            self._reset_count_move(player=i)
        self._count_game = 0
        self._run = True
        self._tags.extend([MESSAGE_STARTGAME1, MESSAGE_STARTGAME2])
        self._drop_into_mailbox()

    def _check_state(self):
        if not MESSAGE_ZOMBIE in self._game_property[1]["tags"] and \
            not MESSAGE_ZOMBIE in self._game_property[2]["tags"]:
            self._run = False

    def _pick_up_from_mailbox(self):
        return self._game_property[1], self._game_property[2]

    @_member_selector("pool", "cur_brick")
    def _check_can_move_to(self, direction, **func_kwargs):
        pool = eval(func_kwargs["pool"])
        cur_brick = eval(func_kwargs["cur_brick"])

        old_position = copy.deepcopy(cur_brick.position)
        cur_brick.move(direction)
        new_position = cur_brick.position
        for x, y in new_position:
            if x < 0 or x > 9 or y > 19:
                cur_brick.position = old_position
                return False
            if y >= 0:
                if pool[y][x] != [0, 0, 0]:
                    cur_brick.position = old_position
                    return False
        cur_brick.position = old_position
        return True

    @_member_selector("pool", "cur_brick")
    def _check_can_rotate(self, **func_kwargs):
        pool = eval(func_kwargs["pool"])
        cur_brick = eval(func_kwargs["cur_brick"])
        can = False
        shift = -1
        for i in range(4):
            old_position = copy.deepcopy(cur_brick.position)
            old_state = cur_brick.state
            cur_brick.rotate(i)
            new_position = cur_brick.position
            count = 0
            for x, y in new_position:
                if x < 0 or x > 9 or y > 19:
                    cur_brick.position = old_position
                    cur_brick.state = old_state
                    break
                if y >= 0:
                    if pool[y][x] != [0, 0, 0]:
                        cur_brick.position = old_position
                        cur_brick.state = old_state
                        break
                count += 1
            if count == 4:
                can = True
                shift = i
                cur_brick.position = old_position
                cur_brick.state = old_state
                break
        return can, shift

    @_member_selector("count_move", "cur_brick")
    def _check_count_move(self, **func_kwargs):
        count_move = eval(func_kwargs["count_move"])
        cur_brick = eval(func_kwargs["cur_brick"])
        if count_move < 0:
            if self._check_can_move_to("DOWN", player=func_kwargs["player"]):
                self._reset_count_move(player=func_kwargs["player"])
                cur_brick.move("DOWN")
            else:
                if max(cur_brick.position, key=lambda x: x[1])[1] < 0:
                    if func_kwargs["player"] == 1:
                        self._tags.append(MESSAGE_PLAYER2WIN)
                    else:
                        self._tags.append(MESSAGE_PLAYER1WIN)
                else:
                    self._reset_count_move(player=func_kwargs["player"])
                    self._update_pool(player=func_kwargs["player"])
                    self._reset_bricks(player=func_kwargs["player"])

    @_member_selector("count_move", "speed")
    def _reset_count_move(self, **func_kwargs):
        exec("%s = %d" % (func_kwargs["count_move"], (GAME_FPS * PERIOD_SPEED_1_PER_MOVE) * (0.95 ** eval(func_kwargs["speed"]))))

    @_member_selector("motion_eliminate")
    def _reset_motion_eliminate(self, num_lines, **func_kwargs):
        motion_eliminate = eval(func_kwargs["motion_eliminate"])
        motion_eliminate[0] = num_lines
        motion_eliminate[1] = COUNT_MOTION_ELIMINATE * GAME_FPS

    @_member_selector("pool", "cur_brick")
    def _update_pool(self, **func_kwargs):
        pool = eval(func_kwargs["pool"])
        cur_brick = eval(func_kwargs["cur_brick"])

        for x, y in cur_brick.position:
            if y >= 0:
                pool[y][x] = cur_brick.color[:]

    @_member_selector("queue_bricks", "cur_brick")
    def _reset_bricks(self, **func_kwargs):
        queue_bricks = eval(func_kwargs["queue_bricks"])
        queue_bricks.pop(0)
        queue_bricks.append(Brick())
        exec("%s = %s" % (func_kwargs["cur_brick"], "queue_bricks[0]"))


    def _update_counters(self):
        self._count_game += 1
        self._count_move1 -= 1
        self._count_move2 -= 1

    def _update_motions(self):
        self._motion_eliminate1[1] -= 1
        self._motion_eliminate2[1] -= 1

    def _check_speed_up(self):
        if self._count_game % (GAME_FPS * PERIOD_SPEED_1_PER_MOVE) == 0:
            for i in range(1, 3):
                self._speed_up(1, player=i)

    @_member_selector("speed")
    def _speed_up(self, count, **func_kwargs):
        speed = eval(func_kwargs["speed"])
        speed = min(speed + count, 100)

    def _drop_into_mailbox(self):
        for i in range(1, 3):
            exec(f"queue_bricks{i} = [brick._get_public_member_dict() for brick in self._queue_bricks{i}]")
            exec(f"cur_brick{i} = self._cur_brick{i}._get_public_member_dict()")
            exec(f"pool{i} = self._pool{i}")
            exec(f"motion_eliminate{i} = self._motion_eliminate{i}")
            exec(f"speed{i} = self._speed{i}")
            exec(f"score{i} = self._score{i}")
            exec(f"badge{i} = self._badge{i}")
            exec(f"trace_code{i} = self._trace_code{i}")
        
        dict_game_property = {
            "queue_bricks1": eval("queue_bricks1"),
            "cur_brick1": eval("cur_brick1"),
            "pool1": eval("pool1"),
            "motion_eliminate1": eval("motion_eliminate1"),
            "speed1": eval("speed1"),
            "score1": eval("score1"),
            "badge1": eval("badge1"),
            "trace_code1": eval("trace_code1"),
            "queue_bricks2": eval("queue_bricks2"),
            "cur_brick2": eval("cur_brick2"),
            "pool2": eval("pool2"),
            "motion_eliminate2": eval("motion_eliminate2"),
            "speed2": eval("speed2"),
            "score2": eval("score2"),
            "badge2": eval("badge2"),
            "trace_code2": eval("trace_code2"),
            "tags": self._tags
            }

        self._game_property[3].update(dict_game_property)

    @_member_selector("pool")
    def _check_eliminate(self, **func_kwargs):
        pool = eval(func_kwargs["pool"])
        cur_row = POOL_HEIGHT - 1
        total_lines = 0

        while cur_row >= 0:
            count = 0
            for i in range(POOL_WIDTH):
                if pool[cur_row][i] == [0, 0, 0]:
                    break
                else:
                    count += 1
            if count == POOL_WIDTH:
                total_lines += 1
                for j in range(cur_row - 1, -1, -1):
                    for k in range(POOL_WIDTH):
                        pool[j + 1][k] = pool[j][k][:]
                for col in range(POOL_WIDTH):
                    pool[0][col] = [0, 0, 0]
            else:
                cur_row -= 1

        if total_lines == 1:
            self._reset_motion_eliminate(total_lines, player=func_kwargs["player"])
            if func_kwargs["player"] == 1:
                self._speed_up(1, player=2)
            elif func_kwargs["player"] == 2:
                self._speed_up(1, player=1)
        elif total_lines == 2:
            self._reset_motion_eliminate(total_lines, player=func_kwargs["player"])
            if func_kwargs["player"] == 1:
                self._speed_up(2, player=2)
            elif func_kwargs["player"] == 2:
                self._speed_up(2, player=1)
        elif total_lines == 3:
            self._reset_motion_eliminate(total_lines, player=func_kwargs["player"])
            if func_kwargs["player"] == 1:
                self._speed_up(4, player=2)
            elif func_kwargs["player"] == 2:
                self._speed_up(4, player=1)
        elif total_lines == 4:
            self._reset_motion_eliminate(total_lines, player=func_kwargs["player"])
            if func_kwargs["player"] == 1:
                self._speed_up(8, player=2)
            elif func_kwargs["player"] == 2:
                self._speed_up(8, player=1)
        







