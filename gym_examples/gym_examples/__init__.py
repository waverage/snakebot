from gym.envs.registration import register

register(
    id='gym_examples/Grid-v0',
    entry_point='gym_examples.envs:GridEnv',
    max_episode_steps=300,
)

register(
    id='gym_examples/Snake-v0',
    entry_point='gym_examples.envs:SnakeEnv',
    max_episode_steps=300,
)