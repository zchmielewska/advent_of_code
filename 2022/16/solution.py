import itertools
import numpy as np
import os
import re

from collections import deque
from queue import LifoQueue

filename = os.path.join(os.path.dirname(__file__), "data.txt")


class Valve:
    def __init__(self, name, rate, tunnels_names):
        self.name = name
        self.rate = rate
        self.tunnels_names = tunnels_names
        self.tunnels = []
        self.num = None

    def __repr__(self):
        return f"{self.name}"


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


def solve1(valves, working_valves, minutes):
    for i, valve in enumerate(working_valves):
        valve.num = i

    start_valve = get_valve_by_name(valves, "AA")
    stack = LifoQueue()
    stack.put(([start_valve], minutes, 0))

    best_score = 0
    while not stack.empty():
        path, minutes, score = stack.get()
        valve = path[-1]
        unvisited = set(working_valves) - set(path)
        visitable = [valve_to for valve_to in unvisited if minutes - get_distance(valve, valve_to) - 1 > 0]
        scores = [(minutes - get_distance(valve, valve_to) - 1) * valve_to.rate for valve_to in visitable]
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
        sorted_visitables = [visitable[i] for i in sorted_indices]

        for visitable in sorted_visitables:
            next_valve = visitable
            next_path = path + [next_valve]

            distance = get_distance(valve, next_valve)
            next_minutes = minutes - distance - 1
            next_score = score + next_minutes * next_valve.rate

            if next_score > best_score:
                best_score = next_score
                best_path = next_path
                # print("best_score:", best_score, "best_path:", best_path)

            stack.put((next_path, next_minutes, next_score))

    return best_score


def solve2(valves, working_valves, minutes):
    best_score = 0
    combinations = itertools.combinations(working_valves, 8)

    for combination in combinations:
        score1 = solve1(valves, combination, minutes)
        rest = [*set(working_valves)-set(combination)]
        score2 = solve1(valves, rest, minutes)
        if score1 + score2 > best_score:
            best_score = score1 + score2
            # print(f"best_score: {best_score} ({score1} + {score2})")

    return best_score


valves = get_valves(filename)
working_valves = [valve for valve in valves if valve.rate > 0]
print(solve1(valves, working_valves, minutes=30))  # 1940
print(solve2(valves, working_valves, minutes=26))  # 2469
