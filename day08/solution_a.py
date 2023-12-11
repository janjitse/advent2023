import sys
from itertools import cycle

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    all_input = f.read().strip()

instructions_raw, nodes = all_input.split("\n\n")

instructions = cycle(instructions_raw)

node_map = dict()
first_origin = "AAA"
origins = []
for line in nodes.split("\n"):
    origin, dests = line.strip().split("=")
    left_dest, right_dest = dests.strip()[1:-1].split(",")
    node_map[origin.strip()] = (left_dest.strip(), right_dest.strip())
    if origin.strip().endswith("A"):
        origins.append(origin.strip())
    # if first_origin is None:
    #     first_origin = origin.strip()

steps = 0
while first_origin != "ZZZ":
    direction = next(instructions)
    if direction == "L":
        first_origin = node_map[first_origin][0]
    else:
        first_origin = node_map[first_origin][1]
    steps += 1
print(steps)
