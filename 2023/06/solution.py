import functools
import re


def read_input(filename):
    with open(filename) as file:
        lines = file.readlines()

    times = lines[0].strip().replace("Time:", "")
    times = re.split(r"\s+", times)
    times = [int(t) for t in times if t != ""]

    records = lines[1].strip().replace("Distance:", "")
    records = re.split(r"\s+", records)
    records = [int(d) for d in records if d != ""]
    return times, records


def time_to_num_ways_to_win(time, record):
    distances = [i * (time - i) for i in range(time+1)]
    num_ways = len([d for d in distances if d > record])
    return num_ways


def solve1(filename):
    times, records = read_input(filename)
    num_ways_to_win = [time_to_num_ways_to_win(time, record) for time, record in zip(times, records)]
    result = functools.reduce((lambda x, y: x * y), num_ways_to_win)
    return result


def read_input_with_kerning(filename):
    with open(filename) as file:
        lines = file.readlines()

    time = lines[0].strip().replace("Time:", "")
    time = re.sub(r"\s+", "", time)
    time = int(time)

    record = lines[1].strip().replace("Distance:", "")
    record = re.sub(r"\s+", "", record)
    record = int(record)

    return time, record


def solve2(filename):
    time, record = read_input_with_kerning(filename)
    return time_to_num_ways_to_win(time, record)


print(solve1("data.txt"))
print(solve2("data.txt"))
