import gym
import ant
from stable_baselines3 import DQN
from torchinfo import summary

# Parallel environments
env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="human", visibleArea=10)

model = DQN.load("models/dqn_10", env=env, verbose=1)

# print(model.policy)

obs = env.reset()

print("obs shape", env.observation_space.shape)
# summary(model.policy.q_net, (1, 108))
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