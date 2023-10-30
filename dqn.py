import gym
import ant
from stable_baselines3 import DQN

# Parallel environments
env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="human", visibleArea=10)

model = DQN.load("models/dqn_10", env=env, verbose=1)

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