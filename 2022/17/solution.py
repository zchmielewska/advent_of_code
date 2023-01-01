import copy
import numpy as np
import os
import time


filename = os.path.join(os.path.dirname(__file__), "data.txt")


class Tetris:
    def __init__(self, blocks, grid):
        self.blocks = blocks
        self.block_num = 0
        self.block = blocks[0]
        self.grid = grid
        self.empty_grid = grid
        self.board = np.concatenate((blocks[0], grid))
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
            self.board[self.board == 1] = 2  # 2 = fixed block
            self.counter += 1
            return True

        else:
            only_block = copy.deepcopy(self.board)
            only_block[only_block != 1] = 0
            zeros = np.zeros([1, 7])
            only_block_down = np.concatenate((zeros, only_block[:-1, :]))
            board_without_block = copy.deepcopy(self.board)
            board_without_block[board_without_block == 1] = 0

            # Can I move down without colision?
            touches_floor = np.any(self.board[[-1], ] == 1)
            if np.any(board_without_block + only_block_down == 3) or touches_floor:
                # There is a colision --> fix the board
                self.board[self.board == 1] = 2  # 2 = fixed block
                self.counter += 1
                return True
            else:
                # No colision --> go down
                self.board = board_without_block + only_block_down
                # Remove first line if consists only of zeros
                if sum(self.board[0, ]) == 0:
                    self.board = self.board[1:, ]
                return False

    def start_new_block(self):
        self.board = np.concatenate((self.empty_grid, self.board))
        self.block_num = (self.block_num + 1) % 5
        self.block = self.blocks[self.block_num]
        self.board = np.concatenate((self.block, self.board))


def get_blocks():
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
    return blocks


def get_grid():
    grid = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])
    return grid


def get_directions(filename):
    with open(filename) as file:
        for line in file:
            pushes = line

    directions = [_ for _ in pushes]
    return directions


def get_height(array):
    height = 0
    for x in array:
        if x == 0:
            height += 1
        else:
            return height
    return height


def solve1(filename):
    blocks = get_blocks()
    grid = get_grid()
    directions = get_directions(filename)
    tetris = Tetris(blocks, grid)

    direction_index = 0
    felt = False
    while tetris.counter <= 2022:
        if felt:
            tetris.start_new_block()

        direction = directions[direction_index]
        tetris.push(direction)
        felt = tetris.fall()

        if direction_index == len(directions)-1:
            direction_index = 0
        else:
            direction_index += 1

    top_rows = 0
    result = tetris.board.shape[0] - top_rows
    return result


def solve2(filename):
    blocks = get_blocks()
    grid = get_grid()
    directions = get_directions(filename)
    tetris = Tetris(blocks, grid)

    direction_index = 0
    felt = False
    visited_states = []
    metadata = []
    check_states = True
    while tetris.counter <= 10**12:
        if felt:
            if check_states:
                # Save state of the game after the block has felt
                heights = [get_height(tetris.board[:, i]) for i in range(7)]
                min_height = min(heights)
                relative_heights = [height - min_height for height in heights]
                state = (relative_heights, tetris.block_num, direction_index)
                if state in visited_states:
                    current_height = tetris.board.shape[0]
                    current_counter = tetris.counter
                    index = visited_states.index(state)
                    past_height = metadata[index][0]
                    past_counter = metadata[index][1]

                    # How many cycles will fit until the end?
                    delta_height = current_height - past_height
                    delta_counter = current_counter - past_counter

                    remaining_counters = 10**12 - current_counter
                    remaining_full_cycles = remaining_counters // delta_counter

                    height_in_cycles = remaining_full_cycles * delta_height
                    tetris.counter += remaining_full_cycles * delta_counter
                    check_states = False
                else:
                    visited_states.append(state)
                    metadata.append((tetris.board.shape[0], tetris.counter))

            # Start new round
            tetris.start_new_block()

        # Play tetris
        direction = directions[direction_index]
        tetris.push(direction)
        felt = tetris.fall()
        if direction_index == len(directions)-1:
            direction_index = 0
        else:
            direction_index += 1

    result = tetris.board.shape[0] + height_in_cycles
    return result


print(solve1(filename))  # 3184
print(solve2(filename))  # 1577077363915
