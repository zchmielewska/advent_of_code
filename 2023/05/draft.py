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


def solve1(filename):
    seeds = get_seeds(filename)
    transformations = get_transformations(filename)
    locations = [seed_to_location(seed, transformations) for seed in seeds]
    return min(locations)


def compare_ranges(source_range, destination_range):
    non_overlapping = None
    overlapping = None

    s_min, s_max = source_range[0], source_range[1]
    d_min, d_max = destination_range[0], destination_range[1]

    # source lower than destination
    if s_max < d_min:
        non_overlapping = (s_min, s_max)

    # source touches left of destination
    if s_max == d_min:
        non_overlapping = (s_min, s_max-1)
        overlapping = (s_max, s_max)

    # source and destination overlap partly from the left
    if s_min < d_min and d_min < s_max <= d_max:
        non_overlapping = (s_min, d_min-1)
        overlapping = (d_min, s_max)

    # destination covers source
    if d_min <= s_min and s_max <= d_max:
        overlapping = (s_min, s_max)

    # source and destination overlap partly from the right
    if d_min <= s_min < d_max and s_max > d_max:
        non_overlapping = (d_max+1, s_max)
        overlapping = (s_min, d_max)

    # source touched right of destination
    if s_min == d_max:
        non_overlapping = (s_min+1, s_max)
        overlapping = (s_min, s_min)

    # source higher than destination
    if s_min > d_max:
        non_overlapping = (s_min, s_max)

    # source bigger than destination
    if s_min < d_min and s_max > d_max:
        non_overlapping = [(s_min, d_min-1), (d_max+1, s_max)]
        overlapping = (d_min, d_max)

    return non_overlapping, overlapping


def combine_ranges(ranges):
    if len(ranges) <= 1:
        return ranges

    ranges = sorted(ranges, key=lambda x: x[0])
    new_ranges = [ranges[0]]

    for i in range(1, len(ranges)):
        current_range = ranges[i]

        # current ranges is adjacent to the last range
        if new_ranges[-1][1] + 1 == current_range[0]:
            new_ranges[-1] = (new_ranges[-1][0], current_range[1])
        else:
            new_ranges.append(current_range)
    return new_ranges


def is_in_seeds(value, extended_seeds):
    for extended_seed in extended_seeds:
        if extended_seed["min"] <= value < extended_seed["max"]:
            return True
    return False


def get_extended_seeds(filename):
    seeds = get_seeds(filename)  # part 1 style
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


def get_initial_ranges(transformations):
    ranges = []
    first_transformation = transformations[0]
    for _map in first_transformation:
        length = int(_map["length"])
        destination = int(_map["destination"])
        ranges.append((destination, destination+length-1))
    ranges = combine_ranges(ranges)
    return ranges


def get_locations(ranges, transformations):
    new_ranges = ranges
    for transformation in transformations[1:]:
        # print("\n--->", transformation)

        prev_ranges = combine_ranges(new_ranges)
        new_ranges = []
        # print("prev_ranges=", prev_ranges, "\n")

        for source_range in prev_ranges:  # (50, 51), (52, 99)
            # print("\nsource_range=", source_range)

            for _map in transformation:
                if source_range is not None:
                    # print("\nmap=", _map)
                    source = int(_map["source"])  # 15
                    length = int(_map["length"])  # 37
                    destination = int(_map["destination"])  # 0
                    diff = destination - source
                    destination_range = (source, source + length - 1)

                    # print("\ncomparison against: source_range=", source_range, "destination_range=", destination_range)
                    non_overlapping, overlapping = compare_ranges(source_range, destination_range)
                    # print("non_overlapping=", non_overlapping)
                    # print("overlapping=", overlapping)

                    if isinstance(non_overlapping, list):
                        source_range = non_overlapping[1]
                        new_ranges.append(non_overlapping[0])
                    else:
                        source_range = non_overlapping

                    if overlapping is not None:
                        overlapping_after_transformation = (overlapping[0] + diff, overlapping[1] + diff)
                        # print("overlapping_after_transformation=", overlapping_after_transformation)
                        new_ranges.append(overlapping_after_transformation)

                    # print("new_ranges=", new_ranges)
                    # print("")

            if source_range is not None:
                new_ranges.append(source_range)

    new_ranges = sorted(new_ranges, key=lambda x: x[0])
    return new_ranges


def solve2(filename):
    transformations = get_transformations(filename)
    ranges = get_initial_ranges(transformations)
    extended_seeds = get_extended_seeds(filename)
    locations = get_locations(ranges, transformations)
    for new_range in locations:
        for possible_location in range(new_range[0], new_range[1]):
            possible_seed = location_to_seed(possible_location, transformations)
            if is_in_seeds(possible_seed, extended_seeds):
                return possible_location


print(solve2("data.txt"))
