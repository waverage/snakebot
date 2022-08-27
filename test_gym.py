import gym
env = gym.make("CartPole-v1", new_step_api=True)
observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)

    if done:
        observation, info = env.reset()
env.close()