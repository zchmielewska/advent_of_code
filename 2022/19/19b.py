# 0 = ore | 1 = clay | 2 = obsidian | 3 = geode

import copy
import math
import numpy as np
import re
import time
from queue import LifoQueue


class Game:
    def __init__(self, robots, costs, resources):
        self.robots = robots
        self.costs = costs
        self.resources = resources
        self.robots_in_production = np.array([0, 0, 0, 0])
        self.minute = 1
        self.history = []

    def __repr__(self):
        return f"robots: {self.robots}, resources: {self.resources}, min: {self.minute}, his: {self.history}"

    def buy_robot(self, i):
        self.resources = self.resources - self.costs[i]
        data = np.array([0, 0, 0, 0])
        data[i] = 1
        self.robots_in_production += data

    def collect_robot(self):
        self.robots += self.robots_in_production
        self.robots_in_production = np.array([0, 0, 0, 0])

    def produce_resources(self, times=1):
        for i in range(times):
            self.resources += self.robots

    def get_robots_to_buy(self):
        to_buy = []

        for i in range(4):
            # Can I afford to buy a robot?
            if np.all(self.costs[i] <= self.resources):
                # Don't buy robots if you already produce more than needed to build any robot
                if self.robots[i] < max(self.costs[:, i]):
                    to_buy.append(i)

        # Always buy a geode robot if possible
        if 3 in to_buy:
            return [3]

        return to_buy

    def what_to_buy_next(self):
        robots_to_buy = []
        for i in range(4):
            # I can only buy robots which need resources that I already produce
            if np.all((self.robots > 0) >= (self.costs[i, :] > 0)):
                # I don't need more than X robots where X is maximum cost of this resource (except geode)
                if i == 3 or self.robots[i] < max(self.costs[:, i]):
                    robots_to_buy.append(i)

        # Time that I need to produce this robot
        # cost = current_resource + time * production
        # Time of the resource that takes the most
        times = []
        for robot in robots_to_buy:
            max_time = 0
            for resource in range(4):
                cost = self.costs[robot, resource]
                if cost > 0:
                    current_resource = self.resources[resource]
                    production = self.robots[resource]
                    time = math.ceil((cost - current_resource) / production)
                    max_time = max(max_time, time)
            times.append(max_time)

        # I can't buy anything after 32 minutes
        for i in range(len(robots_to_buy)-1, -1, -1):
            if self.minute + times[i] >= 31:
                del robots_to_buy[i]
                del times[i]

        # If you can buy geode robot first, do it
        if 3 in robots_to_buy:
            geode_index = [i for i, x in enumerate(robots_to_buy) if x == 3][0]
            geode_time = times[geode_index]
            if geode_time == min(times):
                return [(3, geode_time)]

        return [*zip(robots_to_buy, times)]


def solve(start_game):
    stack = LifoQueue()
    stack.put(start_game)

    max_geodes = 0
    i = 0
    while not stack.empty():
    # while i <= 20:
    #     print("")
        game = stack.get()
        # print(f"Game at the end of the minute:\n{game}")

        # No point to look further if no potential to beat current max_geodes
        minutes_left = 32 - game.minute
        if minutes_left * game.robots[3] + game.resources[3] + (minutes_left * (minutes_left-1))/2 <= max_geodes:
            continue

        if game.minute < 32:  # There is no point in building something at the end
            next_steps = game.what_to_buy_next()
            # print("next_steps (robot, mins):", next_steps)

            if len(next_steps) > 0:
                for next_step in next_steps:
                    new_game = copy.deepcopy(game)
                    robot_id = next_step[0]
                    minutes = next_step[1]

                    # Rounds with only producing resources
                    new_game.produce_resources(minutes)
                    new_game.minute += minutes

                    # Round with buying a robot
                    new_game.buy_robot(robot_id)
                    new_game.produce_resources()
                    new_game.collect_robot()
                    new_game.minute += 1

                    # new_game.history.append((robot_id, new_game.minute))
                    stack.put(new_game)

                    if new_game.resources[3] > max_geodes:
                        max_geodes = new_game.resources[3]
                        # print("max_geodes:", max_geodes)

            # Nothing else to buy, just keep producing resources
            else:
                remaining_minutes = 32 - game.minute
                game.produce_resources(remaining_minutes)

                if game.resources[3] > max_geodes:
                    max_geodes = game.resources[3]
                    # print("max_geodes:", max_geodes)
        i += 1
    return max_geodes


filename = "./input/19/data2.txt"

pattern_text = r"Blueprint (?P<blueprint_num>\d+): " \
               r"Each ore robot costs (?P<cost_0_0>\d+) ore. " \
               r"Each clay robot costs (?P<cost_1_0>\d+) ore. " \
               r"Each obsidian robot costs (?P<cost_2_0>\d+) ore and (?P<cost_2_1>\d+) clay. " \
               r"Each geode robot costs (?P<cost_3_0>\d+) ore and (?P<cost_3_2>\d+) obsidian."

result = 1
pattern = re.compile(pattern_text)
with open(filename) as file:
    for line in file:
        start = time.time()
        match = pattern.match(line)
        blueprint_num, cost_0_0, cost_1_0, cost_2_0, cost_2_1, cost_3_0, cost_3_2 = match.groups()

        robots = np.array([1, 0, 0, 0])
        resources = np.array([1, 0, 0, 0])

        costs = np.array([[int(cost_0_0), 0, 0, 0],
                          [int(cost_1_0), 0, 0, 0],
                          [int(cost_2_0), int(cost_2_1), 0, 0],
                          [int(cost_3_0), 0, int(cost_3_2), 0]])

        print(costs)

        start_game = Game(robots, costs, resources)
        max_geodes = solve(start_game)
        result = result * max_geodes
        end = time.time()
        print(f"blueprint {blueprint_num}: max_geodes = {max_geodes}, time = {round(end-start)}, current_result = {result}")


