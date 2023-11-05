import gym
import ant
from stable_baselines3 import DQN
import os.path
import torch as th
from typing import Callable
import torch as th
import torch.nn as nn
from gym import spaces
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

# n_input_channels = observation_space.shape[0]
# self.cnn = nn.Sequential(
#     nn.Conv2d(n_input_channels, 32, kernel_size=8, stride=4, padding=0),
#     nn.ReLU(),
#     nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
#     nn.ReLU(),
#     nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=0),
#     nn.ReLU(),
#     nn.Flatten(),
# )

# # Compute shape by doing one forward pass
# with th.no_grad():
#     n_flatten = self.cnn(th.as_tensor(observation_space.sample()[None]).float()).shape[1]

# self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

class CustomCNN(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: spaces.Box, features_dim: int = 256):
        super().__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        n_input_channels = observation_space.shape[0]
        print("n_input_channels", n_input_channels)

        print("features_dim", features_dim)
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=2, stride=1, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        # print('n_flatten', n_flatten)
        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))

env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="rgb_array", visibleArea=10)
model_name = 'cnn_10'

model_path = 'models/' + model_name + '.zip'
# if os.path.isfile(model_path):
#     model = DQN.load(model_path, env=env)
# else:
# Custom actor (pi) and value function (vf) networks
# of two layers of size 32 each with Relu activation function
# Note: an extra linear layer will be added on top of the pi and the vf nets, respectively
# policy_kwargs = dict(
#     net_arch=[128, 128]
# )
# policy_kwargs = dict(
#     features_extractor_class=CustomCNN,
#     features_extractor_kwargs=dict(features_dim=128),
# )
model = DQN(
    "CnnPolicy",
    env,
    verbose=1,
    # policy_kwargs=policy_kwargs,
    learning_starts=10000,
    device=th.device("mps"),
    # learning_rate=0.1,
    # policy_kwargs=policy_kwargs,
    # learning_rate=linear_schedule(0.0001),
    buffer_size=10_000,
    # batch_size=32,
    # gradient_steps=1,
    # target_update_interval=10_000,
    # exploration_fraction=0.1,
    # exploration_final_eps=0.05,
)


model.learn(total_timesteps=500000)
model.save(model_path)
