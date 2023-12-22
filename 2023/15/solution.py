def _hash(word):
    current_value = 0

    for char in word:
        current_value += ord(char)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


def solve1(filename):
    with open(filename) as file:
        lines = file.readlines()
    steps = lines[0].split(",")

    total = 0
    for step in steps:
        total += _hash(step)

    return total


def remove(label, box):
    index_to_remove = next((index for index, (string, _) in enumerate(box) if string == label), None)
    if index_to_remove is not None:
        del box[index_to_remove]
    return box


def index_of_label(label, box):
    for i, lens in enumerate(box):
        if lens[0] == label:
            return i
    return None


def print_boxes(boxes):
    for key, value in boxes.items():
        if len(value) > 0:
            print(f"Box {key}: {value}")


def solve2(filename):
    # Initiate boxes
    boxes = dict()
    for n in range(256):
        boxes[n] = []

    with open(filename) as file:
        lines = file.readlines()
    steps = lines[0].split(",")

    for step in steps:
        # Remove lens
        if "-" in step:
            label = step[:-1]
            box_num = _hash(label)
            box = boxes[box_num]
            boxes[box_num] = remove(label, box)

        # Add lens
        else:
            label, focal_length = step.split("=")
            focal_length = int(focal_length)
            box_num = _hash(label)
            box = boxes[box_num]

            i = index_of_label(label, box)
            if i is not None:
                boxes[box_num][i] = (label, focal_length)
            else:
                boxes[box_num].append((label, focal_length))

    focusing_power = 0
    for box_num, box in boxes.items():
        for i, lens in enumerate(box):
            factor1 = box_num + 1
            factor2 = i + 1
            factor3 = lens[1]
            focusing_power += factor1 * factor2 * factor3

    return focusing_power


print(solve1("data.txt"))
print(solve2("data.txt"))
