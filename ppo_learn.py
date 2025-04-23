import gym
from stable_baselines3 import PPO
import os.path
import torch as th
from typing import Callable
import gymnasium
import snake_env

def linear_schedule(initial_value: float) -> Callable[[float], float]:
    def func(progress_remaining: float) -> float:
        left = 1 - progress_remaining
        left = left / 2
        left = 1 - left
        return left * initial_value

    return func

env_name = "snake_env/SnakeEnv-v0"
env = gymnasium.make(env_name, render_mode="none", visibleArea=10)
model_name = 'ppo'

model_path = 'models/' + model_name + '.zip'
if os.path.isfile(model_path):
    model = PPO.load(model_path, env=env)
else:
    # Custom actor (pi) and value function (vf) networks
    # of two layers of size 32 each with Relu activation function
    # Note: an extra linear layer will be added on top of the pi and the vf nets, respectively
    policy_kwargs = dict(
        net_arch=[128, 128]
    )
    model = PPO(
        "MultiInputPolicy",
        env,
        verbose=1,
        policy_kwargs=policy_kwargs,
        # learning_rate=linear_schedule(0.0001),
    )


model.learn(total_timesteps=100000)
model.save(model_path)
