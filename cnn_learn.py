import gym
import ant
from stable_baselines3 import DQN
import os.path
import torch as th
from typing import Callable

# def linear_schedule(initial_value: float) -> Callable[[float], float]:
#     def func(progress_remaining: float) -> float:
#         left = 1 - progress_remaining
#         left = left / 2
#         left = 1 - left
#         return left * initial_value

#     return func

env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="none", visibleArea=10)
model_name = 'cnn_10'

model_path = 'models/' + model_name + '.zip'
if os.path.isfile(model_path):
    model = DQN.load(model_path, env=env)
else:
    # Custom actor (pi) and value function (vf) networks
    # of two layers of size 32 each with Relu activation function
    # Note: an extra linear layer will be added on top of the pi and the vf nets, respectively
    policy_kwargs = dict(
        net_arch=[128, 128]
    )
    model = DQN(
        "CnnPolicy",
        env,
        verbose=1,
        # learning_starts=10000,
        # policy_kwargs=policy_kwargs,
        # learning_rate=linear_schedule(0.0001),
        # buffer_size=100_000,
        # batch_size=32,
        # gradient_steps=1,
        # target_update_interval=10_000,
        # exploration_fraction=0.1,
        # exploration_final_eps=0.05,
    )


model.learn(total_timesteps=500000)
model.save(model_path)
