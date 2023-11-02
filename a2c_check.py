import gym
import ant
from stable_baselines3.common.env_checker import check_env

# Parallel environments
env_name = "ant/Snake-v1"
# env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="human", visibleArea=10)

check_env(env)

print('Ok')