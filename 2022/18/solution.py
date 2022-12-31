import os

from collections import deque

filename = os.path.join(os.path.dirname(__file__), "data.txt")


def get_cubes(filename):
    cubes = []
    with open(filename) as file:
        for line in file:
            row = eval(line)
            cubes.append(row)
    return cubes


def total_surface(points):
    total = 0
    for point in points:
        surface = 6
        x, y, z = point

        if (x+1, y, z) in points:
            surface -= 1

        if (x-1, y, z) in points:
            surface -= 1

        if (x, y+1, z) in points:
            surface -= 1

        if (x, y-1, z) in points:
            surface -= 1

        if (x, y, z+1) in points:
            surface -= 1

        if (x, y, z-1) in points:
            surface -= 1

        total += surface
    return total


def get_neighbours(point, min_dim, max_dim):
    neighbours = []
    x, y, z = point
    new_points = [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    for new_point in new_points:
        new_x, new_y, new_z = new_point
        if min_dim <= new_x <= max_dim and min_dim <= new_y <= max_dim and min_dim <= new_z <= max_dim:
            neighbours.append(new_point)
    return neighbours


def solve1(filename):
    cubes = get_cubes(filename)
    total = total_surface(cubes)
    return total


def solve2(filename):
    cubes = get_cubes(filename)
    min_x = min([cube[0] for cube in cubes]) - 1
    min_y = min([cube[1] for cube in cubes]) - 1
    min_z = min([cube[2] for cube in cubes]) - 1
    max_x = max([cube[0] for cube in cubes])
    max_y = max([cube[1] for cube in cubes])
    max_z = max([cube[2] for cube in cubes])

    min_dim = min(min_x, min_y, min_z)
    max_dim = max(max_x, max_y, max_z)

    # outside air
    search_queue = deque()
    search_queue += [(min_dim, min_dim, min_dim)]
    searched = []

    while search_queue:
        point = search_queue.popleft()
        if point not in searched:
            neighbours = get_neighbours(point, min_dim, max_dim)
            air_neighbours = list(set(neighbours) - set(cubes))
            search_queue += air_neighbours
            searched.append(point)

    all_points = []
    for i in range(min_dim, max_dim+1):
        for j in range(min_dim, max_dim+1):
            for k in range(min_dim, max_dim+1):
                all_points.append((i, j, k))

    outside_air = searched
    inside_air = list(set(all_points) - set(outside_air) - set(cubes))

    cubes_surface = total_surface(cubes)
    inside_air_surface = total_surface(inside_air)
    result = cubes_surface - inside_air_surface
    return result


print(solve1(filename))  # 4482
print(solve2(filename))  # 2576
