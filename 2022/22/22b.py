import numpy as np
import re

#   A B
#   C
# D E
# F

filename = "./input/22/data.txt"

rows = []
with open(filename) as file:
    for line in file:
        row = line.rstrip('\n')
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


def facing_to_number(facing):
    if facing == "v":
        return 1
    elif facing == "<":
        return 2
    elif facing == "^":
        return 3
    else:
        return 0


class Game:
    def __init__(self, field, start_col):
        self.field = field
        self.facing = "right"
        self.row = 0
        self.col = start_col

    def move(self):
        if self.facing == "right":
            at_border = self.col == self.field.shape[1]-1
            if not at_border:
                next_tile = self.field[self.row, self.col + 1]
                at_border = next_tile == " "

            # Jump over to the other side
            if at_border:
                # segment B (--> E) [1]
                if self.row < 50:
                    new_row = 149 - self.row
                    new_col = 99
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "left"

                # segment C (--> B) [2]
                elif self.row < 100:
                    new_row = 49
                    new_col = 100 + (self.row - 50)
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "up"

                # segment E (--> B) [3]
                elif self.row < 150:
                    new_row = 49 - (self.row - 100)
                    new_col = 149
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "left"

                # segment F (--> E) [4]
                else:
                    new_row = 149
                    new_col = 50 + (self.row - 150)
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "up"
            # Move by one tile
            else:
                next_tile = self.field[self.row, self.col + 1]
                if next_tile != " " and next_tile != "#":
                    self.field[self.row, self.col+1] = ">"
                    self.col += 1

        elif self.facing == "down":
            at_border = self.row == self.field.shape[0]-1
            if not at_border:
                next_tile = self.field[self.row+1, self.col]
                at_border = next_tile == " "

            if at_border:
                # segment F (--> B) [5]
                if self.col < 50:
                    new_row = 0
                    new_col = 100 + self.col
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "down"

                # segment E (--> F) [6]
                elif self.col < 100:
                    new_row = 150 + (self.col - 50)
                    new_col = 49
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "left"

                # segment B (--> C) [7]
                else:
                    new_row = 50 + (self.col - 100)
                    new_col = 99
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "left"
            else:
                next_tile = self.field[self.row+1, self.col]
                if next_tile != " " and next_tile != "#":
                    self.field[self.row+1, self.col] = "v"
                    self.row += 1

        elif self.facing == "left":
            at_border = self.col == 0
            if not at_border:
                next_tile = self.field[self.row, self.col-1]
                at_border = next_tile == " "

            if at_border:
                # segment A (--> D) [8]
                if self.row < 50:
                    new_row = 149 - self.row
                    new_col = 0
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "right"

                # segment C (--> D) [9]
                elif self.row < 100:
                    new_row = 100
                    new_col = self.row - 50
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "down"

                # segment D (--> A) [10]
                elif self.row < 150:
                    new_row = 49 - (self.row - 100)
                    new_col = 50
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "right"

                # segment F (--> A) [11]
                else:
                    new_row = 0
                    new_col = 50 + (self.row - 150)
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "down"
            else:
                next_tile = self.field[self.row, self.col-1]
                if next_tile != " " and next_tile != "#":
                    self.field[self.row, self.col-1] = "<"
                    self.col -= 1

        elif self.facing == "up":
            at_border = self.row == 0
            if not at_border:
                next_tile = self.field[self.row-1, self.col]
                at_border = next_tile == " "

            if at_border:
                # segment D (--> C) [12]
                if self.col < 50:
                    new_row = 50 + self.col
                    new_col = 50
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "right"

                # segment A (--> F) [13]
                elif self.col < 100:
                    new_row = 150 + (self.col - 50)
                    new_col = 0
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "right"

                # segment B (--> F) [14]
                else:
                    new_row = 199
                    new_col = self.col - 100
                    if field[new_row, new_col] != "#":
                        self.row = new_row
                        self.col = new_col
                        self.facing = "up"
            else:
                next_tile = self.field[self.row-1, self.col]
                if next_tile != " " and next_tile != "#":
                    self.field[self.row-1, self.col] = "^"
                    self.row -= 1

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


field = get_field(rows)
notes = get_notes(rows)
start_col = np.min(np.where(field[0, ] == "."))
field[0, start_col] = ">"
game = Game(field, start_col)

for note in notes:
    try:
        num_moves = int(note)
        for _ in range(num_moves):
            game.move()
    except ValueError:
        game.turn(note)


result = 1000 * (game.row + 1) + 4 * (game.col + 1) + facing_to_number(game.facing)
print("result=", result)
