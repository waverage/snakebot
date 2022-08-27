#import tensorflow as tf
import numpy as np

TURN_UP = 0
TURN_RIGHT = 1
TURN_DOWN = 2
TURN_LEFT = 3
DO_NOTHING = 4

# Input - features
# 1. 9x9 cells around the snake's head
# 000000000
# 000000000
# 000003000
# 000000000
# 001110000
# 000000000
# 000000000
# 000000000
# 000000000
#
# 2. Snake len
#
# 3. Snake direction
#        UP 0  
# LEFT 3       RIGHT 1
#       DOWN 2
#
#
# 4. Food smell. If food is near then value is big, when food far from snake then value is low
# 
#
# Outputs - labels?
# 1. Turn up
# 2. Turn right
# 3. Turn down
# 4. Turn left
# 5. Do nothing
#
class SnakeAgent:
    def __init__(self):      
        numParameters = 9 * 9 + 1 + 4 + 1
        # self.m = tf.keras.Sequential([
        #     tf.keras.layers.Input(shape=(numParameters,)),
        #     tf.keras.layers.Flatten(),
        #     tf.keras.layers.Dense(numParameters),
        #     tf.keras.layers.Dense(128, activation='relu'),
        #     tf.keras.layers.Dense(512, activation='relu'),
        #     tf.keras.layers.Dense(1024, activation='relu'),
        #     tf.keras.layers.Dense(128, activation='relu'),
        #     tf.keras.layers.Dense(5, activation='softmax')
        # ])

    def makeDecision(self):
        return 4