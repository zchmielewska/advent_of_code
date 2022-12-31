import numpy as np

from collections import deque

filename = "../../2022/12/data.txt"


def get_num_steps(final):
    i = 0
    while final.parent is not None:
        final = final.parent
        i += 1
    return i


class Position:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return get_num_steps(self) < get_num_steps(other)


def get_terrain(filename):
    rows = []
    with open(filename) as file:
        for line in file:
            row = [ord(_) for _ in line.rstrip('\n')]
            rows.append(row)

    terrain = np.array(rows)

    start_coord = tuple(np.argwhere(terrain == ord("S")).flatten())
    end_coord = tuple(np.argwhere(terrain == ord("E")).flatten())
    start = Position(start_coord[0], start_coord[1])
    end = Position(end_coord[0], end_coord[1])

    terrain[start.x, start.y] = ord("a")
    terrain[end.x, end.y] = ord("z")
    terrain = terrain - 96
    return terrain, start, end


def distance(pos1, pos2):
    return abs(pos1.x-pos2.x) + abs(pos1.y-pos2.y)


def get_moves(terrain, position):
    moves = []
    value = terrain[position.x, position.y]

    # right
    if position.y < terrain.shape[1]-1:
        move = (position.x, position.y + 1)
        if terrain[move] <= value + 1:
            moves.append(Position(move[0], move[1], position))

    # left
    if position.y > 0:
        move = (position.x, position.y - 1)
        if terrain[move] <= value + 1:
            moves.append(Position(move[0], move[1], position))

    # up
    if position.x > 0:
        move = (position.x - 1, position.y)
        if terrain[move] <= value + 1:
            moves.append(Position(move[0], move[1], position))

    # down
    if position.x < terrain.shape[0]-1:
        move = (position.x + 1, position.y)
        if terrain[move] <= value + 1:
            moves.append(Position(move[0], move[1], position))

    return moves


def search(terrain, start, end):
    search_queue = deque()
    search_queue += [start]
    searched = []

    while search_queue:
        position = search_queue.popleft()
        if position not in searched:
            if position == end:
                return(position)
            else:
                search_queue += get_moves(terrain, position)

                searched.append(position)
    return False


terrain, start, end = get_terrain(filename)
final = search(terrain, start, end)

i = 0
while final.parent is not None:
    final = final.parent
    i += 1

print(i)
