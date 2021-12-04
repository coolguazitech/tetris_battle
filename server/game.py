import time
from brick import Brick
import json
import copy

# PROTOCOL MESSAGE
MESSAGE_DISCONNECT = "$DISCONNECT"
MESSAGE_ZOMBIE = "$ZOMBIE"
MESSAGE_GREETING = "$GREETING"
MESSAGE_DELIVERY = "$DELIVERY"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"

# POOL SIZE
POOL_HEIGHT = 20
POOL_WIDTH = 10

# PROCEDURE TIME
PERIOD_SPEED_1_PER_MOVE = 3
PERIOD_PER_SPEED = 30


class Game:
    def __init__(self, FPS, data):
        self._FPS = FPS
        self._data = data
        self._queue_bricks1 = None
        self._cur_brick1 = None
        self._pool1 = None
        self._queue_bricks2 = None
        self._cur_brick2 = None
        self._pool2 = None
        self._count_game = 0
        self._count_move1 = 0
        self._count_move2 = 0
        self._speed1 = 1
        self._speed2 = 1
        self._run = False
        self._init_game()

    def _member_selector(*obj_names):
        """select objects from whoever you want"""
        def decorator(func):
            def wrapper(*func_args, **func_kwargs):
                for name in obj_names:
                    func_kwargs[name] = f"self._{name}{func_kwargs['player']}"
                func(*func_args, **func_kwargs)
            return wrapper
        return decorator

    def main_loop(self):
        while self._run:
            self._check_state()
            if self._data[3] == MESSAGE_PLAYER1WIN or self._data[3] == MESSAGE_PLAYER2WIN:
                continue
            time.sleep(1.0 / self._FPS)

            data_players = self._pick_up_from_mailbox()
            for i, data in enumerate(data_players):
                if data["LEFT"] > data["RIGHT"] and self._check_can_move_to("LEFT", player=(i + 1)):
                    exec(f"self._cur_brick{i + 1}.move('LEFT')")
                elif data["LEFT"] < data["RIGHT"] and self._check_can_move_to("RIGHT", player=(i + 1)):
                    exec(f"self._cur_brick{i + 1}.move('RIGHT')")
                if data["DOWN"]:
                    exec(f"self._count_move{i + 1} -= (self._FPS * PERIOD_SPEED_1_PER_MOVE) * (0.95 ** self._speed{i + 1}) * 0.5")
                if data["SPACE"]:
                    if self._check_can_transform(player=(i + 1))[0]:
                        exec(f"self._cur_brick{i + 1}.transform(self._check_can_transform(player=(i + 1))[1])")


            self._check_count_move(player=1)
            self._check_count_move(player=2)
            self._update_counters()
            self._check_speed_up()
            self._drop_into_mailbox()

    def _init_game(self):
        for i in range(1, 3):
            exec(f"self._queue_bricks{i} = [Brick() for _ in range(4)]")
            exec(f"self._cur_brick{i} = self._queue_bricks{i}[0]")
            exec(f"self._pool{i} = [[[0, 0, 0] for _ in range(POOL_WIDTH)] for _ in range(POOL_HEIGHT)]")
        self._speed1 = 1
        self._speed2 = 1
        self._count_game = 0
        for i in range(1, 3):
            self._reset_count_move(player=i)
        self._run = True
        self._drop_into_mailbox()

    def _check_state(self):
        if self._data[1] == MESSAGE_ZOMBIE and self._data[2] == MESSAGE_ZOMBIE:
            self._run = False

    def _pick_up_from_mailbox(self):
        return json.loads(self._data[1]), json.loads(self._data[2])

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
    def _check_can_transform(self, **func_kwargs):
        pool = eval(func_kwargs["pool"])
        cur_brick = eval(func_kwargs["cur_brick"])
        can = False
        shift = -1
        for i in range(4):
            old_position = copy.deepcopy(cur_brick.position)
            old_state = cur_brick.state
            cur_brick.transform(i)
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
                    self._data[3] = MESSAGE_PLAYER2WIN if func_kwargs["player"] == 1 else MESSAGE_PLAYER1WIN
                else:
                    self._reset_count_move(player=func_kwargs["player"])
                    self._update_pool(player=func_kwargs["player"])
                    self._reset_bricks(player=func_kwargs["player"])

    @_member_selector("count_move", "speed")
    def _reset_count_move(self, **func_kwargs):
        exec("%s = %d" % (func_kwargs["count_move"], (self._FPS * PERIOD_SPEED_1_PER_MOVE) * (0.95 ** func_kwargs["speed"])))

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

    def _check_speed_up(self):
        if self._count_game % (self.FPS * PERIOD_SPEED_1_PER_MOVE) == 0:
            self._speed_up()

    def _speed_up(self):
        self._speed1 += 1
        self._speed2 += 1

    def _drop_into_mailbox(self):
        for i in range(1, 3):
            exec(f"queue_bricks{i} = [brick._get_public_member_dict() for brick in self._queue_bricks{i}]")
            exec(f"cur_brick{i} = self._cur_brick{i}._get_public_member_dict()")
            exec(f"pool{i} = self._pool{i}")
        
        dict_data = {
            "queue_bricks1": eval("queue_bricks1"),
            "cur_brick1": eval("cur_brick1"),
            "pool1": eval("pool1"),
            "queue_bricks2": eval("queue_bricks2"),
            "cur_brick2": eval("cur_brick2"),
            "pool2": eval("pool2")
            }

        self._data[3] = json.dumps(dict_data)


    def _check_can_eliminate(self):
        pass

    def _eliminate(self):
        pass






