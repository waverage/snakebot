import gym
import gym_examples

env = gym.make('gym_examples/Snake-v0')

observation, info = env.reset(seed=42)
for _ in range(1000):
    env.render()
    #action = policy(observation)  # User-defined policy function
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print('step', observation, info)

    if done:
        observation, info = env.reset()
env.close()