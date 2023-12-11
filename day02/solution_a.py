import sys
from typing import List

input_array: List[str] = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

sum_ids = 0
total_power = 0
for idx, line in enumerate(input_array, 1):
    start = line.index(":")
    rounds = line[start + 1 :].split(";")
    min_blue = 0
    min_red = 0
    min_green = 0
    power = 0
    for r in rounds:
        colors = r.strip().split(",")
        for c in colors:
            digit, color = c.strip().split()
            if color.strip() == "red":
                min_red = max(int(digit), min_red)
            if color.strip() == "green":
                min_green = max(int(digit), min_green)
            if color.strip() == "blue":
                min_blue = max(int(digit), min_blue)
    # print(min_red, min_green, min_blue)
    power = min_red * min_green * min_blue
    total_power += power
    if min_red <= 12 and min_green <= 13 and min_blue <= 14:
        sum_ids += idx

print(sum_ids)

print(total_power)
