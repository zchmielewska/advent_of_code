import numpy as np


def is_int(value):
    result = False
    try:
        int(value)
        result = True
    except ValueError:
        pass
    return result


def file_to_matrix(filename):
    """Convert text file to matrix of chars"""
    with open(filename) as file:
        lines = file.readlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        matrix = np.full(shape=(num_rows, num_cols), fill_value=" ", dtype=str)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                matrix[i, j] = char
    return matrix


def get_numbers(matrix):
    numbers = []
    num_rows, num_cols = matrix.shape

    for i in range(num_rows):
        new_number = []
        for j in range(num_cols):
            # char is an int
            if is_int(matrix[i, j]):
                new_number.append((i, j))

            # char is not an int and number has finished
            if not is_int(matrix[i,j]) and len(new_number) > 0:
                numbers.append(new_number)
                new_number = []

            # last column and number is not trivial
            if j == num_cols-1 and len(new_number) > 0:
                numbers.append(new_number)

    return numbers


def get_adjacent_indexes(row, col, max_row, max_col):
    adjacent_indexes = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (i == 0 and j == 0) and 0 <= row+i < max_row and 0 <= col+j < max_col:
                adjacent_indexes.append((row+i, col+j))
    return adjacent_indexes


def is_part_number(number, matrix):
    """Check if part numbers (there is adjacent char which is not an integer or dot)"""
    for digit in number:
        adjacent_indexes = get_adjacent_indexes(digit[0], digit[1], matrix.shape[0], matrix.shape[1])
        for adjacent_index in adjacent_indexes:
            chr = matrix[adjacent_index]
            if chr != "." and not is_int(chr):
                return True
    return False


def part_number_to_value(part_number, matrix):
    value = ""
    for digit in part_number:
        value += matrix[digit]
    return int(value)


def get_stars(matrix):
    stars = []
    num_rows, num_cols = matrix.shape
    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i, j] == "*":
                stars.append((i, j))
    return stars


def touches(star, part_number, matrix):
    adjacent_indexes = set(get_adjacent_indexes(star[0], star[1], matrix.shape[0], matrix.shape[1]))
    part_number_set = set(part_number)
    common = adjacent_indexes.intersection(part_number_set)
    return len(common) > 0


def get_gear_ratio(star, part_numbers, matrix):
    num_touches = 0
    gear_ratio = 1

    for part_number in part_numbers:
        if touches(star, part_number, matrix):
            num_touches += 1
            gear_ratio *= part_number_to_value(part_number, matrix)
            if num_touches > 2:
                return 0

    if num_touches == 2:
        return gear_ratio

    return 0


def solve1(filename):
    matrix = file_to_matrix(filename)
    numbers = get_numbers(matrix)
    part_numbers = [number for number in numbers if is_part_number(number, matrix)]
    values = [part_number_to_value(part_number, matrix) for part_number in part_numbers]
    return sum(values)


def solve2(filename):
    matrix = file_to_matrix(filename)
    numbers = get_numbers(matrix)
    part_numbers = [number for number in numbers if is_part_number(number, matrix)]
    stars = get_stars(matrix)
    gear_ratios = [get_gear_ratio(star, part_numbers, matrix) for star in stars]
    return sum(gear_ratios)


print(solve1("data.txt"))
print(solve2("data.txt"))
