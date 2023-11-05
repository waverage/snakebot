from ctypes.wintypes import FLOAT
import gym
from gym import spaces
from ant.render import Renderer
import pygame
import numpy as np
import math
from ant.envs.snake.engine import SnakeEngine, TYPE_EMPTY, TYPE_FOOD, TYPE_SNAKE, TYPE_WALL, TYPE_SNAKE_HEAD_UP, TYPE_SNAKE_HEAD_DOWN,  TYPE_SNAKE_HEAD_LEFT, TYPE_SNAKE_HEAD_RIGHT
from ant.envs.snake.snake_unit import SnakeUnit, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP
from ant.envs.snake.wall import Wall
from ant.envs.snake.render import SnakeRenderer

#from snake_unit import SnakeUnit

STEPS_LIMIT = 2000

class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array", "none"], "render_fps": 10}

    def __init__(self, render_mode='human', size=10, visibleArea=5):
        self.size = size  # The size of the square grid
        self.window_size = 180  # The size of the PyGame window
        self.visibleAreaSize = visibleArea
        self.distanceToFood = 0
        self.closed = False
        self.steps = 0

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).

        # self.observation_space = spaces.Dict({
        #     "area": spaces.Box(-1, 1, shape=(self.visibleAreaSize * self.visibleAreaSize,), dtype=float),
        #     "head": spaces.Box(0, 1, shape=(2,), dtype=float),
        #     "food": spaces.MultiBinary(4),
        #     "direction": spaces.MultiBinary(4),
        #     "danger": spaces.MultiBinary(3),
        # })
        #self.observation_space = spaces.Box(0, 255, shape=(self.visibleAreaSize * self.visibleAreaSize,), dtype=np.uint8)
        self.observation_space = spaces.Box(0, 255, shape=(3, self.window_size, self.window_size,), dtype=np.uint8)

        # We have 3 actions, corresponding to "left", "straight", "right"
        self.action_space = spaces.Discrete(4)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self._renderer = Renderer(self.render_mode, self._render_frame)

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
        self._drawer = None

    def _get_obs(self):
        arr = self._render_frame(self.render_mode)
        arr = np.moveaxis(arr, -1, 0)
        # print("arr\n", arr)
        return np.array(arr)
        # flattenArea = np.array(self.getMatrixImage())
        # flattenArea = np.moveaxis(flattenArea, -1, 0)

        # print('flattenArea', flattenArea)
        # if self.render_mode == "human":
        #     print('direction', self.snakeUnit.direction)
        #     print('head', self.getNormalizedHeadPos())
        #     print('target', self.getNormalizedTargetPos())
        #     print('area', flattenArea)

        # return np.array(flattenArea)
        # return {
        #     "area": np.array(flattenArea),
        #     "head": self.getNormalizedHeadPos(),
        #     "food": self.getNormalizedFoodDirection(),
        #     "direction": self.getNormalizedSnakeDirection(),
        #     "danger": self.getDangerObs(),
        # }

    def getDangerObs(self):
        hX = self._headPos[0]
        hY = self._headPos[1]
        d = self.snakeUnit.direction
        # TYPE_EMPTY = 0
        # TYPE_FOOD = 1
        # TYPE_SNAKE_HEAD_UP = 2
        # TYPE_SNAKE_HEAD_RIGHT = 3
        # TYPE_SNAKE_HEAD_DOWN = 4
        # TYPE_SNAKE_HEAD_LEFT = 5
        # TYPE_SNAKE = 6
        # TYPE_WALL = 7

        m = self._visibleArea

        v = [0, 0]
        lv = [0, 0]
        rv = [0, 0]
        if d == DIR_UP:
            v[1] = -1
            lv[0] = -1
            rv[0] = 1
        elif d == DIR_DOWN:
            v[1] = 1
            lv[0] = 1
            rv[0] = -1
        if d == DIR_LEFT:
            v[0] = -1
            lv[1] = 1
            rv[1] = -1
        elif d == DIR_RIGHT:
            v[0] = 1
            lv[1] = -1
            rv[1] = 1

        return np.array([
            1 if m[hX + v[0]][hY + v[1]] > 1 else 0, # ahead
            1 if m[hX + lv[0]][hY + lv[1]] > 1 else 0, # left
            1 if m[hX + rv[0]][hY + rv[1]] > 1 else 0, # right
        ])
    
    def getNormalizedSnakeDirection(self):
        d = self.snakeUnit.direction
        return np.array([
            1 if d == DIR_UP else 0,
            1 if d == DIR_DOWN else 0,
            1 if d == DIR_LEFT else 0,
            1 if d == DIR_RIGHT else 0,
        ])
    
    def getNormalizedFoodDirection(self):
        hX = self._headPos[0]
        hY = self._headPos[1]
        fX = self._target_location[0]
        fY = self._target_location[1]

        return np.array([
            1 if fY < hY else 0, # top
            1 if fY > hY else 0, # down
            1 if fX < hX else 0, # left
            1 if fX > hX else 0, # right
        ])
    
    def getMatrixImage(self):
        flattenArea = []
        y = 0
        for row in self._visibleArea:
            flattenArea.append([])
            for val in row:
                flattenArea[y].append([self.normalizeCellTypeInGrayScale(val)])
            y = y + 1
        return flattenArea

    def _getFlattenVisibleArea(self):
        flattenArea = []
        for row in self._visibleArea:
            for val in row:
                flattenArea.append(self.normalizeCellType(val))
        return flattenArea
    
    def normalizeCellTypeInGrayScale(self, cellType):
        if cellType == TYPE_FOOD:
            return 30
        elif cellType == TYPE_EMPTY:
            return 0
        elif cellType == TYPE_SNAKE_HEAD_UP:
            return 170
        elif cellType == TYPE_SNAKE_HEAD_DOWN:
            return 140
        elif cellType == TYPE_SNAKE_HEAD_LEFT:
            return 110
        elif cellType == TYPE_SNAKE_HEAD_RIGHT:
            return 80
        elif cellType == TYPE_SNAKE:
            return 200
        elif cellType == TYPE_WALL:
            return 255
        else:
            return 0

    def normalizeCellType(self, cellType):
        if cellType > 7:
            cellType = 7

        if cellType == TYPE_FOOD:
            return 1
        elif cellType == TYPE_EMPTY:
            return 0
        elif cellType == TYPE_SNAKE:
            return -0.7
        elif cellType == TYPE_WALL:
            return -1
        else:
            return 0
    
    def getNormalizedHeadPos(self):
        x = self.norm(self._headPos[0], 0, self.size - 1)
        y = self.norm(self._headPos[1], 0, self.size - 1)
        return np.array([x, y])

    # def getNormalizedTargetPos(self):
    #     x = self.norm(self._target_location[0], 0, self.size - 1)
    #     y = self.norm(self._target_location[1], 0, self.size - 1)
    #     return np.array([x, y])

    # normalize from -1 to 1
    def norm(self, val, min, max):
        return 2 * ((val - min) / (max - min)) - 1

    def getDistanceToFood(self):
        return np.linalg.norm(np.array(self._headPos) - np.array(self._target_location), ord=1)

    def reset(self):
        # We need the following line to seed self.np_random
        #super().reset()

        self.engine = SnakeEngine((self.size, self.size))

        self.steps = 0
        self.distanceToFood = 0
        self.snakeUnit = SnakeUnit()
        x = math.floor(self.size / 2)
        y = math.floor(self.size / 2)
        self.snakeUnit.setBody([(x - 1, y), (x, y)])
        self.engine.addSnake(self.snakeUnit)

        # Init walls
        # Generate four walls, like room with four walls
        coords = []
        for x in range(0, self.size):
            for y in range(0, self.size):
                if y == 0 or y == self.size - 1 or x == 0 or x == self.size - 1:
                    coords.append((x, y))
        roomWall = Wall(coords)
        self.engine.addWall(roomWall)

        self.engine.reset()

        self._headPos = self.snakeUnit.getHeadPos()
        self._visibleArea = self.engine.getVisibleArea(self.visibleAreaSize, self.snakeUnit.getHeadPos())

        # print('')
        # print('Agent head pos', self._headPos)
        # print('Agent area', self._visibleArea)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self.engine.getFoodPosition()

        observation = self._get_obs()

        self._renderer.reset()
        self._renderer.render_step()

        # print("reset obs ", observation)

        return observation

    def prepareModelAction(self, modelAction):
        # DIR_UP = 0
        # DIR_RIGHT = 1
        # DIR_DOWN = 2
        # DIR_LEFT = 3
        LEFT = 0
        STRAIGHT = 1
        RIGHT = 2

        return modelAction

    def step(self, action):
        self.snakeUnit.turn(self.prepareModelAction(action))
        self.engine.step()

        done = self.engine.isFoodReached()

        done = False
        if self.engine.isFoodReached():
            reward = 1
        elif self.engine.isGameOver():
            if self.render_mode == "human":
                snakeLen = len(self.snakeUnit.snake)
                print('Game over: ', snakeLen)
            reward = -10
            done = True
        else:
            distance = self.getDistanceToFood()
            #print('distance to food', distance)
            if distance > self.distanceToFood:
                reward = -0.11
            else:
                reward = 0.1

            self.distanceToFood = distance

        self.steps += 1
        if self.steps >= STEPS_LIMIT:
            reward = -1
            done = True

        self._headPos = self.snakeUnit.getHeadPos()
        self._visibleArea = self.engine.getVisibleArea(self.visibleAreaSize, self.snakeUnit.getHeadPos())
        self._target_location = self.engine.getFoodPosition()

        observation = self._get_obs()

        self._renderer.render_step()

        return observation, reward, done, {
            "closed": self.closed
        }

    def render(self, second):
        return self._renderer.get_renders()

    def _render_frame(self, mode):
        assert mode is not None

        if self.window is None and mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and mode == "human":
            self.clock = pygame.time.Clock()

        if self._drawer is None and (mode == "human" or mode == "rgb_array"):
            self._drawer = SnakeRenderer(self.window, (self.size, self.size), (self.window_size, self.window_size))

        if mode == "human" or mode == "rgb_array":
            canvas = self._drawer.draw(self.engine.getMatrix(), {
                "visibleArea": self._visibleArea
            })

        if mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Received pygame.quit')
                    self.close()
                    return

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        elif mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        else:  # rgb_array
            return None

    def close(self):
        self.closed = True
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()