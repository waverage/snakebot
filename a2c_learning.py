import gym
import ant
from stable_baselines3 import A2C
import os.path
from typing import Callable
import torch as th

def linear_schedule(initial_value: float) -> Callable[[float], float]:
    """
    Linear learning rate schedule.

    :param initial_value: Initial learning rate.
    :return: schedule that computes
      current learning rate depending on remaining progress
    """
    def func(progress_remaining: float) -> float:
        """
        Progress will decrease from 1 (beginning) to 0.

        :param progress_remaining:
        :return: current learning rate
        """
        left = 1 - progress_remaining
        left = left / 2
        left = 1 - left
        return left * initial_value

    return func

env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="none", visibleArea=10)#rgb_array
model_name = 'a2c_10'

model_path = 'models/' + model_name + '.zip'
if os.path.isfile(model_path):
    model = A2C.load(model_path, env=env)
else:
    # Custom actor (pi) and value function (vf) networks
    # of two layers of size 32 each with Relu activation function
    # Note: an extra linear layer will be added on top of the pi and the vf nets, respectively
    policy_kwargs = dict(
        activation_fn=th.nn.ReLU,
        net_arch=[dict(pi=[512, 512], vf=[128, 128])]
    )
    model = A2C(
        "MultiInputPolicy",
        env,
        policy_kwargs=policy_kwargs,
        verbose=1,
        learning_rate=linear_schedule(0.00003),
        n_steps=10,
    )


model.learn(total_timesteps=400000)
model.save(model_path)
