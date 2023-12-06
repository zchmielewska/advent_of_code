def get_seeds(filename):
    with open(filename) as file:
        first_line = file.readline().strip()
        first_line = first_line.replace("seeds: ", "")
        first_line = first_line.split()
        seeds = [int(s) for s in first_line]
    return seeds


def get_transformations(filename):
    with open(filename) as file:
        lines = file.readlines()
        transformations = []
        transformation = []
        i = 3
        while i < len(lines):
            line = lines[i].strip()
            if line == "":
                transformations.append(transformation)
                transformation = []
                i += 2
            else:
                items = line.split()
                _map = {
                    "destination": items[0],
                    "source": items[1],
                    "length": items[2]
                }
                i += 1
                transformation.append(_map)
        transformations.append(transformation)  # last line
    return transformations


def transform(seed, transformation):
    for _map in transformation:
        source = int(_map["source"])
        length = int(_map["length"])
        destination = int(_map["destination"])
        diff = destination - source

        if source <= seed < source + length:
            return seed + diff

    return seed


def reverse_transform(location, transformation):
    for _map in transformation:
        source = int(_map["source"])
        length = int(_map["length"])
        destination = int(_map["destination"])
        diff = source - destination

        if destination <= location < destination + length:
            return location + diff

    return location


def seed_to_location(seed, transformations):
    for transformation in transformations:
        seed = transform(seed, transformation)
    return seed


def location_to_seed(location, transformations):
    for transformation in reversed(transformations):
        location = reverse_transform(location, transformation)
    return location


def is_in_seeds(value, extended_seeds):
    for extended_seed in extended_seeds:
        if extended_seed["min"] <= value < extended_seed["max"]:
            return True
    return False


def get_extended_seeds(seeds):
    extended_seeds = []
    i = 0
    while i < len(seeds):
        _range = {
            "min": seeds[i],
            "max": seeds[i] + seeds[i+1],
        }
        extended_seeds.append(_range)
        i += 2
    return extended_seeds


def solve1(filename):
    seeds = get_seeds(filename)
    transformations = get_transformations(filename)
    locations = [seed_to_location(seed, transformations) for seed in seeds]
    return min(locations)


def solve2(filename):
    seeds = get_seeds(filename)
    transformations = get_transformations(filename)
    extended_seeds = get_extended_seeds(seeds)
    result = None
    i = 0
    while result is None:
        value = location_to_seed(i, transformations)
        i += 1
        if is_in_seeds(value, extended_seeds):
            result = value
    return i-1


print(solve1("data.txt"))
print(solve2("data.txt"))
