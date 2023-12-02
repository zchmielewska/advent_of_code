import re


def get_color_and_number(cube):
    for c in ["red", "green", "blue"]:
        if c in cube:
            color = c
            number = int(cube.replace(c, "").replace(" ", ""))
            return color, number


def solve1(filename):
    with open(filename) as file:
        total = 0

        for line in file:
            is_correct = True
            grabs = re.split(r"[:;]", line.strip())
            game_id = int(grabs[0].replace("Game ", ""))

            for grab in grabs[1:]:
                cubes = re.split(r",", grab)
                for cube in cubes:
                    color, number = get_color_and_number(cube)
                    if color == "red" and number > 12:
                        is_correct = False

                    if color == "green" and number > 13:
                        is_correct = False

                    if color == "blue" and number > 14:
                        is_correct = False

            if is_correct:
                total += game_id

        return total


def solve2(filename):
    with open(filename) as file:
        total = 0
        for line in file:
            red, green, blue = 0, 0, 0
            grabs = re.split(r"[:;]", line.strip())

            for grab in grabs[1:]:
                cubes = re.split(r",", grab)
                for cube in cubes:
                    color, number = get_color_and_number(cube)
                    if color == "red":
                        red = max(red, number)

                    if color == "green":
                        green = max(green, number)

                    if color == "blue":
                        blue = max(blue, number)

            power = red * green * blue
            total += power

        return total


print(solve1("data.txt"))
print(solve2("data.txt"))
