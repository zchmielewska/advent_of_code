import numpy as np
import os


def lower_than(packet1, packet2):
    i = 0
    while i < max(len(packet1), len(packet2)):
        if i >= len(packet1) or len(packet1) == 0:
            return 1

        if i >= len(packet2) or len(packet2) == 0:
            return 0

        left = packet1[i]
        right = packet2[i]

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return 0

        if isinstance(left, int) and isinstance(right, list):
            left = [left]

        if isinstance(left, list) and isinstance(right, int):
            right = [right]

        if isinstance(left, list) and isinstance(right, list):
            result = lower_than(left, right)
            if result == 0 or result == 1:
                return result
        i += 1


class Packet:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return lower_than(self.value, other.value)

    def __repr__(self):
        return f"{self.value}"


def solve1(filename):
    j = 0
    results = []
    with open(filename) as file:
        for line in file:
            if j % 3 == 0:
                packet1 = eval(line)
            elif j % 3 == 1:
                packet2 = eval(line)
                result = lower_than(packet1, packet2)
                results.append(result)
            j += 1

    indices = [i+1 for i, v in enumerate(results) if v == 1]
    return sum(indices)


def solve2(filename):
    packets = []
    with open(filename) as file:
        for line in file:
            if line.strip() != "":
                packets.append(Packet(eval(line)))

    packets = sorted(packets)
    indices = [i+1 for i, v in enumerate(packets) if v.value == [[2]] or v.value == [[6]]]
    return np.prod(indices)


filename1 = os.path.join(os.path.dirname(__file__), "data1.txt")
filename2 = os.path.join(os.path.dirname(__file__), "data2.txt")
print(solve1(filename1))  # 5825
print(solve2(filename2))  # 24477
