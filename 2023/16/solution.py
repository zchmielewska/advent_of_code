from collections import deque
from copy import deepcopy
import numpy as np


def file_to_matrix(filename):
    with open(filename) as file:
        lines = file.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        matrix = np.full(shape=(num_rows, num_cols), fill_value=" ", dtype=str)
        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                matrix[i, j] = char
    return matrix


def move(beam):
    direction = beam[2]

    if direction == ">":
        moved_beam = (beam[0], beam[1] + 1, beam[2])
    elif direction == "<":
        moved_beam = (beam[0], beam[1] - 1, beam[2])
    elif direction == "^":
        moved_beam = (beam[0] - 1, beam[1], beam[2])
    else:
        moved_beam = (beam[0] + 1, beam[1], beam[2])

    return moved_beam


def change_direction(beam, mirror):
    row, col, direction = beam
    changed_direction = None
    if mirror == "\\":
        if direction == ">":
            changed_direction = "v"
        elif direction == "<":
            changed_direction = "^"
        elif direction == "^":
            changed_direction = "<"
        elif direction == "v":
            changed_direction = ">"
    elif mirror == "/":
        if direction == ">":
            changed_direction = "^"
        elif direction == "<":
            changed_direction = "v"
        elif direction == "^":
            changed_direction = ">"
        elif direction == "v":
            changed_direction = "<"

    return row, col, changed_direction


def count_energized(matrix, initial_beam):
    board = deepcopy(matrix)
    search_queue = deque()
    search_queue.append(initial_beam)

    searched = set()
    energized = set()

    first = True
    while search_queue:
        beam = search_queue.popleft()

        if first:
            beam = move(beam)
            search_queue.appendleft(beam)
            first = False
            continue

        energized.add((beam[0], beam[1]))

        if beam not in searched:
            searched.add(beam)

            board[beam[0], beam[1]] = beam[2]
            item = matrix[(beam[0], beam[1])]

            # move a beam if it's on empty space or splitter with pointy edge
            c1 = item == "."
            c2 = (item == "-") and (beam[2] in (">", "<"))
            c3 = (item == "|") and (beam[2] in ("^", "v"))

            if first or (c1 or c2 or c3):
                beam = move(beam)
                row, col, direction = beam
                if 0 <= row < matrix.shape[0] and 0 <= col < matrix.shape[1]:
                    search_queue.appendleft(beam)

            # if the beam is on the mirror, firstly change direction then move
            if item == "/" or item == "\\":
                beam = change_direction(beam, mirror=item)
                beam = move(beam)
                row, col, direction = beam
                if 0 <= row < matrix.shape[0] and 0 <= col < matrix.shape[1]:
                    search_queue.appendleft(beam)

            # if the beam is on the splitter with flat edge, split beam into two
            c4 = (item == "-") and (beam[2] in ("^", "v"))
            c5 = (item == "|") and (beam[2] in (">", "<"))
            if c4 or c5:
                row, col, direction = beam
                row1, col1, direction1, row2, col2, direction2 = None, None, None, None, None, None
                if c4:
                    row1, col1, direction1 = row, col - 1, "<"
                    row2, col2, direction2 = row, col + 1, ">"
                if c5:
                    row1, col1, direction1 = row - 1, col, "^"
                    row2, col2, direction2 = row + 1, col, "v"

                if 0 <= row1 < matrix.shape[0] and 0 <= col1 < matrix.shape[1]:
                    beam = (row1, col1, direction1)
                    search_queue.appendleft(beam)

                if 0 <= row2 < matrix.shape[0] and 0 <= col2 < matrix.shape[1]:
                    beam = (row2, col2, direction2)
                    search_queue.appendleft(beam)

    result = len(energized)
    return result


def solve1(filename):
    matrix = file_to_matrix(filename)
    initial_beam = (0, -1, ">")
    energized = count_energized(matrix, initial_beam)
    return energized


def solve2(filename):
    matrix = file_to_matrix(filename)
    num_rows, num_cols = matrix.shape

    max_energized = 0
    for x in range(num_rows):
        initial_beam = (x, -1, ">")
        energized = count_energized(matrix, initial_beam)
        max_energized = max(energized, max_energized)

        initial_beam = (x, num_cols, "<")
        energized = count_energized(matrix, initial_beam)
        max_energized = max(energized, max_energized)

    for y in range(num_cols):
        initial_beam = (-1, y, "v")
        energized = count_energized(matrix, initial_beam)
        max_energized = max(energized, max_energized)

        initial_beam = (num_rows, y, "^")
        energized = count_energized(matrix, initial_beam)
        max_energized = max(energized, max_energized)

    return max_energized


print(solve1("data.txt"))
print(solve2("data.txt"))
