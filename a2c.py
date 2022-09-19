import gym
import gym_examples
import pygame
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

# Parallel environments
env_name = "gym_examples/MySnake-v0"
# env = gym.make(env_name)
env = gym.make(env_name, render_mode="none")#rgb_array

#env = make_vec_env(env_name, n_envs=1)

# check_env(env)
# print('Env okay')
# exit()

#model = A2C("MultiInputPolicy", env, verbose=1)
model = A2C.load("a2c_snake1", env=env)

print('before learn')
#model.learn(total_timesteps=500000)

print('Save model')
model.save("a2c_snake1")

del model # remove to demonstrate saving and loading
del env

env = gym.make(env_name, render_mode="human")
model = A2C.load("a2c_snake1",env=env)

obs = env.reset()
print('While true')
while True:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)

    if done:
        env.reset()
        continue

    #print('info', info)
    if info["closed"]:
        break
    env.render()

env.close()