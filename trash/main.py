from gym_examples.gym_examples.envs.snake.snake_unit import Snake, DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT
from gym_examples.gym_examples.envs.snake.wall import Wall
#import tensorflow as tf
import numpy as np
import random
import sys, pygame
import math
import gym_examples.gym_examples.envs.snake.engine as sk
import gym_examples.gym_examples.envs.snake.render as sr
import SnakeBot as sb


pygame.init()

size = width, height = 720, 720
grid = (10, 10) # width / height
cellWidth = math.floor(width / grid[0])
cellHeight = math.floor(height / grid[1])
screenOffset = 20

screen = pygame.display.set_mode((size[0] + screenOffset, size[1] + screenOffset))
clock = pygame.time.Clock()

snakeEngine = sk.SnakeEngine(grid)

snake1 = Snake()
snake2 = Snake()

# init snake in the midle of field
x = math.floor(grid[0] / 2)
y = math.floor(grid[1] / 2)
snake1.setBody([(x - 1, y), (x, y)])
snake2.setBody([(x - 1, y - 2), (x, y - 2)])

snakeEngine.addSnake(snake1)
snakeEngine.addSnake(snake2)

# Generate four walls, like room with four walls
coords = []
for x in range(0, grid[0]):
    for y in range(0, grid[1]):
        if y == 0 or y == grid[1] - 1 or x == 0 or x == grid[0] - 1:
            coords.append((x, y))
roomWall = Wall(coords)

snakeEngine.addWall(roomWall)

snakeEngine.reset()

bot = sb.SnakeBot()

render = sr.DrawSnake(screen, grid, size)

def endGame():
    print('End game')
    #pygame.time.wait(5000)
    snakeEngine.reset()
 
def update():
    snakeEngine.step()

delta = 0

while 1:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:#or event.type == pygame.KEYUP
            if event.mod == pygame.KMOD_NONE:
                continue
            else:
                if event.key == pygame.K_UP:
                    snake1.turn(DIR_UP)
                if event.key == pygame.K_DOWN:
                    snake1.turn(DIR_DOWN)
                if event.key == pygame.K_LEFT:
                    snake1.turn(DIR_LEFT)
                if event.key == pygame.K_RIGHT:
                    snake1.turn(DIR_RIGHT)
                if event.key == pygame.K_F1:
                    snakeEngine.reset()

    action = bot.makeDecision()
    if action == sb.DO_NOTHING:
        pass
    else:
        snake1.do(action)


    ticks = pygame.time.get_ticks()
    if ticks - delta > 500:
        delta = ticks
        update()

    if snakeEngine.isGameOver():
        endGame()

    render.draw(snakeEngine.getMatrix())
    pygame.display.flip()
