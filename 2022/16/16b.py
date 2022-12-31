import itertools
import numpy as np
import re
import time

from collections import deque
from queue import LifoQueue


class Valve:
    def __init__(self, name, rate, tunnels_names):
        self.name = name
        self.rate = rate
        self.tunnels_names = tunnels_names
        self.tunnels = []
        self.num = None

    def __repr__(self):
        return f"{self.name}"


def flatten(lst):
    return sum(lst, [])


def get_valve_by_name(valves, name):
    for valve in valves:
        if valve.name == name:
            return valve
    return None


def get_valves(filename):
    pattern_text = r"Valve (?P<name>\w{2}) has flow rate=(?P<rate>\d+); " \
                   r"tunnel[s]? lead[s]? to valve[s]? (?P<tunnels_names>.*)"

    pattern = re.compile(pattern_text)
    valves = []
    with open(filename) as file:
        i = 0
        for line in file:
            match = pattern.match(line)
            name, rate, tunnels_names = match.groups()
            rate = int(rate)
            tunnels_names = tunnels_names.split(", ")
            valves.append(Valve(name, rate, tunnels_names))
            i += 1

    for valve in valves:
        for tunnel_name in valve.tunnels_names:
            tunnel = get_valve_by_name(valves, tunnel_name)
            if tunnel is not None:
                valve.tunnels.append(tunnel)

    return valves


def get_distance(valve_from, valve_to):
    if valve_from == valve_to:
        return 0

    search_queue = deque()
    search_queue += [valve_from.tunnels]

    distance = 1
    while search_queue:
        tunnels = search_queue.popleft()
        if valve_to in tunnels:
            return distance
        else:
            new_tunnels = set()

            for tunnel in tunnels:
                new_tunnels.update(tunnel.tunnels)

            search_queue += [list(new_tunnels)]
        distance += 1

    return distance


def get_distance_matrix(valves):
    n = len(valves)
    distances = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            valve1 = valves[i]
            valve2 = valves[j]
            distances[i, j] = get_distance(valve1, valve2)
    return distances


# valves = get_valves(filename="./input/16/example.txt")
valves = get_valves(filename="./input/16/data.txt")

working_valves = [valve for valve in valves if valve.rate > 0]
for i, valve in enumerate(working_valves):
    valve.num = i

print(working_valves)
n = len(working_valves)
print("n=", n)
distances = get_distance_matrix(working_valves)
print(distances)


def solve(valves, working_valves):
    start_valve = get_valve_by_name(valves, "AA")
    stack = LifoQueue()
    stack.put(([start_valve], 26, 0))
    # print("initial stack:", stack.qsize())

    best_score = 0
    best_path = None
    while not stack.empty():
        # print("")
        path, minutes, score = stack.get()
        # print("path:", path, "minutes:", minutes)

        valve = path[-1]
        # print("valve:", valve)

        unvisited = set(working_valves) - set(path)
        # print("unvisited:", unvisited)

        visitable = [valve_to for valve_to in unvisited if minutes - get_distance(valve, valve_to) - 1 > 0]
        # print("visitable:", visitable)

        distances = [get_distance(valve, valve_to) for valve_to in visitable]
        # print("distances:", distances)

        scores = [(minutes - get_distance(valve, valve_to) - 1) * valve_to.rate for valve_to in visitable]
        # print("scores:", scores)

        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
        sorted_visitables = [visitable[i] for i in sorted_indices]

        next_indices = [i for i, v in enumerate(scores) if v == max(scores)]
        # print("next_indices:", next_indices)

        for visitable in sorted_visitables:
            # print("next_index:", next_index)

            # next_valve = visitable[next_index]
            next_valve = visitable
            # print("next_valve:", next_valve)

            next_path = path + [next_valve]
            # print("new_path:", next_path)

            distance = get_distance(valve, next_valve)
            next_minutes = minutes - distance - 1
            next_score = score + next_minutes * next_valve.rate

            if next_score > best_score:
                best_score = next_score
                best_path = next_path
                # print("best_score:", best_score, "best_path:", best_path)

            stack.put((next_path, next_minutes, next_score))

        # print("stack:", stack.qsize())

    # print("best_score:", best_score, "best_path:", best_path)
    return best_score, best_path


best_score = 0
combinations = itertools.combinations(working_valves, 8)

i = 1
for combination in combinations:
    if i % 100 == 0:
        print(i)
    score1, path1 = solve(valves, combination)
    rest = [*set(working_valves)-set(combination)]
    score2, path2 = solve(valves, rest)
    if score1 + score2 > best_score:
        best_score = score1 + score2
        print(f"best_score: {best_score} ({score1} + {score2}) [path1: {path1}, path2: {path2}]")
    i += 1

print(f"best_score: {best_score} ({score1} + {score2}) [path1: {path1}, path2: {path2}]")
