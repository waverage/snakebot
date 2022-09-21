import gym
import gym_examples
from stable_baselines3 import A2C
import os.path

env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="none")#rgb_array
model_name = 'a2c_3'

model_path = 'models/' + model_name + '.zip'
if os.path.isfile(model_path):
    model = A2C.load(model_path, env=env)
else:
    model = A2C("MultiInputPolicy", env, verbose=1)


model.learn(total_timesteps=10000)
model.save(model_path)
