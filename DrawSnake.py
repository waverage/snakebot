import math
import sys, pygame
import SnakeEngine as sk
from SnakeEngine import TYPE_SNAKE, TYPE_SNAKE_HEAD_RIGHT

BLUE = (0, 0, 205)
GREEN = (0, 205, 0)
RED = (205, 0, 0)
BLACK = (0, 0, 0)
SILVER = (40, 40, 40)

class DrawSnake:
    def __init__(self, screen, grid, cellWidth, cellHeight, screenOffset):
        self.screen = screen
        self.grid = grid
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.screenOffset = screenOffset

    def draw(self, matrix):
        self.screen.fill(BLACK)

        offset = math.floor(self.screenOffset / 2)
        innerBoxOffset = 2
        # Grid
        # for wo in range(0, self.grid[0] + 1):
        #     pygame.draw.line(self.screen, BLUE, (wo * self.cellWidth + offset, offset), (wo * self.cellWidth + offset, self.cellWidth * self.grid[0] + offset))

        #     for ho in range(0, self.grid[1] + 1):
        #         pygame.draw.line(self.screen, BLUE, (offset, ho * self.cellHeight + offset), (self.cellHeight * self.grid[1] + offset, ho * self.cellHeight + offset))

        for x in range(0, self.grid[0]):
            for y in range(0, self.grid[1]):
                x0 = x * self.cellWidth + offset + innerBoxOffset
                y0 = y * self.cellHeight + offset + innerBoxOffset

                if matrix[x][y] == TYPE_SNAKE:
                    pygame.draw.rect(self.screen, GREEN, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))
                elif self.isHeadBlock(matrix[x][y]):
                    self.drawHead(x0, y0, matrix[x][y], innerBoxOffset)
                elif matrix[x][y] == sk.TYPE_FOOD:
                    pygame.draw.rect(self.screen, RED, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))
                elif matrix[x][y] == sk.TYPE_WALL:
                    pygame.draw.rect(self.screen, SILVER, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))

    def isHeadBlock(self, blockType):
        return blockType >= 2 and blockType <= 5

    def drawHead(self, x0, y0, headType, innerBoxOffset):
        pygame.draw.rect(self.screen, GREEN, (x0, y0, self.cellWidth - (innerBoxOffset * 2), self.cellHeight - (innerBoxOffset * 2)))

        if headType == sk.TYPE_SNAKE_HEAD_RIGHT:
            x = x0 + self.cellWidth - 12 - innerBoxOffset
            y = y0 - innerBoxOffset + math.floor(self.cellHeight / 2)
            pygame.draw.circle(self.screen, BLUE, (x, y - 10), 6)
            pygame.draw.circle(self.screen, BLUE, (x, y + 10), 6)
        elif headType == sk.TYPE_SNAKE_HEAD_DOWN:
            x = x0 - innerBoxOffset + math.floor(self.cellWidth / 2)#
            y = y0 + self.cellHeight - 12 - innerBoxOffset
            pygame.draw.circle(self.screen, BLUE, (x - 10, y), 6)
            pygame.draw.circle(self.screen, BLUE, (x + 10, y), 6)
        elif headType == sk.TYPE_SNAKE_HEAD_LEFT:
            x = x0 + 12 - innerBoxOffset
            y = y0 - innerBoxOffset + math.floor(self.cellHeight / 2)
            pygame.draw.circle(self.screen, BLUE, (x, y - 10), 6)
            pygame.draw.circle(self.screen, BLUE, (x, y + 10), 6)
        elif headType == sk.TYPE_SNAKE_HEAD_UP:
            x = x0 - innerBoxOffset + math.floor(self.cellWidth / 2)#
            y = y0 + 12 - innerBoxOffset
            pygame.draw.circle(self.screen, BLUE, (x - 10, y), 6)
            pygame.draw.circle(self.screen, BLUE, (x + 10, y), 6)