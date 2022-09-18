from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import imageio
# import IPython
import matplotlib
import matplotlib.pyplot as plt
import PIL.Image
#import pyvirtualdisplay

import tensorflow as tf
import tf_agents
from tf_agents.metrics import tf_metrics
from tf_agents.environments import suite_gym

from tf_agents.agents.categorical_dqn import categorical_dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils

from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import categorical_q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

import gym_examples

env_name = "gym_examples/MySnake-v0"

num_iterations = 15000 # @param {type:"integer"}

initial_collect_steps = 1000 
collect_steps_per_iteration = 1  # @param {type:"integer"}
replay_buffer_capacity = 100000  # @param {type:"integer"}

fc_layer_params = (100,)

batch_size = 64  # @param {type:"integer"}
learning_rate = 1e-3  # @param {type:"number"}
gamma = 0.99
log_interval = 200  # @param {type:"integer"}

num_atoms = 51  # @param {type:"integer"}
min_q_value = -20  # @param {type:"integer"}
max_q_value = 20  # @param {type:"integer"}
n_step_update = 2  # @param {type:"integer"}

num_eval_episodes = 10  # @param {type:"integer"}
eval_interval = 1000  # @param {type:"integer"}

train_py_env = suite_gym.load(env_name)
eval_py_env = suite_gym.load(env_name)

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

# utils.validate_py_environment(train_env, episodes=5)

# exit()
simplySpace = tf_agents.environments.gym_wrapper.spec_from_gym_space(train_env.observation_spec())

print('=====================')
print('Observation spec', train_env.observation_spec())
print('Converted space:', simplySpace)
print('=====================')

categorical_q_net = categorical_q_network.CategoricalQNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    num_atoms=num_atoms,
    fc_layer_params=fc_layer_params,
    preprocessing_combiner=tf.keras.layers.Concatenate(axis=-1),
    preprocessing_layers=(tf.keras.layers.Layer(), tf.keras.layers.Layer(), tf.keras.layers.Layer()),
    #preprocessing_layers=tf.nest.map_structure(lambda _: tf.keras.layers.Layer(), train_env.observation_spec())
)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

train_step_counter = tf.Variable(0)

print('=====================')
print('time_step_spec', train_env.time_step_spec())
print('action spec', train_env.action_spec())
print('=====================')

agent = categorical_dqn_agent.CategoricalDqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    categorical_q_network=categorical_q_net,
    optimizer=optimizer,
    min_q_value=min_q_value,
    max_q_value=max_q_value,
    n_step_update=n_step_update,
    td_errors_loss_fn=common.element_wise_squared_loss,
    gamma=gamma,
    train_step_counter=train_step_counter)
agent.initialize()

train_env.close()
eval_env.close()
exit()