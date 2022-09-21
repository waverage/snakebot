import numpy as np

arr = [
    [0, 0, 0, 7],
    [0, 0, 0, 7],
    [0, 1, 4, 7],
    [0, 0, 0, 7],
    [6, 0, 0, 7]
]

r = np.pad(arr, ((0, 0), (0, 1)), 'constant', constant_values=0)
print('r', r)

def pad(a, size, x0, x1, y0, y1):
    return a

x0 = 3
x1 = 8
y0 = 6
y1 = 11
size = (10, 10)

r = pad(arr, size, x0, x1, y0, y1)

# print('Result', r)