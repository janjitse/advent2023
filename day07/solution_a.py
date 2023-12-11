import sys
from collections import Counter
from functools import cmp_to_key

input_array = []

with open(sys.path[0] + "/input_large.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

hand_bid = []

card_value = {
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
for l in input_array:
    hand, bid = l.split()
    hand_list = [card_value[h] for h in hand]
    o = Counter(hand_list).most_common()
    hand_bid.append((o, hand_list, bid))


def compare_hands(hand1, hand2):
    for h1, h2 in zip(hand1[0], hand2[0]):
        if h1[1] != h2[1]:
            return h1[1] - h2[1]
    for h1, h2 in zip(hand1[1], hand2[1]):
        if h1 != h2:
            return h1 - h2
    return 0


sorted_hands = sorted(hand_bid, key=cmp_to_key(compare_hands))
total = 0
for idx, s in enumerate(sorted_hands, 1):
    total += idx * int(s[2])

print(total)
