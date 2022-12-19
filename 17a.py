import numpy as np


class Tetris:
    def __init__(self, shape, grid):
        self.shape = shape
        self.grid = grid


class Block:
    def __init__(self, shape):
        self.shape = shape

    def move(self, direction):
        if direction == "<":
            if self.shape.ndim == 1:
                if self.shape[0] == 0:
                    for i in range(len(self.shape) - 1):
                        self.shape[i] = self.shape[i+1]
            else:
                if sum(self.shape[:, 0]) == 0:
                    for col in range(self.shape.shape[1] - 1):
                        self.shape[:, col] = self.shape[:, col+1]

        elif direction == ">":
            if self.shape.ndim == 1:
                if self.shape[-1] == 0:
                    for i in range(len(self.shape)-1, 0, -1):
                        self.shape[i] = self.shape[i - 1]
            else:
                if sum(self.shape[:, -1]) == 0:
                    for col in range(self.shape.shape[1]-1, 0, -1):
                        self.shape[:, col] = self.shape[:, col - 1]


shape1 = np.array(
    [0, 0, 1, 1, 1, 1, 0],
)

shape2 = np.array([
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
])

shape3 = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
])

shape4 = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
])

shape5 = np.array([
    [0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0],
])

shapes = [shape1, shape2, shape3, shape4, shape5]

grid = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

