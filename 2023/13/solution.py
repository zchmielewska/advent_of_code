import numpy as np


def lines_to_pattern(lines):
    array_of_chars = np.array([list(string) for string in lines])
    return np.matrix(array_of_chars)


def get_patterns(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        breakpoints = np.where(np.array(lines) == "")[0]

    patterns = []
    for i in range(len(breakpoints)):
        breakpoint = breakpoints[i]

        # first breakpoint
        if i == 0:
            pattern = lines_to_pattern(lines[:breakpoint])
            patterns.append(pattern)

        if 0 < i <= len(breakpoints):
            prev_breakpoint = breakpoints[i-1]
            pattern = lines_to_pattern(lines[prev_breakpoint+1:breakpoint])
            patterns.append(pattern)

        # last breakpoint
        if i == len(breakpoints)-1:
            pattern = lines_to_pattern(lines[breakpoint+1:])
            patterns.append(pattern)

    return patterns


def get_vertical_reflection(pattern, smudge=False):
    num_rows, num_cols = pattern.shape

    for i in range(1, num_cols):
        width = min(i, num_cols-i)
        left = pattern[:, (i-width):i]
        right = pattern[:, i:(i+width)]

        if not smudge:
            if np.all(left == right[:, ::-1]):
                return i
        else:
            if np.sum(left != right[:, ::-1]) == 1:
                return i

    return 0


def get_horizontal_reflection(pattern, smudge=False):
    num_rows, num_cols = pattern.shape

    for i in range(1, num_rows):
        length = min(i, num_rows - i)
        top = pattern[(i-length):i, :]
        bottom = pattern[i:(i + length), :]

        if not smudge:
            if np.all(top == bottom[::-1, :]):
                return i
        else:
            if np.sum(top != bottom[::-1, :]) == 1:
                return i

    return 0


def solve1(filename):
    patterns = get_patterns(filename)
    total = 0
    for i, pattern in enumerate(patterns):
        v = get_vertical_reflection(pattern)
        h = get_horizontal_reflection(pattern)
        value = h * 100 + v
        total += value

    return total


def solve2(filename):
    patterns = get_patterns(filename)
    total = 0
    for i, pattern in enumerate(patterns):
        v = get_vertical_reflection(pattern, smudge=True)
        h = get_horizontal_reflection(pattern, smudge=True)
        value = h * 100 + v
        total += value

    return total


print(solve1("data.txt"))
print(solve2("data.txt"))
