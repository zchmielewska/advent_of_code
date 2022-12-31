import numpy as np


filename = "./input/13/example2.txt"
filename = "./input/13/data2.txt"


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


packets = []
with open(filename) as file:
    for line in file:
        if line.strip() != "":
            packets.append(Packet(eval(line)))

packets = sorted(packets)
indices = [i+1 for i, v in enumerate(packets) if v.value == [[2]] or v.value == [[6]]]
print(np.prod(indices))
