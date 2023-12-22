from copy import deepcopy
import numpy as np


def file_to_matrix(filename):
    with open(filename) as file:
        lines = file.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        matrix = np.full(shape=(num_rows, num_cols), fill_value=" ", dtype=object)
        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                matrix[i, j] = char
    return matrix


def tilt_line(line, dir="N"):
    while True:
        line_before = deepcopy(line)

        for i in range(len(line) - 1):
            if dir in ("N", "W"):
                bef_index, aft_index = i, i+1
            else:
                bef_index, aft_index = i+1, i

            bef = line[bef_index]
            aft = line[aft_index]

            if bef == "." and aft == "O":
                line[bef_index] = "O"
                line[aft_index] = "."

        if np.all(line_before == line):
            break

    return line


def tilt_matrix(matrix, dir="N"):
    num_rows, num_cols = matrix.shape

    if dir in ("N", "S"):
        num_lines = num_cols
    else:
        num_lines = num_rows

    for i in range(num_lines):
        if dir in ("N", "S"):
            line = matrix[:, i]
            tilted_line = tilt_line(line, dir)
            matrix[:, i] = tilted_line
        else:
            line = matrix[i, :]
            tilted_line = tilt_line(line, dir)
            matrix[i, :] = tilted_line
    return matrix


def get_load(matrix):
    load = 0
    num_rows = matrix.shape[0]
    for i in range(num_rows):
        num_rocks = sum(matrix[i, :] == "O")
        value = num_rocks * (num_rows - i)
        load += value
    return load


def solve1(filename):
    matrix = file_to_matrix(filename)
    matrix = tilt_matrix(matrix)
    load = get_load(matrix)
    return load


def spin(matrix):
    matrix = tilt_matrix(matrix, "N")
    matrix = tilt_matrix(matrix, "W")
    matrix = tilt_matrix(matrix, "S")
    matrix = tilt_matrix(matrix, "E")
    return matrix


def find_pattern(loads):
    N = len(loads)
    for starting_point in range(N):
        max_length = (N - starting_point) // 2 + 1
        for length in range(1, max_length):
            num_patterns = (N - starting_point) // length
            for n in range(num_patterns-1):
                if n == 0:
                    min1 = starting_point
                    max1 = starting_point + length
                    min2 = starting_point + length
                    max2 = starting_point + 2 * length

                pattern1 = loads[min1:max1]
                pattern2 = loads[min2:max2]

                if pattern1 == pattern2:
                    min1 = min2
                    max1 = max2
                    min2 = max1
                    max2 = min2 + length
                else:
                    break

                # all patterns match
                if n == num_patterns - 2:
                    print("Success - pattern found!")
                    return starting_point, pattern2

    print("Failure - no pattern found; increase N.")
    return None, None


def solve2(filename, N=200):
    matrix = file_to_matrix(filename)
    cycle = 0
    loads = [None] * N

    while cycle < N:
        matrix = spin(matrix)
        loads[cycle] = get_load(matrix)
        cycle += 1

    starting_point, pattern = find_pattern(loads)

    if starting_point is not None:
        # How far in the cycle is the last element?
        index = (1_000_000_000 - starting_point) % len(pattern) - 1
        return pattern[index]


print(solve1("data.txt"))
print(solve2("data.txt"))
