import gym
import gym_examples

env = gym.make('gym_examples/Grid-v0')

observation, info = env.reset(seed=42)
for _ in range(1000):
    print('step')
    env.render()
    #action = policy(observation)  # User-defined policy function
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)

    if done:
        observation, info = env.reset()
env.close()