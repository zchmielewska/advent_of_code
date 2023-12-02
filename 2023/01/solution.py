
def to_digit(word):
    digits = {
        "one":   "1",
        "two":   "2",
        "three": "3",
        "four":  "4",
        "five":  "5",
        "six":   "6",
        "seven": "7",
        "eight": "8",
        "nine":  "9",
    }
    for key in digits:
        if key in word:
            return digits[key]
    return None


def solve2(filename):
    total = 0
    with (open(filename) as file):
        for line in file:
            value = ""

            # forward
            word = ""
            for ch in line.strip():
                # is a number?
                try:
                    int(ch)
                    value += ch
                    break
                except ValueError:
                    pass

                # is a spelled number?
                word += ch
                digit = to_digit(word)
                if digit is not None:
                    value += digit
                    break

            # backward
            word = ""
            for i in range(len(line) - 1, -1, -1):
                ch = line[i]

                # is a number?
                try:
                    int(ch)
                    value += ch
                    break
                except ValueError:
                    pass

                # is a spelled number?
                word = ch + word
                digit = to_digit(word)
                if digit is not None:
                    value += digit
                    break

            total += int(value)
    return total


def solve1(filename):
    total = 0
    with open(filename) as file:
        for line in file:
            value = ""

            # forward
            for ch in line.strip():
                try:
                    int(ch)
                    value += ch
                    break
                except ValueError:
                    pass

            # backward
            for i in range(len(line)-1, -1, -1):
                ch = line[i]
                try:
                    int(ch)
                    value += ch
                    break
                except ValueError:
                    pass

            total += int(value)

    return total


answer1 = solve1("data1.txt")
print(answer1)

answer2 = solve2("data2.txt")
print(answer2)
