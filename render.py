import gym
import ant

# Parallel environments
env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="human", visibleArea=10, observation_type="image", window_size=270)


obs = env.reset()

while True:
    action = env.action_space.sample()
    obs, rewards, done, info = env.step(action)

    if done:
        env.reset()
        continue

    #print('info', info)
    if info["closed"]:
        break
    env.render()

env.close()