import gym
import gym_examples
from stable_baselines3.common.env_checker import check_env

# Parallel environments
env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="human")

check_env(env)

print('Ok')