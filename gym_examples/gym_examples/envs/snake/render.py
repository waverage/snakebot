import math
import sys, pygame
from gym_examples.envs.snake.engine import TYPE_SNAKE, TYPE_EMPTY, TYPE_WALL, TYPE_FOOD, TYPE_SNAKE_HEAD_RIGHT, TYPE_SNAKE_HEAD_DOWN, TYPE_SNAKE_HEAD_LEFT, TYPE_SNAKE_HEAD_UP

BLUE = (0, 0, 205)
GREEN = (0, 205, 0)
RED = (205, 0, 0)
BLACK = (0, 0, 0)
SILVER = (40, 40, 40)

class SnakeRenderer:
    def __init__(self, screen, grid, windowSize):
        self.screen = screen
        self.grid = grid

        cellWidth = math.floor(windowSize[0] / grid[0])
        cellHeight = math.floor(windowSize[1] / grid[1])

        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.screenOffset = 20
        self.windowSize = windowSize
        self.canvas = pygame.Surface(windowSize)

    def draw(self, matrix):
        self.canvas.fill(BLACK)

        offset = math.floor(self.screenOffset / 2)
        innerBoxOffset = 2
        # Grid
        # for wo in range(0, self.grid[0] + 1):
        #     pygame.draw.line(self.canvas, BLUE, (wo * self.cellWidth + offset, offset), (wo * self.cellWidth + offset, self.cellWidth * self.grid[0] + offset))

        #     for ho in range(0, self.grid[1] + 1):
        #         pygame.draw.line(self.canvas, BLUE, (offset, ho * self.cellHeight + offset), (self.cellHeight * self.grid[1] + offset, ho * self.cellHeight + offset))

        for x in range(0, self.grid[0]):
            for y in range(0, self.grid[1]):
                x0 = x * self.cellWidth + offset + innerBoxOffset
                y0 = y * self.cellHeight + offset + innerBoxOffset

                if matrix[x][y] == TYPE_SNAKE:
                    pygame.draw.rect(self.canvas, GREEN, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))
                elif self.isHeadBlock(matrix[x][y]):
                    self.drawHead(x0, y0, matrix[x][y], innerBoxOffset)
                elif matrix[x][y] == TYPE_FOOD:
                    pygame.draw.rect(self.canvas, RED, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))
                elif matrix[x][y] == TYPE_WALL:
                    pygame.draw.rect(self.canvas, SILVER, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))

        return self.canvas

    def isHeadBlock(self, blockType):
        return blockType >= 2 and blockType <= 5

    def drawHead(self, x0, y0, headType, innerBoxOffset):
        pygame.draw.rect(self.canvas, GREEN, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))

        if headType == TYPE_SNAKE_HEAD_RIGHT:
            x = x0 + self.cellWidth - 12 - innerBoxOffset
            y = y0 - innerBoxOffset + math.floor(self.cellHeight / 2)
            pygame.draw.circle(self.canvas, BLUE, (x, y - 10), 6)
            pygame.draw.circle(self.canvas, BLUE, (x, y + 10), 6)
        elif headType == TYPE_SNAKE_HEAD_DOWN:
            x = x0 - innerBoxOffset + math.floor(self.cellWidth / 2)#
            y = y0 + self.cellHeight - 12 - innerBoxOffset
            pygame.draw.circle(self.canvas, BLUE, (x - 10, y), 6)
            pygame.draw.circle(self.canvas, BLUE, (x + 10, y), 6)
        elif headType == TYPE_SNAKE_HEAD_LEFT:
            x = x0 + 12 - innerBoxOffset
            y = y0 - innerBoxOffset + math.floor(self.cellHeight / 2)
            pygame.draw.circle(self.canvas, BLUE, (x, y - 10), 6)
            pygame.draw.circle(self.canvas, BLUE, (x, y + 10), 6)
        elif headType == TYPE_SNAKE_HEAD_UP:
            x = x0 - innerBoxOffset + math.floor(self.cellWidth / 2)#
            y = y0 + 12 - innerBoxOffset
            pygame.draw.circle(self.canvas, BLUE, (x - 10, y), 6)
            pygame.draw.circle(self.canvas, BLUE, (x + 10, y), 6)