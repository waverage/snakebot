import gym
env = gym.make("LunarLander-v2")

def policy(observation):
    return (0, 0, 0, 0)

observation, info, d, r, s, a, r, w = env.reset(seed=42)
for _ in range(1000):
   env.render()
   #action = policy(observation)  # User-defined policy function
   action = env.action_space.sample()
   observation, reward, done, info = env.step(action)

   if done:
      observation, info, d, r, s, a, r, w = env.reset()
env.close()