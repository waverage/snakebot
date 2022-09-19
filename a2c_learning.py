import gym
import gym_examples
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="none")#rgb_array

#model = A2C("MultiInputPolicy", env, verbose=1)
model = A2C.load("a2c_snake1", env=env)

print('before learn')
model.learn(total_timesteps=500000)

print('Save model')
model.save("a2c_snake1")
