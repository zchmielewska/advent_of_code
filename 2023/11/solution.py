from itertools import combinations
import numpy as np
np.set_printoptions(linewidth=1_000)


def file_to_matrix(filename):
    """Convert text file to matrix of chars"""
    with open(filename) as file:
        lines = file.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        matrix = np.full(shape=(num_rows, num_cols), fill_value=" ", dtype=str)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                matrix[i, j] = char
    return matrix


def expand_universe(universe):
    num_rows, num_cols = universe.shape
    for i in range(num_rows-1, -1, -1):
        if np.all(universe[i, :] == '.'):
            new_row = np.full((1, num_cols), '.', dtype=str)
            universe = np.insert(universe, i, new_row, axis=0)

    num_rows, num_cols = universe.shape
    for j in range(num_cols-1, -1, -1):
        if np.all(universe[:, j] == '.'):
            new_col = np.full((1, num_rows), '.', dtype=str)
            universe = np.insert(universe, j, new_col, axis=1)
    return universe


def get_shortest_path(galaxy1, galaxy2):
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])


def solve1(filename):
    universe = file_to_matrix(filename)
    universe = expand_universe(universe)
    indices = np.transpose(np.where(universe == "#"))
    galaxies = [tuple(index) for index in indices]
    pairs = list(combinations(galaxies, 2))
    shortest_paths = [get_shortest_path(pair[0], pair[1]) for pair in pairs]
    return sum(shortest_paths)


def prepare_universe(universe):
    num_rows, num_cols = universe.shape

    row_indices = []
    for i in range(num_rows):
        if np.all(universe[i, :] == '.'):
            row_indices.append(i)

    col_indices = []
    for j in range(num_cols):
        if np.all(universe[:, j] == '.'):
            col_indices.append(j)

    universe[row_indices, :] = "_"
    universe[:, col_indices] = "_"

    return universe


def get_distance(galaxy1, galaxy2, universe):
    n = 1_000_000

    i1, j1 = galaxy1
    i2, j2 = galaxy2

    min_i = min(i1, i2)
    max_i = max(i1, i2)
    min_j = min(j1, j2)
    max_j = max(j1, j2)

    path1 = universe[min_i:(max_i+1), min_j]
    path2 = universe[max_i, min_j:(max_j+1)]

    result = 0
    result += np.sum(np.count_nonzero(path1 == "."))
    result += np.sum(np.count_nonzero(path1 == "#"))
    result += np.sum(np.count_nonzero(path1 == "_")) * n
    result += np.sum(np.count_nonzero(path2 == "."))
    result += np.sum(np.count_nonzero(path2 == "#"))
    result += np.sum(np.count_nonzero(path2 == "_")) * n

    return result - 2


def solve2(filename):
    universe = file_to_matrix(filename)
    universe = prepare_universe(universe)
    indices = np.transpose(np.where(universe == "#"))
    galaxies = [tuple(index) for index in indices]
    pairs = list(combinations(galaxies, 2))

    result = np.float64(0)
    for pair in pairs:
        result += get_distance(pair[0], pair[1], universe)

    return result


print(solve1("data.txt"))
print(solve2("data.txt"))
