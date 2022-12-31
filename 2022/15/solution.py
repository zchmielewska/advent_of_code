import os
import numpy as np
import re


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
        self.border = None

    def __repr__(self):
        return f"[{self.sensor.row}, {self.sensor.col}, {self.distance}]"

    def get_border(self):
        border = set()
        for e, i in enumerate(range(self.sensor.row, self.sensor.row + self.distance + 2)):
            if i >= 0:
                col1 = self.sensor.col - (self.distance + 1) + e
                if col1 >= 0:
                    point1 = (i, col1)
                    border.add(point1)

                col2 = self.sensor.col + (self.distance + 1) - e
                if col2 >= 0:
                    point2 = (i, col2)
                    border.add(point2)

        for e, i in enumerate(range(self.sensor.row, self.sensor.row - self.distance - 2, -1)):
            if i >= 0:
                col1 = self.sensor.col - (self.distance + 1) + e
                if col1 >= 0:
                    point1 = (i, col1)
                    border.add(point1)

                col2 = self.sensor.col + (self.distance + 1) - e
                if col2 >= 0:
                    point2 = (i, col2)
                    border.add(point2)
        self.border = border


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
    for pair in pairs:
        row = func(row, pair.sensor.row, pair.sensor.row + pair.distance, pair.sensor.row - pair.distance)
        col = func(col, pair.sensor.col, pair.sensor.col + pair.distance, pair.sensor.col - pair.distance)
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


def solve1(filename, y):
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

    return len(occupied)


def solve2(filename, limit):
    chosen_point = None

    pairs = get_pairs(filename)
    for pair in pairs:
        pair.get_border()

    for border_pair in pairs:
        for point in border_pair.border:
            row, col = point
            if row > limit or col > limit:
                continue

            result = 1
            for area_pair in pairs:
                if manhattan_distance(point, (area_pair.sensor.row, area_pair.sensor.col)) <= area_pair.distance:
                    result = 0
                    break

            if result == 1:
                chosen_point = point
                break

    tuning_frequency = chosen_point[1] * 4000000 + chosen_point[0]
    return tuning_frequency


filename = os.path.join(os.path.dirname(__file__), "data.txt")
print(solve1(filename, y=2000000))  # 5125700
print(solve2(filename, limit=4_000_000))  # 11379394658764
