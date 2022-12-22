import re

filename = "./input/21/example.txt"


class Monkey:
    def __init__(self, name, formula):
        self.name = name
        self.formula = formula
        self.value = None
        self.child1 = None
        self.child2 = None
        self.op = None

    def __repr__(self):
        return f"{self.name} ({self.formula})"


def get_monkeys(filename):
    monkeys = []
    with open(filename) as file:
        for line in file:
            name, formula = line.rstrip('\n').split(": ")
            monkeys.append(Monkey(name, formula))
    return monkeys


monkeys = get_monkeys(filename)
print(monkeys)

# jeżeli eval formula to children = 0
for monkey in monkeys:
    try:
        monkey.value = int(monkey.formula)
    except ValueError:
        pattern_text = r"(?P<child1>\w{4}) (?P<op>.{1}) (?P<child2>\w{4})"
        pattern = re.compile(pattern_text)
        match = pattern.match(monkey.formula)
        child1, op, child2 = match.groups()
        monkey.c