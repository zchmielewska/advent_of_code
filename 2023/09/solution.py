import numpy as np


def get_lines(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split() for line in lines]
        lines = [[int(num) for num in sublist] for sublist in lines]
        lines = [np.array(line) for line in lines]
    return lines


def line_to_history(line):
    history = [line]
    while not all(line == 0):
        line_moved = np.append(line[1:], 0)
        new_line = (line_moved - line)[:-1]
        history.append(new_line)
        line = new_line
    return history


def history_to_next_value(history):
    history.reverse()
    for i in range(len(history)):
        if i == 0:
            history[i] = np.append(history[i], 0)
        else:
            history[i] = np.append(history[i], history[i - 1][-1] + history[i][-1])
    next_value = history[-1][-1]
    return next_value


def line_to_next_value(line):
    history = line_to_history(line)
    next_value = history_to_next_value(history)
    return next_value


def line_to_prev_value(line):
    history = line_to_history(line)
    prev_value = history_to_prev_value(history)
    return prev_value


def solve1(filename):
    lines = get_lines(filename)
    next_values = [line_to_next_value(line) for line in lines]
    return sum(next_values)


def history_to_prev_value(history):
    history.reverse()
    for i in range(len(history)):
        if i == 0:
            history[i] = np.append(0, history[i])
        else:
            history[i] = np.append(history[i][0] - history[i - 1][0], history[i])
    prev_value = history[-1][0]
    return prev_value


def solve2(filename):
    lines = get_lines(filename)
    prev_values = [line_to_prev_value(line) for line in lines]
    return sum(prev_values)


print(solve1("data.txt"))
print(solve2("data.txt"))
