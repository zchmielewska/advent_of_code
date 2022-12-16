import numpy as np
import re


from functools import partial


np.set_printoptions(linewidth=200)


class Sensor:
    def __init__(self, row, col):
        self.row = int(row)
        self.col = int(col)

    def __repr__(self):
        return f"[Sensor: [{self.row}, {self.col}]"


class Beacon:
    def __init__(self, row, col):
        self.row = int(row)
        self.col = int(col)

    def __repr__(self):
        return f"[Beacon: [{self.row}, {self.col}]"


class Pair:
    def __init__(self, sensor, beacon):
        self.sensor = sensor
        self.beacon = beacon
        self.distance = manhattan_distance((sensor.row, sensor.col), (beacon.row, beacon.col))

    def __repr__(self):
        return f"[{self.sensor.row}, {self.sensor.col}, {self.distance}]"


def get_pairs(filename):
    pattern_text = r"Sensor at x=(?P<s_x>[-]?\d+), y=(?P<s_y>[-]?\d+): " \
                   r"closest beacon is at x=(?P<b_x>[-]?\d+), y=(?P<b_y>[-]?\d+)"
    pattern = re.compile(pattern_text)
    pairs = []
    with open(filename) as file:
        for line in file:
            match = pattern.match(line)
            s_x, s_y, b_x, b_y = (match.groups())
            sensor = Sensor(s_y, s_x)
            beacon = Beacon(b_y, b_x)
            pairs.append(Pair(sensor, beacon))
    return pairs


def get_edges(pairs, func):
    row = func(pairs[0].sensor.row, pairs[0].sensor.row + pairs[0].distance, pairs[0].sensor.row - pairs[0].distance)
    col = func(pairs[0].sensor.col, pairs[0].sensor.col + pairs[0].distance, pairs[0].sensor.col - pairs[0].distance)
    # row = func(pairs[0].sensor.row, pairs[0].beacon.row)
    # col = func(pairs[0].sensor.col, pairs[0].beacon.col)

    for pair in pairs:
        row = func(row, pair.sensor.row, pair.sensor.row + pair.distance, pair.sensor.row - pair.distance)
        col = func(col, pair.sensor.col, pair.sensor.col + pair.distance, pair.sensor.col - pair.distance)
        # row = func(row, pair.sensor.row, pair.beacon.row)
        # col = func(col, pair.sensor.col, pair.beacon.col)

    return row, col


def normalize(pairs, row, col):
    for pair in pairs:
        pair.sensor.row += row
        pair.beacon.row += row
        pair.sensor.col += col
        pair.beacon.col += col
    return pairs


def manhattan_distance(x, y):
    x1, y1 = x
    x2, y2 = y
    return abs(x1 - x2) + abs(y1 - y2)


def get_indices(nrow, ncol):
    indices = np.empty([nrow, ncol], dtype=object)
    for i in range(indices.shape[0]):
        for j in range(indices.shape[1]):
            indices[i, j] = (i, j)
    return indices


def solve(filename, y):
    pairs1 = get_pairs(filename)

    # Pairs which signal intersects with row y
    pairs2 = []
    for pair in pairs1:
        if pair.sensor.row - pair.distance <= y <= pair.sensor.row + pair.distance:
            pairs2.append(pair)

    # Occupied cells in row y
    occupied = set()
    for pair in pairs2:
        row_diff = abs(pair.sensor.row - y)
        occupation = list(range(pair.sensor.col-pair.distance+row_diff, pair.sensor.col+pair.distance-row_diff+1))
        for col in occupation:
            occupied.add(col)

    # Remove sensors and beacons from occupied cells
    for pair in pairs1:
        if pair.beacon.row == y and pair.beacon.col in occupied:
            occupied.remove(pair.beacon.col)

        if pair.sensor.row == y and pair.sensor.col in occupied:
            occupied.remove(pair.sensor.col)

    return occupied


result = solve(filename="./input/15/example.txt", y=10)
print(len(result))

result = solve(filename="./input/15/data.txt", y=2000000)
print(len(result))
