import gym
import gym_examples

env = gym.make('gym_examples/MySnake-v0')

observation, head, info = env.reset(seed=42)
for _ in range(1000):
    env.render()
    #action = policy(observation)  # User-defined policy function
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print("step\n", observation["area"], info)

    if done:
        observation, head, info = env.reset()
env.close()