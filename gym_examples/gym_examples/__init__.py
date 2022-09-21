from gym.envs.registration import register

register(
    id='gym_examples/MySnake-v0',
    entry_point='gym_examples.envs:SnakeEnv',
    max_episode_steps=300,
)