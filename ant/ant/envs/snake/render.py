import math
import sys, pygame
from ant.envs.snake.engine import TYPE_SNAKE, TYPE_EMPTY, TYPE_WALL, TYPE_FOOD, TYPE_SNAKE_HEAD_RIGHT, TYPE_SNAKE_HEAD_DOWN, TYPE_SNAKE_HEAD_LEFT, TYPE_SNAKE_HEAD_UP

BLUE = (0, 0, 205)
GREEN = (0, 205, 0)
RED = (205, 0, 0)
BLACK = (0, 0, 0)
SILVER = (40, 40, 40)

class SnakeRenderer:
    def __init__(self, screen, grid, windowSize):
        self.screen = screen
        self.grid = grid
        self.screenOffset = 0
        self.cell_margin = 1

        cellWidth = math.floor((windowSize[0] - self.screenOffset) / grid[0])
        cellHeight = math.floor((windowSize[1] - self.screenOffset) / grid[1])

        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.windowSize = windowSize
        self.canvas = pygame.Surface(windowSize)

    def draw(self, matrix, info):
        visibleArea = info["visibleArea"]

        self.canvas.fill(BLACK)

        offset = math.floor(self.screenOffset / 2)
        innerBoxOffset = 1
        # Grid
        # for wo in range(0, self.grid[0] + 1):
        #     pygame.draw.line(self.canvas, BLUE, (wo * self.cellWidth + offset, offset), (wo * self.cellWidth + offset, self.cellWidth * self.grid[0] + offset))

        #     for ho in range(0, self.grid[1] + 1):
        #         pygame.draw.line(self.canvas, BLUE, (offset, ho * self.cellHeight + offset), (self.cellHeight * self.grid[1] + offset, ho * self.cellHeight + offset))

        headPos = []

        for x in range(0, self.grid[0]):
            for y in range(0, self.grid[1]):
                x0 = x * self.cellWidth + offset + self.cell_margin
                y0 = y * self.cellHeight + offset + self.cell_margin

                if matrix[x][y] == TYPE_SNAKE:
                    pygame.draw.rect(self.canvas, GREEN, (x0, y0, self.cellWidth - (self.cell_margin * 2), self.cellHeight - (self.cell_margin * 2)))
                elif self.isHeadBlock(matrix[x][y]):
                    headPos = [x, y]
                    self.drawHead(x0, y0, matrix[x][y])
                elif matrix[x][y] == TYPE_FOOD:
                    pygame.draw.rect(self.canvas, RED, (x0, y0, self.cellWidth - (self.cell_margin * 2), self.cellHeight - (self.cell_margin * 2)))
                elif matrix[x][y] == TYPE_WALL:
                    pygame.draw.rect(self.canvas, SILVER, (x0, y0, self.cellWidth - (self.cell_margin * 2), self.cellHeight - (self.cell_margin * 2)))

        
        s = pygame.Surface((1000,750))  # the size of your rect
        s.set_alpha(32)                # alpha level
        #s.fill((255,255,255))           # this fills the entire surface

        # Draw visible area rect
        # visibleAreaOffset = round((len(visibleArea) - 1) / 2)
        # for x in range(0, len(visibleArea)):
        #     for y in range(0, len(visibleArea[x])):
        #         rx = headPos[0] + x - visibleAreaOffset
        #         ry = headPos[1] + y - visibleAreaOffset
        #         x0 = rx * self.cellWidth + offset + self.cell_margin
        #         y0 = ry * self.cellHeight + offset + self.cell_margin
        #         pygame.draw.rect(s, RED, (x0, y0, self.cellWidth - (self.cell_margin * 2), self.cellHeight - (self.cell_margin * 2)))

        self.canvas.blit(s, (0,0))    # (0,0) are the top-left coordinates

        return self.canvas

    def isHeadBlock(self, blockType):
        return blockType >= 2 and blockType <= 5

    def drawHead(self, x0, y0, headType):
        pygame.draw.rect(self.canvas, GREEN, (x0, y0, self.cellWidth - (self.cell_margin * 2), self.cellHeight - (self.cell_margin * 2)))

        if headType == TYPE_SNAKE_HEAD_RIGHT:
            pygame.draw.rect(self.canvas, BLUE, (x0 + self.cellWidth - math.floor(self.cellWidth / 3), y0, math.floor(self.cellWidth / 3), self.cellHeight - (self.cell_margin * 2)))
        elif headType == TYPE_SNAKE_HEAD_DOWN:
            pygame.draw.rect(self.canvas, BLUE, (x0, y0 + self.cellHeight - math.floor(self.cellHeight / 3), self.cellWidth - (self.cell_margin * 2), math.floor(self.cellHeight / 3)))
        elif headType == TYPE_SNAKE_HEAD_LEFT:
            pygame.draw.rect(self.canvas, BLUE, (x0, y0, math.floor(self.cellWidth / 3), self.cellHeight - (self.cell_margin * 2)))
        elif headType == TYPE_SNAKE_HEAD_UP:
            pygame.draw.rect(self.canvas, BLUE, (x0, y0, self.cellWidth - (self.cell_margin * 2), math.floor(self.cellHeight / 3)))