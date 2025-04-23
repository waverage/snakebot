import gym
from stable_baselines3 import PPO
import gymnasium
import snake_env

# Parallel environments
env_name = "snake_env/SnakeEnv-v0"

env = gymnasium.make(env_name, render_mode="human", visibleArea=10)

model = PPO.load("models/ppo", env=env, verbose=1)

# print(model.policy)

obs, info = env.reset()

print("obs shape", env.observation_space.shape)
# summary(model.policy.q_net, (1, 108))
while True:
    action, _states = model.predict(obs)
    obs, rewards, done, truncated, info = env.step(action)

    if done:
        env.reset()
        continue

    #print('info', info)
    if info["closed"]:
        break
    env.render()

env.close()