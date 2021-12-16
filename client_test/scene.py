from set import Set

# PROTOCOL TAGS
MESSAGE_ENDSCENE = "$ENDSCENE"
MESSAGE_STARTGAME1 = "$STARTGAME1"
MESSAGE_STARTGAME2 = "$STARTGAME2"
EVENT_QUEUE = "$QUEUE"
EVENT_CHANGESCENE = "$CHANGESCENE"
ERROR_TIMEOUT = "$ERROR_TIMEOUT"
ERROR_VERSION = "$ERROR_VERSION"
MESSAGE_PLAYER1WIN = "$PLAYER1WIN"
MESSAGE_PLAYER2WIN = "$PLAYER2WIN"
EVENT_CONFIRMLEAVE = "$CONFIRMLEAVE"

# WINDOW
WIN_HEIGHT = 600
WIN_WIDTH = 900

# ATTRIBUTES
POSITION_DIALOGUE = (int(0.500 * WIN_WIDTH), int(0.500 * WIN_HEIGHT))

# COLORS
COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]
COLOR_BLUE = [0, 0, 255]
COLOR_YELLOW = [255, 255, 0]
COLOR_PURPLE = [255, 0, 255]
COLOR_CYAN = [0, 255, 255]
COLOR_WHITE = [255, 255, 255]
COLOR_BLACK = [0, 0, 0]

class Scene:
    def __init__(self):
        self.name = type(self).__name__
        self._rundown = {"init": self.init}
        self._name_entrance = "init"
        self._name_current_part = self._name_entrance
        self._run = True
        self._name_next_scene = self.name
        self.events = []
        self._equipment = {}

    def init(self):
        if EVENT_CHANGESCENE in self.events:
            self.events = []
            self._name_current_part = self._name_entrance
            self._name_next_scene = self.name
        name_next_part = MESSAGE_ENDSCENE
        return name_next_part


    def _switch_to_part(self, name_part):
        self._name_current_part = name_part

    def _action(self):
        while self._run:
            name_next_part = self._rundown[self._name_current_part]()
            if name_next_part == MESSAGE_ENDSCENE:
                self._run = False
            else:
                self._switch_to_part(name_next_part)

        # reset
        if EVENT_CHANGESCENE in self.events:
            self._name_current_part = "init"
        else:
            self._name_current_part = self._name_entrance
        self._run = True
        return self._name_next_scene

    def __call__(self, equipment):
        self._equipment = equipment
        return self._action()
      
        
