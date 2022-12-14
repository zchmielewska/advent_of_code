import os


def snafu_to_decimal(value):
    value = str(value)
    n = len(value)-1
    result = 0
    for i in range(n, -1, -1):
        item = value[i]
        if item == "=":
            item = -2
        if item == "-":
            item = -1
        item = int(item)
        power = n-i
        result += item * (5**power)
    return result


def decimal_to_snafu(value):
    result = ""
    while value > 0:
        quotient = value // 5
        remainder = value % 5

        if remainder == 3:
            quotient += 1
            remainder = "="

        if remainder == 4:
            quotient += 1
            remainder = "-"
        result = str(remainder) + result
        value = quotient
    return result


def solve(filename):
    snafus = []
    with open(filename) as file:
        for line in file:
            snafus.append(line.rstrip('\n'))

    total = sum([snafu_to_decimal(snafu) for snafu in snafus])
    return decimal_to_snafu(total)


filename = os.path.join(os.path.dirname(__file__), "data.txt")
print(solve(filename))  # 2-1=10=1=1==2-1=-221
