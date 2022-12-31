import copy
import numpy as np
import time


filename = "./input/20/example.txt"
filename = "./input/20/data.txt"


arrangement = []
with open(filename) as file:
    for line in file:
        row = eval(line)
        arrangement.append(row)


arrangement = [item * 811589153 for item in arrangement]

places = [*range(len(arrangement))]
initial_arrangement = copy.deepcopy(arrangement)
initial_places = copy.deepcopy(places)
used = []

place = places[0]
value = initial_arrangement[place]

# print("initial:")
# print(arrangement)
# print(places)
# print("\n\n")


def move(arrangement, places, place):
    index = np.min(np.where(np.array(places) == place))
    value = arrangement[index]
    # print("let's move:", "place:", place, "index:", index, "value:", value)

    remainder = abs(value) % (len(arrangement) - 1)
    remainder = remainder if value >= 0 else -remainder
    # print("remainder", remainder)

    new_index = index + remainder if index + remainder != len(arrangement) else 0
    # print("new_index", new_index)
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
    # used.append(place)

    # return arrangement, places, used
    return arrangement, places


start = time.time()
for _ in range(10):
    for i in range(len(arrangement)):
        arrangement, places = move(arrangement, places, i)
    # print(arrangement)
    # print(places)
    # print("")
# print("--- End of rund ---")
# print("")
end = time.time()

zero_index = np.min(np.where(np.array(arrangement) == 0))
a = (zero_index + 1000) % len(arrangement)
b = (zero_index + 2000) % len(arrangement)
c = (zero_index + 3000) % len(arrangement)

print(arrangement[a])   # 1623178306 811589153
print(arrangement[b])   # 2434767459 2434767459
print(arrangement[c])   # -1623178306 -1623178306
result = arrangement[a] + arrangement[b] + arrangement[c]
print(result)
print("Elapsed: ", end-start)