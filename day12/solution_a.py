import sys
from itertools import zip_longest

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())


def nr_pos(line, numbers):
    possibilities = 0
    possible_gaps = [c == "?" for c in line]
    possible_gap_locs = [idx for idx, c in enumerate(line) if c == "?"]
    total_possibilities = 2 ** sum(possible_gaps)
    for b in range(total_possibilities):
        bin_b = format(b, f"0{sum(possible_gaps)}b")
        line_try = [c for c in line]

        for idx, c in enumerate(bin_b):
            if c == "0":
                line_try[possible_gap_locs[idx]] = "."
            else:
                line_try[possible_gap_locs[idx]] = "#"
        if compatible("".join(line_try), numbers):
            possibilities += 1
    return possibilities


def compatible(gaps, numbers):
    actual_gaps = [g for g in gaps.split(".") if len(g) > 0]
    if len(actual_gaps) != len(numbers):
        return False
    for g, n in zip(actual_gaps, numbers):
        if len(g) != n:
            return False
    return True


total_possible = 0

for line in input_array:
    springs, numbers = line.split()
    numbers_l = [int(d) for d in numbers.split(",")]
    total_possible += nr_pos(springs, numbers_l)

print(total_possible)
