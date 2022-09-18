import gym
import gym_examples

from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env

# Parallel environments
env_name = "gym_examples/MySnake-v0"
env = make_vec_env(env_name, n_envs=1)

model = A2C("MultiInputPolicy", env, verbose=1)

print('before learn')
model.learn(total_timesteps=20)

print('Save model')
model.save("a2c_snake1")

del model # remove to demonstrate saving and loading

model = A2C.load("a2c_snake1")

obs = env.reset()
print('While true')
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()