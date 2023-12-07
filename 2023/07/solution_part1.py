from collections import Counter


class Card:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.type = hand_to_type(hand)

    def __repr__(self):
        return f"Card: {self.hand} (bid={self.bid}, type={self.type})"

    def __gt__(self, other):
        if self.type == other.type:
            return is_greater(self.hand, other.hand)
        else:
            return self.type > other.type


def get_cards(filename):
    with open(filename) as file:
        cards = []
        for line in file:
            hand, bid = line.strip().split()
            hand = list(hand)
            bid = int(bid)
            card = Card(hand, bid)
            cards.append(card)
    return cards


def hand_to_type(hand):
    counts = Counter(hand)
    values = list(counts.values())
    values.sort(reverse=True)

    if values == [5]:
        return 7
    elif values == [4, 1]:
        return 6
    elif values == [3, 2]:
        return 5
    elif values == [3, 1, 1]:
        return 4
    elif values == [2, 2, 1]:
        return 3
    elif values == [2, 1, 1, 1]:
        return 2
    else:
        return 1


def is_greater(hand1, hand2):
    dct = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    for i in range(5):
        if dct.get(hand1[i]) > dct.get(hand2[i]):
            return True
        elif dct.get(hand1[i]) < dct.get(hand2[i]):
            return False

    return True


def solve(filename):
    cards = get_cards(filename)
    sorted_cards = sorted(cards)
    wins = [sorted_cards[i].bid * (i+1) for i in range(len(sorted_cards))]
    return sum(wins)


print(solve("data.txt"))
