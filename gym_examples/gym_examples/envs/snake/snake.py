import gym
from gym import spaces
from gym.utils.renderer import Renderer
import pygame
import numpy as np
import math
from gym_examples.envs.snake.engine import SnakeEngine
from gym_examples.envs.snake.snake_unit import SnakeUnit
from gym_examples.envs.snake.wall import Wall
from gym_examples.envs.snake.render import SnakeRenderer

#from snake_unit import SnakeUnit

class SnakeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "single_rgb_array"], "render_fps": 4}

    def __init__(self, render_mode='human', size=10):
        self.size = size  # The size of the square grid
        self.window_size = 720  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
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
        return {
            "agent": self._agentArr,
            "target": self._target_location
        }

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                np.array(self._agent_location) - np.array(self._target_location), ord=1
            )
        }

    def reset(self, seed=None, return_info=False, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.engine = SnakeEngine((self.size, self.size))

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

        self._agentArr = self.snakeUnit.getArr()

        # Choose the agent's location uniformly at random
        self._agent_location = self.snakeUnit.getHeadPos() #self.np_random.integers(0, self.size, size=2, dtype=int)
        print('')
        print('Agent arr', self._agentArr)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self.engine.getFoodPosition()

        observation = self._get_obs()
        info = self._get_info()

        self._renderer.reset()
        self._renderer.render_step()

        return (observation, info) if return_info else observation

    def step(self, action):
        self.snakeUnit.turn(action)
        self.engine.step()

        done = self.engine.isFoodReached()

        done = False
        if self.engine.isFoodReached():
            reward = 1
        elif self.engine.isGameOver():
            reward = -1
            done = True
            print('Game end')
        else:
            reward = 0

        self._agentArr = self.snakeUnit.getArr()
        self._agent_location = self.snakeUnit.getHeadPos()
        self._target_location = self.engine.getFoodPosition()

        observation = self._get_obs()
        info = self._get_info()

        self._renderer.render_step()

        return observation, reward, done, info

    def render(self):
        return self._renderer.get_renders()

    def _render_frame(self, mode):
        assert mode is not None

        if self.window is None and mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and mode == "human":
            self.clock = pygame.time.Clock()

        if self._drawer is None and mode == "human":
            self._drawer = SnakeRenderer(self.window, (self.size, self.size), (self.window_size, self.window_size))

        canvas = self._drawer.draw(self.engine.getMatrix())

        if mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()