from gym import spaces

d = spaces.Discrete(4)
b = spaces.MultiBinary(4)

print(d.sample())

print("binary", b.sample())