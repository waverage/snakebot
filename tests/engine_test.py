import numpy as np

arr = np.array([
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 7],
    [7, 7, 7, 7, 7, 7],
])

narr = arr[2:5,3:6]

print(narr)