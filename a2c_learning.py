import gym
import gym_examples
from stable_baselines3 import A2C

env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="none")#rgb_array

#model = A2C("MultiInputPolicy", env, verbose=1)
model = A2C.load("a2c_snake10", env=env)

model.learn(total_timesteps=10000000)
model.save("a2c_snake10")
