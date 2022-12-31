import copy
import numpy as np
import os

filename = os.path.join(os.path.dirname(__file__), "data.txt")


class Blizzard:
    def __init__(self, direction, row, col):
        self.direction = direction
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.direction} ({self.row}, {self.col})"

    def move(self, max_x, max_y):
        if self.direction == ">":
            if self.col == max_y - 1:
                self.col = 1
            else:
                self.col += 1

        elif self.direction == "v":
            if self.row == max_x - 1:
                self.row = 1
            else:
                self.row += 1

        elif self.direction == "<":
            if self.col == 1:
                self.col = max_y - 1
            else:
                self.col -= 1

        elif self.direction == "^":
            if self.row == 1:
                self.row = max_x - 1
            else:
                self.row -= 1


def fill_board(empty_board, blizzards):
    board = copy.copy(empty_board)
    for blizzard in blizzards:
        board[blizzard.row, blizzard.col] = blizzard.direction
    return board


def move_blizzard(blizzards, max_x, max_y):
    for blizzard in blizzards:
        blizzard.move(max_x, max_y)
    return None


def get_neighbours(position, max_x, max_y):
    x, y = position
    if x == 0:
        return [(x, y+1), (x+1, y), (x, y-1)]
    if y == 0:
        return [(x-1, y), (x, y+1), (x+1, y)]
    if x == max_x:
        return [(x-1, y), (x, y+1), (x, y-1)]
    if y == max_y:
        return [(x-1, y), (x+1, y), (x, y-1)]

    return [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]


def read_data(filename):
    empty_board = []
    blizzards = []
    with open(filename) as file:
        i = 0
        for line in file:
            row = [_ for _ in line.rstrip('\n')]
            for col in range(len(row)):
                field = row[col]
                if field != "#" and field != ".":
                    blizzards.append(Blizzard(field, i, col))
                    row[col] = "."
            empty_board.append(row)
            i += 1
    empty_board = np.array(empty_board)
    return empty_board, blizzards


def solve1(empty_board, blizzards, expeditions):
    max_x = empty_board.shape[0] - 1
    max_y = empty_board.shape[1] - 1

    max_row = 0
    rund = 1
    while max_row < max_x:
        move_blizzard(blizzards, max_x, max_y)
        board = fill_board(empty_board, blizzards)
        new_expeditions = []
        for expedition in expeditions:
            neighbours = get_neighbours(expedition, max_x, max_y)
            neighbours.append(expedition)  # don't move
            moves = [neighbour for neighbour in neighbours if board[neighbour] == "."]
            new_expeditions += moves
            new_expeditions = [*set(new_expeditions)]

        expeditions = new_expeditions
        max_row = max([e[0] for e in expeditions])
        rund += 1
    return rund-1


def solve2(empty_board, blizzards, expeditions, destination):
    max_x = empty_board.shape[0] - 1
    max_y = empty_board.shape[1] - 1
    rund = 1
    while True:
        move_blizzard(blizzards, max_x, max_y)
        board = fill_board(empty_board, blizzards)
        new_expeditions = []
        for expedition in expeditions:
            neighbours = get_neighbours(expedition, max_x, max_y)
            neighbours.append(expedition)  # don't move
            moves = [neighbour for neighbour in neighbours if board[neighbour] == "."]
            new_expeditions += moves
            new_expeditions = [*set(new_expeditions)]

        expeditions = new_expeditions
        min_row = min([e[0] for e in expeditions])
        max_row = max([e[0] for e in expeditions])

        if destination == "goal":
            if max_row == max_x:
                break

        if destination == "back":
            if min_row == 0:
                break
        rund += 1
    return rund, blizzards


empty_board, blizzards = read_data(filename)
expeditions = [(0, 1)]
result1 = solve1(empty_board, blizzards, expeditions)
print(result1)  # 311

empty_board, blizzards = read_data(filename)
max_x = empty_board.shape[0] - 1
max_y = empty_board.shape[1] - 1
rund1, blizzards = solve2(empty_board, blizzards, expeditions=[(0, 1)], destination="goal")
rund2, blizzards = solve2(empty_board, blizzards, expeditions=[(max_x, max_y-1)], destination="back")
rund3, blizzards = solve2(empty_board, blizzards, expeditions=[(0, 1)], destination="goal")
result2 = rund1 + rund2 + rund3
print(result2)  # 869
