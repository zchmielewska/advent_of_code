import copy
import numpy as np
import os

filename = os.path.join(os.path.dirname(__file__), "data.txt")


def move1(arrangement, places, used):
    index = None
    for i in range(len(arrangement)):
        if places[i] not in used:
            index = i
            break

    value = arrangement[index]
    place = places[index]

    remainder = abs(value) % (len(arrangement) - 1)
    remainder = remainder if value >= 0 else -remainder

    new_index = index + remainder
    if new_index < 0:
        new_index = new_index + (len(arrangement) - 1)

    if new_index > len(arrangement):
        new_index = new_index - (len(arrangement) - 1)

    if new_index == 0:
        new_index = len(arrangement)-1

    if index <= new_index:
        for i in range(index, new_index):
            arrangement[i] = arrangement[i+1]
            places[i] = places[i+1]
    else:
        for i in range(index, new_index, -1):
            arrangement[i] = arrangement[i-1]
            places[i] = places[i-1]

    arrangement[new_index] = value
    places[new_index] = place
    used.append(place)

    return arrangement, places, used


def move2(arrangement, places, place):
    index = np.min(np.where(np.array(places) == place))
    value = arrangement[index]
    remainder = abs(value) % (len(arrangement) - 1)
    remainder = remainder if value >= 0 else -remainder

    new_index = index + remainder if index + remainder != len(arrangement) else 0
    if new_index < 0:
        new_index = new_index + (len(arrangement) - 1)

    if new_index > len(arrangement):
        new_index = new_index - (len(arrangement) - 1)

    if new_index == 0:
        new_index = len(arrangement)-1

    if index <= new_index:
        for i in range(index, new_index):
            arrangement[i] = arrangement[i+1]
            places[i] = places[i+1]
    else:
        for i in range(index, new_index, -1):
            arrangement[i] = arrangement[i-1]
            places[i] = places[i-1]

    arrangement[new_index] = value
    places[new_index] = place
    return arrangement, places


def get_arrangement(filename):
    arrangement = []
    with open(filename) as file:
        for line in file:
            row = eval(line)
            arrangement.append(row)
    return arrangement


def solve1(filename):
    arrangement = get_arrangement(filename)
    places = [*range(len(arrangement))]
    used = []

    for i in range(len(arrangement)):
        arrangement, places, used = move1(arrangement, places, used)

    zero_index = np.min(np.where(np.array(arrangement) == 0))
    a = (zero_index + 1000) % len(arrangement)
    b = (zero_index + 2000) % len(arrangement)
    c = (zero_index + 3000) % len(arrangement)

    result = arrangement[a] + arrangement[b] + arrangement[c]
    return result


def solve2(filename):
    arrangement = get_arrangement(filename)
    arrangement = [item * 811589153 for item in arrangement]
    places = [*range(len(arrangement))]

    for _ in range(10):
        for i in range(len(arrangement)):
            arrangement, places = move2(arrangement, places, i)

    zero_index = np.min(np.where(np.array(arrangement) == 0))
    a = (zero_index + 1000) % len(arrangement)
    b = (zero_index + 2000) % len(arrangement)
    c = (zero_index + 3000) % len(arrangement)

    result = arrangement[a] + arrangement[b] + arrangement[c]
    return result


print(solve1(filename))  # 2275
print(solve2(filename))  # 4090409331120
