from collections import deque
import numpy as np
np.set_printoptions(linewidth=1_000)


def file_to_matrix(filename):
    """Convert text file to matrix of chars"""
    with open(filename) as file:
        lines = file.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        matrix = np.full(shape=(num_rows, num_cols), fill_value=" ", dtype=object)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                matrix[i, j] = Tile(i, j, char)
    return matrix


def cell_exists(i, j, matrix):
    num_rows, num_cols = matrix.shape
    return 0 <= i < num_rows and 0 <= j < num_cols


def is_up_neighbour(pipe1, pipe2):
    c1 = pipe1 in ["|", "L", "J"]
    c2 = pipe2 in ["|", "7", "F"]
    return c1 and c2


def is_dn_neighbour(pipe1, pipe2):
    c1 = pipe1 in ["|", "7", "F"]
    c2 = pipe2 in ["|", "L", "J"]
    return c1 and c2


def is_lt_neighbour(pipe1, pipe2):
    c1 = pipe1 in ["-", "J", "7"]
    c2 = pipe2 in ["-", "L", "F"]
    return c1 and c2


def is_rt_neighbour(pipe1, pipe2):
    c1 = pipe1 in ["-", "L", "F"]
    c2 = pipe2 in ["-", "J", "7"]
    return c1 and c2


class Tile:
    def __init__(self, row, col, pipe):
        self.row = row
        self.col = col
        self.pipe = pipe

    def __repr__(self):
        return self.pipe

    def get_neighbours(self, matrix):
        """There are 4 potential neighbours"""
        neighbours = []

        # up
        i, j = self.row - 1, self.col
        if cell_exists(i, j, matrix):
            other = matrix[i, j]
            if is_up_neighbour(self.pipe, other.pipe):
                neighbours.append(other)

        # dn
        i, j = self.row + 1, self.col
        if cell_exists(i, j, matrix):
            other = matrix[i, j]
            if is_dn_neighbour(self.pipe, other.pipe):
                neighbours.append(other)

        # lt
        i, j = self.row,  self.col - 1
        if cell_exists(i, j, matrix):
            other = matrix[i, j]
            if is_lt_neighbour(self.pipe, other.pipe):
                neighbours.append(other)

        # rt
        i, j = self.row, self.col + 1
        if cell_exists(i, j, matrix):
            other = matrix[i, j]
            if is_rt_neighbour(self.pipe, other.pipe):
                neighbours.append(other)

        return neighbours


def get_starting_tile(matrix):
    for i, row in enumerate(matrix):
        for j, tile in enumerate(row):
            if tile.pipe == "S":
                return matrix[i, j]


def get_loop(starting_tile, matrix):
    loop = {starting_tile}
    search_queue = deque()
    search_queue += starting_tile.get_neighbours(matrix)
    while search_queue:
        tile = search_queue.popleft()
        if tile not in loop:
            loop.add(tile)
            search_queue += tile.get_neighbours(matrix)
    return loop


def solve1(filename):
    matrix = file_to_matrix(filename)
    starting_tile = get_starting_tile(matrix)
    starting_tile.pipe = "-"
    loop = get_loop(starting_tile, matrix)
    return len(loop)/2


def solve2(filename):
    matrix = file_to_matrix(filename)
    starting_tile = get_starting_tile(matrix)
    starting_tile.pipe = "-"
    loop = get_loop(starting_tile, matrix)

    _map = np.full(shape=matrix.shape, fill_value=" ", dtype=str)
    for tile in loop:
        i, j = tile.row, tile.col
        _map[i, j] = tile.pipe

    for i in range(_map.shape[0]):
        for j in range(_map.shape[1]):
            if _map[i, j] == " ":
                pipes_lt = np.sum(np.isin(_map[i, :j], ["|", "L", "J"]))
                if pipes_lt % 2 != 0:
                    _map[i, j] = "I"

    return np.sum(_map == "I")


print(solve1("data.txt"))
print(solve2("data.txt"))
