import re

filename = "./input/21/data.txt"


class Monkey:
    def __init__(self, name, formula):
        self.name = name
        self.formula = formula
        self.value = None
        self.child1 = None
        self.child2 = None
        self.op = None
        self.children = []
        self.grandchildren = []

    def __repr__(self):
        return f"{self.name} [{self.value}]"

    def __lt__(self, other):
        return len(self.grandchildren) < len(other.grandchildren)

    def calculate(self):
        try:
            self.value = int(monkey.formula)
        except ValueError:
            self.value = eval(f"{self.child1.value} {self.op} {self.child2.value}")


def unique_extend(lst1, lst2):
    output = lst1.copy()
    for item in lst2:
        if item not in lst1:
            output.append(item)
    return output


def get_monkeys(filename):
    monkeys = []
    with open(filename) as file:
        for line in file:
            name, formula = line.rstrip('\n').split(": ")
            monkeys.append(Monkey(name, formula))
    return monkeys


def get_monkey_by_name(name, monkeys):
    for monkey in monkeys:
        if monkey.name == name:
            return monkey
    return None


def set_children(monkeys):
    for monkey in monkeys:
        try:
            int(monkey.formula)
        except ValueError:
            pattern_text = r"(?P<child1>\w{4}) (?P<op>.{1}) (?P<child2>\w{4})"
            pattern = re.compile(pattern_text)
            match = pattern.match(monkey.formula)
            child1, op, child2 = match.groups()
            if monkey.name == "root":
                op = "=="
            monkey.child1 = get_monkey_by_name(child1, monkeys)
            monkey.child2 = get_monkey_by_name(child2, monkeys)
            monkey.children = [monkey.child1, monkey.child2]
            monkey.op = op
    return monkeys


def set_grandchildren(monkeys):
    for monkey in monkeys:
        if monkey.child1 is not None:
            monkey.grandchildren = [monkey.child1, monkey.child2]
            i = 0
            while i < len(monkey.grandchildren):
                grandchild = monkey.grandchildren[i]
                monkey.grandchildren = unique_extend(monkey.grandchildren, grandchild.children)
                i += 1
    return monkeys


monkeys = get_monkeys(filename)
monkeys = set_children(monkeys)
monkeys = set_grandchildren(monkeys)
monkeys = sorted(monkeys)

humn = get_monkey_by_name("humn", monkeys)
root = get_monkey_by_name("root", monkeys)

humn.formula = 0
for monkey in monkeys:
    monkey.calculate()


# For the future --> I used semi binary search here
i = 366552086 * 10**4
while not root.value:
# while i < 11:
# while i <= 366552087 * 10**4:
    # if i % 10**3 == 0:
    # print("i=", i)
    humn.formula = i
    for monkey in monkeys:
        monkey.calculate()
    diff = root.child1.value-root.child2.value
    # print("child1:", root.child1.value, "child2:", root.child2.value, "diff:", diff)
    # i += 10**3
    i += 1

print(root.child1.value)
print(root.child2.value)
print(root.value)
print(i-1)
