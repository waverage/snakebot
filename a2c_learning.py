import gym
import gym_examples
from stable_baselines3 import A2C
import os.path

env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="none")#rgb_array
model_name = 'a2c_snake5'

if os.path.isfile(model_name + '.zip'):
    model = A2C.load(model_name, env=env)
else:
    model = A2C("MultiInputPolicy", env, verbose=1)


model.learn(total_timesteps=100000)
model.save(model_name)
