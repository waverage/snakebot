from gym.envs.registration import register

register(
    id='ant/Snake-v1',
    entry_point='ant.envs:SnakeEnv',
    max_episode_steps=300,
)