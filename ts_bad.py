from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import imageio
import matplotlib
import matplotlib.pyplot as plt
import PIL.Image
import gym
import gym_examples
import random

import numpy as np

import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque

from tensorflow.keras import backend as K
from tf_agents.metrics import tf_metrics
from tf_agents.environments import suite_gym

from tf_agents.agents.categorical_dqn import categorical_dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import categorical_q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tensorflow.keras import optimizers
from tensorflow.keras.utils import to_categorical

# Realization of DQN agent

class DQN:
    def __init__(self, env, params):
        self.action_space = env.action_space
        self.obs_space = env.obs_space
        self.epsilon = params['epsilon']
        self.gamma = params['gamma']
        self.batch_size = params['batch_size']
        self.epsilon_min = params['epsilon_min'] 
        self.epsilon_decay = params['epsilon_decay'] 
        self.learning_rate = params['learning_rate']
        self.layer_sizes = params['layer_sizes']
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        for i in range(len(self.layer_sizes)):
            if i == 0:
                model.add(Dense(self.layer_sizes[i], input_shape=(self.state_space,), activation='relu'))
            else:
                model.add(Dense(self.layer_sizes[i], activation='relu'))
        model.add(Dense(self.action_space, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
class Agent:
    def __init__(self, inp_shape):
        self.inp_shape = inp_shape
        self.model = Sequential()
        self.model.add(Dense(128, activation='relu', input_shape=inp_shape, kernel_initializer='he_normal'))
        self.model.add(Dense(3, activation='softmax'))

        action_prob_placeholder = self.model.output
        action_onehot_placeholder = K.placeholder(shape=(None, 3), name="action_onehot_placeholder")
        discount_reward_placeholder = K.placeholder(shape=(None,), name="discount_reward")

        action_prob = K.sum(action_prob_placeholder * action_onehot_placeholder, axis=1)
        log_action_prob = K.log(action_prob)

        loss = - log_action_prob * discount_reward_placeholder
        loss = K.mean(loss)

        adam = optimizers.Adam(learning_rate=1e-4)

        w = self.model.trainable_weights
        updates = adam.get_updates(params=w,
                                   loss=loss)

        self.train_fn = K.function(
            inputs=[self.model.input,
                    action_onehot_placeholder,
                    discount_reward_placeholder],
            outputs=[],
            updates=updates
        )

    def action(self, state):
        action_prob = np.squeeze(self.model.predict(state))
        return np.random.choice(np.arange(4), p=action_prob), action_prob

    def discounted_reward(self, R, discount_rate=0.99):
        disc_R = np.zeros_like(R, dtype=np.float32)
        running_add = 0

        for t in reversed(range(len(R))):
            running_add = running_add * discount_rate + R[t]
            disc_R[t] = running_add

        disc_R -= disc_R.mean()
        disc_R /= disc_R.std()

        return disc_R

    def fit(self, S, A, R):
        action_onehot = to_categorical(A, num_classes=4)
        self.train_fn([S, action_onehot, self.discounted_reward(R)])

    def run_episode(self, env, verbose=False, render=False):
        S = []
        A = []
        R = []

        done = False
        s = env.reset()

        print('env.reset return s:', s, 'shape: ', s.shape)

        reward_total = 0

        while not done:
            if render:
                env.render()
            a, a_prob = self.action(s.reshape((1,) + self.inp_shape))
            if verbose:
                print(f"ACTION PROB: {a_prob} Action: {env.ACTIONS[a]}")
            s2, r, done, _ = env.step(a)

            reward_total += r

            S.append(s.reshape(self.inp_shape))
            A.append(a)
            R.append(r)

            s = s2

            if done:
                self.fit(np.array(S), np.array(A), np.array(R))

        if verbose:
            print(f"TOTAL REWARD: {reward_total} SNAKE LENGTH: {env.snake_size}")
            print("=================================================================")

        return env.snake_size, reward_total


if __name__ == "__main__":
    agent = Agent((484,))

    env_name = "gym_examples/MySnake-v0"
    env = gym.make(env_name)
    max_length = 0
    episode = 1

    try:
        while True:
            print(f"Episode: {episode}")
            print("=============")
            length, reward = agent.run_episode(env, verbose=True, render=True)
            if length > max_length:
                max_length = length
            episode += 1
    except KeyboardInterrupt:
        print(f"Best score: {max_length}")
        agent.model.save("model.h5")


# num_iterations = 1000

# initial_collect_steps = 1000 
# collect_steps_per_iteration = 1
# replay_buffer_capacity = 100000

# fc_layer_params = (100,)

# batch_size = 64
# learning_rate = 1e-3
# gamma = 0.99
# log_interval = 200

# num_atoms = 51
# min_q_value = -20
# max_q_value = 20
# n_step_update = 2

# num_eval_episodes = 10
# eval_interval = 1000

# train_py_env = suite_gym.load(env_name)
# eval_py_env = suite_gym.load(env_name)

# train_env = tf_py_environment.TFPyEnvironment(train_py_env)
# eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

# print('obs spec', train_env.observation_spec())



train_env.close()
eval_env.close()
exit()
categorical_q_net = categorical_q_network.CategoricalQNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    num_atoms=num_atoms,
    fc_layer_params=fc_layer_params)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

train_step_counter = tf.Variable(0)