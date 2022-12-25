import numpy as np
import re


filename = "./input/22/data.txt"

rows = []
with open(filename) as file:
    for line in file:
        row = line.rstrip('\n')
        # row = row.replace(" ", "9")
        # row = row.replace(".", "0")
        # row = row.replace("#", "1")
        rows.append(row)


def get_field(rows):
    rows = rows[:-2]
    max_n = max([len(row) for row in rows])
    field_rows = []
    for row in rows:
        if len(row) < max_n:
            row = row + (" " * (max_n - len(row)))
        field_row = [_ for _ in row]
        field_rows.append(field_row)
    field = np.array(field_rows)
    return field


def get_notes(rows):
    notes = rows[-1]
    regex = re.compile(r"(\d+|\s+)")
    notes = regex.split(notes)
    notes = [note for note in notes if note != ""]
    return notes


field = get_field(rows)
notes = get_notes(rows)
start_col = np.min(np.where(field[0, ] == "."))
field[0, start_col] = ">"


class Game:
    def __init__(self, field, start_col):
        self.field = field
        self.facing = "right"
        self.row = 0
        self.col = start_col

    def move(self):
        if self.facing == "right":

            # Touching the border
            if self.col == self.field.shape[1]-1:
                first_col = np.min(np.where(field[self.row,] != " "))
                if field[self.row, first_col] != "#":
                    self.field[self.row, first_col] = ">"
                    self.col = first_col
            else:
                next_tile = self.field[self.row, self.col+1]

                # Move by one tile
                if next_tile != " " and next_tile != "#":
                    self.field[self.row, self.col+1] = ">"
                    self.col += 1

                # Jump over to the other side
                elif next_tile == " ":
                    first_col = np.min(np.where(field[self.row, ] != " "))
                    if field[self.row, first_col] != "#":
                        self.field[self.row, first_col] = ">"
                        self.col = first_col

        if self.facing == "down":

            # Touching the border
            if self.row == self.field.shape[0]-1:
                first_row = np.min(np.where(field[:, self.col] != " "))
                if field[first_row, self.col] != "#":
                    self.field[first_row, self.col] = "v"
                    self.row = first_row

            else:
                next_tile = self.field[self.row+1, self.col]

                # Move by one tile
                if next_tile != " " and next_tile != "#":
                    self.field[self.row+1, self.col] = "v"
                    self.row += 1

                # Jump over to the other side
                elif next_tile == " ":
                    first_row = np.min(np.where(field[:, self.col] != " "))
                    if field[first_row, self.col] != "#":
                        self.field[first_row, self.col] = "v"
                        self.row = first_row

        if self.facing == "left":

            # Touching the border
            if self.col == 0:
                last_col = np.max(np.where(field[self.row, ] != " "))
                if field[self.row, last_col] != "#":
                    self.field[self.row, last_col] = "<"
                    self.col = last_col
            else:
                next_tile = self.field[self.row, self.col-1]

                # Move by one tile
                if next_tile != " " and next_tile != "#":
                    self.field[self.row, self.col-1] = "<"
                    self.col -= 1

                # Jump over to the other side
                elif next_tile == " ":
                    last_col = np.max(np.where(field[self.row, ] != " "))
                    if field[self.row, last_col] != "#":
                        self.field[self.row, last_col] = "<"
                        self.col = last_col

        if self.facing == "up":

            # Touching the border
            if self.row == 0:
                last_row = np.max(np.where(field[:, self.col] != " "))
                if field[last_row, self.col] != "#":
                    self.field[last_row, self.col] = "^"
                    self.row = last_row

            else:
                next_tile = self.field[self.row-1, self.col]

                # Move by one tile
                if next_tile != " " and next_tile != "#":
                    self.field[self.row-1, self.col] = "^"
                    self.row -= 1

                # Jump over to the other side
                elif next_tile == " ":
                    last_row = np.max(np.where(field[:, self.col] != " "))
                    if field[last_row, self.col] != "#":
                        self.field[last_row, self.col] = "^"
                        self.row = last_row

    def turn(self, direction):
        if direction == "R":
            if self.facing == "right":
                self.facing = "down"
                self.field[self.row, self.col] = "v"

            elif self.facing == "down":
                self.facing = "left"
                self.field[self.row, self.col] = "<"

            elif self.facing == "left":
                self.facing = "up"
                self.field[self.row, self.col] = "^"

            elif self.facing == "up":
                self.facing = "right"
                self.field[self.row, self.col] = ">"

        elif direction == "L":
            if self.facing == "right":
                self.facing = "up"
                self.field[self.row, self.col] = "^"

            elif self.facing == "down":
                self.facing = "right"
                self.field[self.row, self.col] = ">"

            elif self.facing == "left":
                self.facing = "down"
                self.field[self.row, self.col] = "v"

            elif self.facing == "up":
                self.facing = "left"
                self.field[self.row, self.col] = "<"


print(notes)

game = Game(field, start_col)

for note in notes:
    # print("note:", note)
    try:
        num_moves = int(note)
        for _ in range(num_moves):
            game.move()
    except ValueError:
        game.turn(note)
    # print("(", game.row, game.col, ")", "\n", game.field)


def facing_to_number(facing):
    if facing == "v":
        return 1
    elif facing == "<":
        return 2
    elif facing == "^":
        return 3
    else:
        return 0


result = 1000 * (game.row + 1) + 4 * (game.col + 1) + facing_to_number(game.facing)
print("result=", result)