import random

# COLORS
COLOR_RED = [255, 0, 0]
COLOR_GREEN = [0, 255, 0]
COLOR_BLUE = [0, 0, 255]
COLOR_YELLOW = [255, 255, 0]
COLOR_PURPLE = [255, 0, 255]
COLOR_CYAN = [0, 255, 255]
COLOR_WHITE = [255, 255, 255]

class Brick:
    def __init__(self):
        self.type = 0       
        self.color = None
        self.position = None
        self.state = 1
        self._probability = [1] * 1 + [2] * 1 + [3] * 1 + [4] * 1 + [5] * 1 + [6] * 1 + [7] * 1
        self._spawn()

    def _spawn(self):
        random_type = random.choice(self._probability)
        if random_type == 1:
            self.position = [[3, -1], [4, -1], [5, -1], [5, -2]]
            self.color = COLOR_RED
        elif random_type == 2:
            self.position = [[3, -2], [3, -1], [4, -1], [5, -1]]
            self.color = COLOR_GREEN
        elif random_type == 3:
            self.position = [[4, -1], [4, -1], [5, -2], [5, -2]]
            self.color = COLOR_BLUE
        elif random_type == 4:
            self.position = [[3, -1], [4, -1], [5, -1], [6, -1]]
            self.color = COLOR_YELLOW  
        elif random_type == 5:
            self.position = [[3, -1], [4, -1], [4, -2], [5, -2]]
            self.color = COLOR_PURPLE
        elif random_type == 6:
            self.position = [[3, -2], [4, -2], [4, -1], [5, -1]]
            self.color = COLOR_CYAN
        elif random_type == 7:
            self.position = [[3, -1], [4, -1], [5, -1], [4, -2]]
            self.color = COLOR_WHITE
        self.type = random_type

    def move(self, direction):
        if direction == "LEFT":
            for debris in self.position:
                debris[0] -= 1
        elif direction == "RIGHT":
            for debris in self.position:
                debris[0] += 1
        elif direction == "DOWN":
            for debris in self.position:
                debris[1] += 1

    def transform(self, shift):
        if self.type == 1:
            if self.state == 1:
                self.position[0][0] += 1
                self.position[0][1] -= 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] -= 1 
                self.position[2][1] += 1 
                self.position[3][0] += 0 
                self.position[3][1] += 2
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] -= 1   
            elif self.state == 2:
                self.position[0][0] += 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] -= 1 
                self.position[2][1] -= 1 
                self.position[3][0] -= 2 
                self.position[3][1] += 0 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
            elif self.state == 3:
                self.position[0][0] -= 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] -= 1 
                self.position[3][0] += 0 
                self.position[3][1] -= 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
            elif self.state == 4:
                self.position[0][0] -= 1
                self.position[0][1] -= 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] += 1 
                self.position[3][0] += 2
                self.position[3][1] += 0 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] -= 1  
        elif self.type == 2:
            if self.state == 1:
                self.position[0][0] += 2
                self.position[0][1] += 0
                self.position[1][0] += 1 
                self.position[1][1] -= 1 
                self.position[2][0] -= 0 
                self.position[2][1] += 0 
                self.position[3][0] -= 1 
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] -= 1  
            elif self.state == 2:
                self.position[0][0] += 0
                self.position[0][1] += 2
                self.position[1][0] += 1 
                self.position[1][1] += 1 
                self.position[2][0] -= 0 
                self.position[2][1] -= 0 
                self.position[3][0] -= 1 
                self.position[3][1] -= 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
            elif self.state == 3:
                self.position[0][0] -= 2
                self.position[0][1] += 0
                self.position[1][0] -= 1
                self.position[1][1] += 1 
                self.position[2][0] += 0 
                self.position[2][1] -= 0 
                self.position[3][0] += 1 
                self.position[3][1] -= 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
            elif self.state == 4:
                self.position[0][0] -= 0
                self.position[0][1] -= 2
                self.position[1][0] -= 1 
                self.position[1][1] -= 1 
                self.position[2][0] += 0
                self.position[2][1] += 0 
                self.position[3][0] += 1
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] -= 1  
        elif self.type == 4:
            if self.state == 1:
                self.position[0][0] += 1
                self.position[0][1] -= 1
                self.position[1][0] += 0 
                self.position[1][1] -= 0 
                self.position[2][0] -= 1 
                self.position[2][1] += 1 
                self.position[3][0] -= 2 
                self.position[3][1] += 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
                if shift == 2:
                    for i in range(4):
                        self.position[i][1] -= 1  
                if shift == 3:
                    for i in range(4):
                        self.position[i][1] -= 2  
            elif self.state == 2:
                self.position[0][0] -= 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] -= 1 
                self.position[3][0] += 2 
                self.position[3][1] -= 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
                if shift == 2:
                    for i in range(4):
                        self.position[i][0] -= 1  
                if shift == 3:
                    for i in range(4):
                        self.position[i][0] -= 2  
            if self.state == 3:
                self.position[0][0] += 1
                self.position[0][1] -= 1
                self.position[1][0] += 0 
                self.position[1][1] -= 0 
                self.position[2][0] -= 1 
                self.position[2][1] += 1 
                self.position[3][0] -= 2 
                self.position[3][1] += 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
                if shift == 2:
                    for i in range(4):
                        self.position[i][1] -= 1  
                if shift == 3:
                    for i in range(4):
                        self.position[i][1] -= 2  
            elif self.state == 4:
                self.position[0][0] -= 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] -= 1 
                self.position[3][0] += 2 
                self.position[3][1] -= 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
                if shift == 2:
                    for i in range(4):
                        self.position[i][0] -= 1  
                if shift == 3:
                    for i in range(4):
                        self.position[i][0] -= 2  
        elif self.type == 5:
            if self.state == 1:
                self.position[0][0] += 0
                self.position[0][1] -= 2
                self.position[1][0] -= 1 
                self.position[1][1] -= 1 
                self.position[2][0] -= 0 
                self.position[2][1] += 0 
                self.position[3][0] -= 1 
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
            elif self.state == 2:
                self.position[0][0] += 2
                self.position[0][1] += 0
                self.position[1][0] += 1 
                self.position[1][1] -= 1 
                self.position[2][0] -= 0 
                self.position[2][1] -= 0 
                self.position[3][0] -= 1 
                self.position[3][1] -= 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] -= 1  
            elif self.state == 3:
                self.position[0][0] -= 0
                self.position[0][1] += 2
                self.position[1][0] += 1
                self.position[1][1] += 1 
                self.position[2][0] += 0 
                self.position[2][1] -= 0 
                self.position[3][0] += 1 
                self.position[3][1] -= 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] -= 1  
            elif self.state == 4:
                self.position[0][0] -= 2
                self.position[0][1] -= 0
                self.position[1][0] -= 1 
                self.position[1][1] += 1 
                self.position[2][0] += 0
                self.position[2][1] += 0 
                self.position[3][0] += 1
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
        elif self.type == 6:
            if self.state == 1:
                self.position[0][0] += 1
                self.position[0][1] -= 1
                self.position[1][0] -= 0 
                self.position[1][1] -= 0 
                self.position[2][0] -= 1 
                self.position[2][1] -= 1 
                self.position[3][0] -= 2 
                self.position[3][1] += 0 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
            elif self.state == 2:
                self.position[0][0] += 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] -= 0 
                self.position[2][0] += 1 
                self.position[2][1] -= 1 
                self.position[3][0] -= 0 
                self.position[3][1] -= 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] -= 1  
            elif self.state == 3:
                self.position[0][0] -= 1
                self.position[0][1] += 1
                self.position[1][0] += 0
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] += 1 
                self.position[3][0] += 2 
                self.position[3][1] -= 0 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] -= 1  
            elif self.state == 4:
                self.position[0][0] -= 1
                self.position[0][1] -= 1
                self.position[1][0] -= 0 
                self.position[1][1] += 0 
                self.position[2][0] -= 1
                self.position[2][1] += 1 
                self.position[3][0] += 0
                self.position[3][1] += 2 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
        elif self.type == 7:
            if self.state == 1:
                self.position[0][0] += 1
                self.position[0][1] -= 1
                self.position[1][0] -= 0 
                self.position[1][1] -= 0 
                self.position[2][0] -= 1 
                self.position[2][1] += 1 
                self.position[3][0] += 1 
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] -= 1  
            elif self.state == 2:
                self.position[0][0] += 1
                self.position[0][1] += 1
                self.position[1][0] += 0 
                self.position[1][1] -= 0 
                self.position[2][0] -= 1 
                self.position[2][1] -= 1 
                self.position[3][0] -= 1
                self.position[3][1] += 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] += 1  
            elif self.state == 3:
                self.position[0][0] -= 1
                self.position[0][1] += 1
                self.position[1][0] += 0
                self.position[1][1] += 0 
                self.position[2][0] += 1 
                self.position[2][1] -= 1 
                self.position[3][0] -= 1 
                self.position[3][1] -= 1 
                if shift == 1:
                    for i in range(4):
                        self.position[i][1] += 1  
            elif self.state == 4:
                self.position[0][0] -= 1
                self.position[0][1] -= 1
                self.position[1][0] -= 0 
                self.position[1][1] += 0 
                self.position[2][0] += 1
                self.position[2][1] += 1 
                self.position[3][0] += 1
                self.position[3][1] -= 1
                if shift == 1:
                    for i in range(4):
                        self.position[i][0] -= 1  

        self.state = 1 if self.state + 1 == 5 else self.state + 1
    
    def _get_public_member_dict(self):
        dict_member = self.__dict__
        public_member = []
        for k, v in dict_member.items():
            if k[0] != '_':
                public_member.append((k, v))
        return dict(public_member)



            
        
        