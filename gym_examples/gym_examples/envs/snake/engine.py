import math
import random
import numpy as np

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

TYPE_EMPTY = 0
TYPE_SNAKE = 1
TYPE_SNAKE_HEAD_UP = 2
TYPE_SNAKE_HEAD_RIGHT = 3
TYPE_SNAKE_HEAD_DOWN = 4
TYPE_SNAKE_HEAD_LEFT = 5
TYPE_FOOD = 6
TYPE_WALL = 7

class SnakeEngine:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.isGameEnd = False
        self.isWin = False
        self.snakes = [] # Snake.py
        self.walls = [] # Wall.py
        self.foodPos = (-1, -1)
        self.foodReached = False

    def reset(self):
        self.isGameEnd = False
        self.isWin = False

        for sn in self.snakes:
            sn.reset()

        # init food position
        self.generateNewFood()
    
    def getFoodPosition(self):
        return self.foodPos

    def generateNewFood(self):
        matrix = self.getMatrix()

        freePositions = []
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if matrix[x][y] == TYPE_EMPTY:
                    freePositions.append((x, y))

        if len(freePositions) <= 0:
            self.isWin = True
            self.isGameEnd = True
            return

        foodIndex = random.randint(0, len(freePositions) - 1)
        self.foodPos = freePositions[foodIndex]

    def checkCollisions(self, pos):
        if pos[0] > self.size[0] - 1 or pos[1] > self.size[1] or pos[0] < 0 or pos[1] < 0:
            # Collision with wall. Out of world map
            return True

        for i in range(0, len(self.snake) - 2):
            spos = self.snake[i]

            if spos[0] == pos[0] and spos[1] == pos[1]:
                # Collision with the snake
                return True

        return False

    def isFood(self, pos):
        return pos[0] == self.foodPos[0] and pos[1] == self.foodPos[1]
    
    def isFoodReached(self):
        return self.foodReached

    def step(self):
        if self.isGameEnd:
            return

        matrix = self.generateEmptyMatrix()

        for wall in self.walls:
            for pos in wall.getArr():
                if self.checkPosOutOfRange(pos):
                    continue
                matrix[pos[0]][pos[1]] = TYPE_WALL

        matrix[self.foodPos[0]][self.foodPos[1]] = TYPE_FOOD

        for snake in self.snakes:
            snake.getNextSnakeArr(self.foodPos)

            nextSnake = snake.nextSnake
            snakeLen = len(nextSnake)
            index = -1
            for pos in nextSnake:
                index = index + 1
                if self.checkPosOutOfRange(pos):
                    # Snake out of range so snake should die
                    snake.die()
                    break

                if matrix[pos[0]][pos[1]] == TYPE_WALL:
                    snake.die()
                    break

                if index == snakeLen - 1 and matrix[pos[0]][pos[1]] == TYPE_SNAKE:
                    snake.die()
                    break

                matrix[pos[0]][pos[1]] = TYPE_SNAKE

        self.foodReached = False
        for snake in self.snakes:
            if not snake.isDie:
                snake.snake = snake.nextSnake[::]
                snake.nextSnake = []
                snake.step()

                pos = snake.getHeadPos()
                if not self.foodReached and pos[0] == self.foodPos[0] and pos[1] == self.foodPos[1]:
                    self.generateNewFood()
                    self.foodReached = True

        self.checkIfAllDied()

    def checkIfAllDied(self):
        for snake in self.snakes:
            if not snake.isDie:
                return
        self.isGameEnd = True

    def checkPosOutOfRange(self, pos):
        return pos[0] > self.size[0] - 1 or pos[1] > self.size[1] - 1 or pos[0] < 0 or pos[1] < 0

    def generateEmptyMatrix(self):
        matrix = []
        for x in range(0, self.size[0]):
            matrix.append([])
            for y in range(0, self.size[1]):
                matrix[x].append(TYPE_EMPTY)
        return matrix

    def getMatrix(self):
        matrix = self.generateEmptyMatrix()

        for snake in self.snakes:
            for pos in snake.getArr():
                if self.checkPosOutOfRange(pos):
                    continue
                matrix[pos[0]][pos[1]] = TYPE_SNAKE
            pos = snake.getHeadPos()
            if self.checkPosOutOfRange(pos):
                continue

            blockType = TYPE_SNAKE_HEAD_RIGHT 
            if snake.direction == DIR_UP:
                blockType = TYPE_SNAKE_HEAD_UP
            elif snake.direction == DIR_DOWN:
                blockType = TYPE_SNAKE_HEAD_DOWN
            elif snake.direction == DIR_LEFT:
                blockType = TYPE_SNAKE_HEAD_LEFT
            elif snake.direction == DIR_RIGHT:
                blockType = TYPE_SNAKE_HEAD_RIGHT 
            matrix[pos[0]][pos[1]] = blockType


        for wall in self.walls:
            for pos in wall.getArr():
                if self.checkPosOutOfRange(pos):
                    continue
                matrix[pos[0]][pos[1]] = TYPE_WALL

        matrix[self.foodPos[0]][self.foodPos[1]] = TYPE_FOOD

        return matrix

    def isGameOver(self):
        return self.isGameEnd

    def addSnake(self, snake):
        self.snakes.append(snake)

    def addWall(self, wall):
        self.walls.append(wall)

    def getVisibleArea(self, size, headPos):
        matrix = np.array(self.getMatrix())

        xHalfSize = math.floor(size[0] / 2)
        yHalfSize = math.floor(size[1] / 2)

        x0 = headPos[0] - xHalfSize
        x1 = headPos[0] + xHalfSize + 1

        y0 = headPos[1] - yHalfSize
        y1 = headPos[1] + yHalfSize + 1

        area = matrix[x0:x1,y0:y1]

        if x0 < 0:
            addToXBegin = abs(x0)
            area = np.pad(area, ((addToXBegin, 0), (0, 0)), 'constant', constant_values=0)
        if x1 > self.size[0]:
            addToXEnd = x1 - (self.size[0])
            area = np.pad(area, ((0, addToXEnd), (0, 0)), 'constant', constant_values=0)
        if y0 < 0:
            addToYBegin = abs(y0)
            area = np.pad(area, ((0, 0), (addToYBegin, 0)), 'constant', constant_values=0)
        if y1 > self.size[1]:
            addToYEnd = y1 - (self.size[1])
            area = np.pad(area, ((0, 0), (0, addToYEnd)), 'constant', constant_values=0)

        for x in range(0, len(area)):
            for y in range(0, len(area[x])):
                if area[x][y] >= 2 and area[x][y] <= 5:
                    area[x][y] = TYPE_SNAKE

        return area