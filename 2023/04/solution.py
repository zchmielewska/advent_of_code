import numpy as np
import re


def clean_string(input_string):
    cleaned_string = input_string.strip()
    cleaned_string = ' '.join(cleaned_string.split())
    return cleaned_string


def get_games(filename):
    with open(filename) as file:
        games = []
        for line in file:
            parts = re.split(r"[:|]", line.strip())
            parts = [clean_string(p) for p in parts]
            games.append((re.split(" ", parts[1]), re.split(" ", parts[2])))
    return games


def solve1(filename):
    games = get_games(filename)
    total = 0
    for game in games:
        common = set(game[0]).intersection(set(game[1]))
        if len(common) == 0:
            score = 0
        else:
            score = 2**(len(common)-1)
        total += score
    return total


def solve2(filename):
    games = get_games(filename)
    counts = np.ones(len(games), dtype=int)
    for i, game in enumerate(games):
        num_cards = counts[i]
        num_common = len(set(game[0]).intersection(set(game[1])))
        for j in range(i+1, i+num_common+1):
            if j < len(counts):
                counts[j] += num_cards
    return sum(counts)


print(solve1("data.txt"))
print(solve2("data.txt"))
