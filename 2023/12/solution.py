from functools import cache
from itertools import product
import numpy as np

result = 0


def get_records(filename):
    """records = list of tuples like ('???.###', (1, 1, 3))"""
    with open(filename) as file:
        records = []
        for line in file:
            springs, clues = line.strip().split()
            clues = clues.split(",")
            clues = [int(item) for item in clues]
            clues = tuple(clues)
            records.append((springs, clues))
    return records


def spring_to_tpl(spring):
    """'#.#.###' --> (1, 1, 3)"""
    tpl = ()
    num_operational = 0
    for i in range(len(spring)):
        char = spring[i]

        # last spring
        if i == len(spring) - 1:
            if char == "#":
                num_operational += 1
            if num_operational > 0:
                tpl += (num_operational,)

        # operational spring
        elif char == "#":
            num_operational += 1

        # damaged spring
        elif char == ".":
            if num_operational > 0:
                tpl += (num_operational,)
                num_operational = 0

    return tpl


def get_combinations(length, num_operational):
    """all combinations with '#' and '.' where number of '#' equals num_operational"""
    elements = ["#", "."]
    all_combinations = product(elements, repeat=length)
    desired_combinations = [combo for combo in all_combinations if combo.count("#") == num_operational]
    return desired_combinations


def solve1(filename):
    records = get_records(filename)
    total = 0

    for record in records:
        spring = np.array(list(record[0]))
        clues = record[1]
        indices = np.where(spring == "?")[0]
        num_operational = sum(clues) - sum(spring == "#")
        combinations = get_combinations(len(indices), num_operational)

        for c in combinations:
            spring[indices] = c
            arrangement = spring_to_tpl(spring)
            if arrangement == clues:
                total += 1

    return total


@cache
def count_solutions(spring, clues, pos):
    global result
    # print(f"\nspring = {spring} \nclues = {clues} \npos = {pos} \nresult = {result}")

    # spring has no "?" - is it a correct arrangement?
    if spring.count("?") == 0:
        lst = spring_to_tpl("".join(spring))
        return lst == clues

    # "?"
    if spring[pos] == "?":
        result = (count_solutions(spring[:pos] + "." + spring[pos+1:], clues, pos) +
                  count_solutions(spring[:pos] + "#" + spring[pos+1:], clues, pos))

    # "."
    if spring[pos] == ".":
        if pos == 0:
            result = count_solutions(spring, clues, pos+1)

        elif pos > 0:
            # the end of group
            if spring[pos-1] == "#" and spring[pos] == ".":
                # how big is group?
                group_count = spring[:pos].count("#")

                # does it align with clues?
                if len(clues) == 0:
                    return 0
                elif group_count == clues[0]:
                    # analyse the rest of the spring and clues
                    result = count_solutions(spring[pos:], clues[1:], pos=0)
                else:
                    return 0

            # not the end of group
            else:
                result = count_solutions(spring, clues, pos+1)

    # "#"
    if spring[pos] == "#":
        result = count_solutions(spring, clues, pos+1)

    return result


def solve2(filename):
    records = get_records(filename)
    total = 0
    for record in records:
        spring = (record[0] + "?") * 4 + record[0] + "."
        clues = record[1] * 5
        total += count_solutions(spring, clues, pos=0)
    return total


print(solve1("data.txt"))
print(solve2("data.txt"))
