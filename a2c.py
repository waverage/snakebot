import gym
import gym_examples
from stable_baselines3 import A2C

# Parallel environments
env_name = "gym_examples/MySnake-v0"
env = gym.make(env_name, render_mode="human")

model = A2C.load("models/a2c_snake3",env=env)

obs = env.reset()
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