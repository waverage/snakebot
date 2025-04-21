import gym
import ant
import gptbot

# Parallel environments
env_name = "ant/Snake-v1"
env = gym.make(env_name, render_mode="human", size=7, visibleArea=7, observation_type="text", window_size=270)


obs = env.reset()

print("obs shape", env.observation_space.shape)

bot = gptbot.ChatGptBot()

while True:
    action = bot.predict(obs)
    obs, rewards, done, info = env.step(action)

    if done:
        env.reset()
        bot.punch(info["reason"])
        continue

    #print('info', info)
    if info["closed"]:
        break
    env.render()

env.close()

