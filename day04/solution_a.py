import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

total_points = 0
total_cards = dict()
for line_idx, line in enumerate(input_array, 1):
    if line_idx in total_cards:
        total_cards[line_idx] += 1
    else:
        total_cards[line_idx] = 1
    _, numbers = line.strip().split(":")
    winning_numbers, your_numbers = numbers.strip().split("|")
    winning_numbers_set = set(int(i) for i in winning_numbers.strip().split())
    total_occ = 0
    for your_number in your_numbers.strip().split():
        if int(your_number) in winning_numbers_set:
            total_occ += 1
    if total_occ > 0:
        total_points += 2 ** (total_occ - 1)
        x_cards = total_cards[line_idx]
        for s in range(1, total_occ + 1):
            if s + line_idx in total_cards:
                total_cards[s + line_idx] += x_cards
            else:
                total_cards[s + line_idx] = x_cards
print(total_cards)
print(total_points)
print(sum([v for k, v in total_cards.items()]))
