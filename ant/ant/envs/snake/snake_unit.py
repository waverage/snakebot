DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

TURN_UP = 0
TURN_RIGHT = 1
TURN_DOWN = 2
TURN_LEFT = 3

class SnakeUnit:
    def __init__(self):
        self.direction = DIR_RIGHT
        self.directionWasChanged = False
        self.defaultBody = None
        self.snake = []
        self.nextSnake = []
        self.isDie = False

    def getArr(self):
        return self.snake
    
    def reset(self):
        self.direction = DIR_RIGHT
        self.directionWasChanged = False
        self.isDie = False

        if self.defaultBody is not None:
            self.snake = self.defaultBody

    def setBody(self, body):
        self.snake = body

        if self.defaultBody is None:
            self.defaultBody = body

    def do(self, action):
        if action >= 0 and action <= 4:
            self.turn(action)

    def turn(self, direction):
        if self.directionWasChanged:
            return

        if self.direction == DIR_LEFT and direction == DIR_RIGHT:
                return
        if self.direction == DIR_RIGHT and direction == DIR_LEFT:
            return
        if self.direction == DIR_UP and direction == DIR_DOWN:
            return
        if self.direction == DIR_DOWN and direction == DIR_UP:
            return

        self.direction = direction
        self.directionWasChanged = True

    def getHeadPos(self):
        return self.snake[len(self.snake) - 1]

    def getNewHeadPos(self):
        pos = self.getHeadPos()
        if self.direction == DIR_RIGHT:
            pos = (pos[0] + 1, pos[1])
        elif self.direction == DIR_DOWN:
            pos = (pos[0], pos[1] + 1)
        elif self.direction == DIR_LEFT:
            pos = (pos[0] - 1, pos[1])
        elif self.direction == DIR_UP:
            pos = (pos[0], pos[1] - 1)

        return pos

    def equalPos(self, pos1, pos2):
        return pos1[0] == pos2[0] and pos1[1] == pos2[1]

    def getNextSnakeArr(self, foodPos):
        newHeadPos = self.getNewHeadPos()
        foodReached = False

        if self.equalPos(newHeadPos, foodPos):
            # is food
            foodReached = True

        # Move head forward and remove last part if need
        newSnake = self.snake[::]

        newSnake.append(newHeadPos)
        if not foodReached:
            newSnake.pop(0)

        self.nextSnake = newSnake

    def die(self):
        self.isDie = True

    def step(self):
        self.directionWasChanged = False