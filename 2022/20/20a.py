import copy
import numpy as np


filename = "./input/20/example.txt"
filename = "./input/20/data.txt"


arrangement = []
with open(filename) as file:
    for line in file:
        row = eval(line)
        arrangement.append(row)

places = [*range(len(arrangement))]

initial_arrangement = copy.deepcopy(arrangement)
initial_places = copy.deepcopy(places)

used = []

place = places[0]
value = initial_arrangement[place]

print("initial:")
print(arrangement)
print(places)
print("\n\n")


def move(arrangement, places, used):
    index = None
    for i in range(len(arrangement)):
        if places[i] not in used:
            index = i
            break

    value = arrangement[index]
    place = places[index]

    print("index:", index, "place:", place, "value:", value)

    remainder = abs(value) % (len(arrangement) - 1)
    remainder = remainder if value >= 0 else -remainder
    # print("remainder", remainder)

    new_index = index + remainder
    if new_index < 0:
        new_index = new_index + (len(arrangement) - 1)

    if new_index > len(arrangement):
        new_index = new_index - (len(arrangement) - 1)

    if new_index == 0:
        new_index = len(arrangement)-1

    # print("new_index", new_index)
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


for i in range(len(arrangement)):
    arrangement, places, used = move(arrangement, places, used)
    # print(arrangement)
    # print(places)
    # print(used)
    # print("")


zero_index = np.min(np.where(np.array(arrangement) == 0))
a = (zero_index + 1000) % len(arrangement)
b = (zero_index + 2000) % len(arrangement)
c = (zero_index + 3000) % len(arrangement)

result = arrangement[a] + arrangement[b] + arrangement[c]
print(result)
