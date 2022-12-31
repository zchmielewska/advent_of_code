import copy
import numpy as np


class Tetris:
    def __init__(self, blocks, grid):
        self.blocks = blocks
        self.block_num = 0
        self.block = blocks[0]
        self.grid = grid
        self.empty_grid = grid
        self.board = np.concatenate((blocks[0], grid))
        self.active_row = self.block.shape[0]-1
        self.counter = 1

    def push(self, direction):
        if direction == "<":
            # I can't push left, if it touches left border
            if any(self.board[:, 0] == 1):
                return None

            only_block = copy.deepcopy(self.board)
            only_block[only_block != 1] = 0
            zeros = np.zeros([self.board.shape[0], 1])
            only_block_left = np.hstack((only_block[:, 1:], zeros))

            board_without_block = copy.deepcopy(self.board)
            board_without_block[board_without_block == 1] = 0

            # Can I move to the left without colision?
            if np.any(board_without_block + only_block_left == 3):
                # there is a colision
                return None
            else:
                # no colision
                self.board = board_without_block + only_block_left

        elif direction == ">":
            # I can't push right, if it touches right border
            if any(self.board[:, -1] == 1):
                return None

            only_block = copy.deepcopy(self.board)
            only_block[only_block != 1] = 0
            zeros = np.zeros([self.board.shape[0], 1])
            only_block_right = np.hstack((zeros, only_block[:, :-1]))

            board_without_block = copy.deepcopy(self.board)
            board_without_block[board_without_block == 1] = 0

            # Can I move to the right without colision?
            if np.any(board_without_block + only_block_right == 3):
                # there is a colision
                return None
            else:
                # no colision
                self.board = board_without_block + only_block_right

    def fall(self):
        # board has only one row
        if self.board.shape[0] == 1:
            self.board[self.board == 1] = 2
            self.board = np.concatenate((self.empty_grid, self.board))
            self.block_num = (self.block_num + 1) % 5
            self.block = self.blocks[self.block_num]
            self.board = np.concatenate((self.block, self.board))
            self.active_row = self.block.shape[0]-1
            self.counter += 1
        else:
            # is there anything below the figure?
            block_last_row_cols = self.board[self.active_row, ] == 1

            if self.active_row == self.board.shape[0]-1:  # block touches floor
                below_empty = False
            else:
                below_empty = sum(self.board[self.active_row+1, block_last_row_cols]) == 0

            if below_empty:
                only_block = copy.deepcopy(self.board)
                only_block[only_block != 1] = 0
                zeros = np.zeros([1, 7])
                only_block_lowered = np.concatenate((zeros, only_block[:-1, ]))

                # clean board from block
                self.board[self.board == 1] = 0

                # add lowered block
                self.board = self.board + only_block_lowered

                # remove first line if consists only of zeros
                if sum(self.board[0, ]) == 0:
                    self.board = self.board[1:, ]
                else:
                    self.active_row += 1

            else:
                # 2 = fixed block
                self.board[self.board == 1] = 2
                self.board = np.concatenate((self.empty_grid, self.board))
                self.block_num = (self.block_num + 1) % 5
                self.block = self.blocks[self.block_num]
                self.board = np.concatenate((self.block, self.board))
                self.active_row = self.block.shape[0]-1
                self.counter += 1
                # print("counter:", self.counter)
                # print(self.board)


block1 = np.array([
    [0, 0, 1, 1, 1, 1, 0],
])

block2 = np.array([
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
])

block3 = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
])

block4 = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
])

block5 = np.array([
    [0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0],
])

blocks = [block1, block2, block3, block4, block5]


grid = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

filename = "./input/17/example.txt"
filename = "./input/17/data.txt"
with open(filename) as file:
    for line in file:
        pushes = line

directions = [_ for _ in pushes]

tetris = Tetris(blocks, grid)
print(tetris.board, "\n")

i = 0
while tetris.counter <= 2022:
    # print("i =", i)
    # print("active_row:", tetris.active_row)
    # print(tetris.board, "\n")

    direction = directions.pop(0)
    directions.append(direction)
    tetris.push(direction)
    # print(direction)
    # print(tetris.board, "\n")

    tetris.fall()
    # print("v")
    # print(tetris.board, "\n")
    # print("counter:", tetris.counter, "\n")
    i += 1

print(tetris.board.shape)