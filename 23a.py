import copy
import numpy as np

filename = "./input/23/data.txt"
DEBUG = False


def propose(position, elves, case):
    x, y = position

    # No neighbours around
    neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                  (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
                  (x, y - 1), (x, y + 1)]
    if not any(value in elves for value in neighbours):
        return x, y

    if case == 0:
        # North
        neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x - 1, y

        # South
        neighbours = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x + 1, y

        # West
        neighbours = [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
        if not any(value in elves for value in neighbours):
            return x, y - 1

        # East
        neighbours = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x, y + 1

    if case == 1:
        # South
        neighbours = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x + 1, y

        # West
        neighbours = [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
        if not any(value in elves for value in neighbours):
            return x, y - 1

        # East
        neighbours = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x, y + 1

        # North
        neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x - 1, y

    if case == 2:
        # West
        neighbours = [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
        if not any(value in elves for value in neighbours):
            return x, y - 1

        # East
        neighbours = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x, y + 1

        # North
        neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x - 1, y

        # South
        neighbours = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x + 1, y

    if case == 3:
        # East
        neighbours = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x, y + 1

        # North
        neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x - 1, y

        # South
        neighbours = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if not any(value in elves for value in neighbours):
            return x + 1, y

        # West
        neighbours = [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
        if not any(value in elves for value in neighbours):
            return x, y - 1

    return x, y


def normalize(position, min_x, min_y):
    x, y = position
    return x - min_x, y - min_y


def get_size(elves):
    xs = [position[0] for position in elves]
    ys = [position[1] for position in elves]
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)
    return min_x, min_y, max_x, max_y


elves = []
with open(filename) as file:
    i = 0
    for line in file:
        row = [_ for _ in line.rstrip('\n')]
        cols = np.where(np.array(row) == "#")[0]
        for col in cols:
            elves.append((i, col))
        i += 1

if DEBUG:
    print("At the beginning")
    print(elves)
    min_x, min_y, max_x, max_y = get_size(elves)
    board = np.full((max_x+1, max_y+1), ".")

    for elf in elves:
        board[elf[0], elf[1]] = "#"
    print(board)

for rund in range(10):
    confirmed = []
    case = rund % 4
    proposed = [propose(position, elves, case) for position in elves]
    for i in range(len(elves)):
        if proposed.count(proposed[i]) == 1:
            confirmed.append(proposed[i])
        else:
            confirmed.append(elves[i])
    elves = copy.copy(confirmed)

    if DEBUG:
        min_x, min_y, max_x, max_y = get_size(elves)
        elves = [normalize(position, min_x, min_y) for position in elves]
        min_x, min_y, max_x, max_y = get_size(elves)
        board = np.full((max_x+1, max_y+1), ".")

        for elf in elves:
            board[elf[0], elf[1]] = "#"
        print("\nAfter rund", rund + 1)
        print(board)
        print(elves)


xs = [position[0] for position in elves]
ys = [position[1] for position in elves]
result = (max(xs)-min(xs)+1) * (max(ys)-min(ys)+1) - len(elves)
print(result)
