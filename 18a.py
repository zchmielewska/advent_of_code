
filename = "./input/18/example.txt"
filename = "./input/18/data.txt"


cubes = []
with open(filename) as file:
    for line in file:
        row = eval(line)
        cubes.append(row)

print(cubes)

def total_surface(cubes):
    total = 0
    for cube in cubes:
        surface = 6
        x, y, z = cube

        if (x+1, y, z) in cubes:
            surface -= 1

        if (x-1, y, z) in cubes:
            surface -= 1

        if (x, y+1, z) in cubes:
            surface -= 1

        if (x, y-1, z) in cubes:
            surface -= 1

        if (x, y, z+1) in cubes:
            surface -= 1

        if (x, y, z-1) in cubes:
            surface -= 1

        total += surface
    return(total)

total = total_surface(cubes)
print(total)
