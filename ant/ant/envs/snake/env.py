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
from PIL import Image

STEPS_LIMIT = 2000
OBS_TYPE_IMAGE = "image"
OBS_TYPE_DICT = "dict"
OBS_TYPE_TEXT = "text"

class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array", "none"], "render_fps": 10}

    def __init__(self, render_mode='human', size=10, visibleArea=5, observation_type=OBS_TYPE_IMAGE, window_size=180, cnn_input_size=40, random_state=False):
        self.size = size  # The size of the square grid
        self.window_size = window_size  # The size of the PyGame window
        self.visibleAreaSize = visibleArea
        self.distanceToFood = 0
        self.closed = False
        self.steps = 0
        self.observation_type = observation_type
        self.cnn_input_size = cnn_input_size
        self.random_state = random_state

        if self.observation_type == OBS_TYPE_IMAGE:
            self.observation_space = spaces.Box(0, 255, shape=(3, self.cnn_input_size, self.cnn_input_size,), dtype=np.uint8)
        else:
            self.observation_space = spaces.Dict({
                "area": spaces.Box(-1, 1, shape=(self.visibleAreaSize * self.visibleAreaSize,), dtype=float),
                "head": spaces.Box(0, 1, shape=(2,), dtype=float),
                "food": spaces.MultiBinary(4),
                "direction": spaces.MultiBinary(4),
            })

        # We have 4 actions, corresponding to "left", "up", "down", "right"
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
        if self.observation_type == OBS_TYPE_IMAGE:
            arr = self._render_frame(self.render_mode)
            pimg = Image.fromarray(arr, "RGB")
            pimg = pimg.resize((self.cnn_input_size, self.cnn_input_size))
            # pimg.show()
            # exit()
            # print('big image', np.asarray(pimg))

            arr = np.asarray(pimg)
            arr = np.moveaxis(arr, -1, 0)
            return arr
        elif self.observation_type == OBS_TYPE_TEXT:
            state = ""
            #print("visible area\n", self._visibleArea)
            rows = []
            for x in range(0, self.size):
                rows.append([])
                for y in range(0, self.size):
                    rows[x].append(0)

            for x, column in enumerate(self._visibleArea):
                for y, val in enumerate(column):
                    cell = self.normalizeCellTypeText(val)
                    rows[y][x] = cell

            for row in rows:
                for i, cell in enumerate(row):
                    if i == len(row) - 1:
                        state += cell
                    else:
                        state += cell + " "
                state += "\n"

            return state
        else:
            flattenArea = self._getFlattenVisibleArea()
            return {
                "area": np.array(flattenArea),
                "head": self.getNormalizedHeadPos(),
                "food": self.getNormalizedFoodDirection(),
                "direction": self.getNormalizedSnakeDirection(),
            }        
    
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

    def _getFlattenVisibleArea(self):
        flattenArea = []
        for row in self._visibleArea:
            for val in row:
                flattenArea.append(self.normalizeCellType(val))
        return flattenArea


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

    def normalizeCellTypeText(self, cellType):
        if cellType > 7:
            cellType = 7

        if cellType == TYPE_FOOD:
            return "f"
        elif cellType == TYPE_EMPTY:
            return "."
        elif cellType == TYPE_SNAKE:
            return "b"
        elif cellType == TYPE_WALL:
            return "w"
        elif cellType == TYPE_SNAKE_HEAD_UP:
            return "u"
        elif cellType == TYPE_SNAKE_HEAD_RIGHT:
            return "r"
        elif cellType == TYPE_SNAKE_HEAD_DOWN:
            return "d"
        elif cellType == TYPE_SNAKE_HEAD_LEFT:
            return "l"
        else:
            return "0"
    
    def getNormalizedHeadPos(self):
        x = self.norm(self._headPos[0], 0, self.size - 1)
        y = self.norm(self._headPos[1], 0, self.size - 1)
        return np.array([x, y])

    # normalize from -1 to 1
    def norm(self, val, min, max):
        return 2 * ((val - min) / (max - min)) - 1

    def getDistanceToFood(self):
        return np.linalg.norm(np.array(self._headPos) - np.array(self._target_location), ord=1)

    def reset(self):
        # We need the following line to seed self.np_random
        #super().reset()

        self.engine = SnakeEngine((self.size, self.size), random_state=self.random_state)

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

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self.engine.getFoodPosition()

        observation = self._get_obs()

        self._renderer.reset()
        self._renderer.render_step()

        return observation

    def prepareModelAction(self, modelAction):
        return modelAction

    def step(self, action):
        self.snakeUnit.turn(self.prepareModelAction(action))
        self.engine.step()

        doneReason = ""
        done = False
        if self.engine.isFoodReached():
            reward = 1
        elif self.engine.isGameOver():
            doneReason = self.engine.gameEndReason
            if self.render_mode == "human":
                snakeLen = len(self.snakeUnit.snake)
                print('Game over: ', snakeLen)
            reward = -3
            done = True
        else:
            distance = self.getDistanceToFood()
            if distance > self.distanceToFood:
                reward = -0.09
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
            "closed": self.closed,
            "reason": doneReason
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

        if self._drawer is None and (mode == "human" or mode == "rgb_array" or mode == "single_rgb_array"):
            self._drawer = SnakeRenderer(self.window, (self.size, self.size), (self.window_size, self.window_size))

        if mode == "human" or mode == "rgb_array" or mode == "single_rgb_array":
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
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        elif mode == "rgb_array" or mode == "single_rgb_array":
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