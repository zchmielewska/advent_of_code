import math


def get_input(filename):
    with open(filename) as file:
        maps = dict()

        for i, line in enumerate(file):
            if i == 0:
                instructions = list(line.strip())
            elif i == 1:
                continue
            else:
                _from = line[0:3]
                left = line[7:10]
                right = line[12:15]
                maps[_from] = (left, right)
    return instructions, maps


def solve1(filename):
    instructions, maps = get_input(filename)
    num_steps = 0
    element = "AAA"
    while True:
        direction = instructions[num_steps % len(instructions)]
        direction_index = 0 if direction == "L" else 1

        num_steps += 1
        element = maps[element][direction_index]
        if element == "ZZZ":
            break
    return num_steps


def get_num_steps(element, instructions, maps):
    num_steps = 0
    while True:
        direction = instructions[num_steps % len(instructions)]
        direction_index = 0 if direction == "L" else 1
        num_steps += 1
        element = maps[element][direction_index]
        if element[-1] == "Z":
            break
    return num_steps


def lcm(a, b):
    return a * b // math.gcd(a, b)


def solve2(filename):
    instructions, maps = get_input(filename)
    elements = [e for e in maps.keys() if e[-1] == "A"]
    num_steps = [get_num_steps(e, instructions, maps) for e in elements]

    result = num_steps[0]
    for i in range(1, len(num_steps)):
        result = lcm(result, num_steps[i])

    return result


print(solve1("data.txt"))
print(solve2("data.txt"))
