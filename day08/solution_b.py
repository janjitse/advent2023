import sys
from itertools import cycle
import math

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

print(origins)
steps = 0
all_done = False
instructions = cycle(instructions_raw)
cycle_times = [0 for _ in origins]
while not all_done:
    # if steps % 1000 == 0:
    #     print(origins)
    steps += 1
    direction = next(instructions)
    all_done = True
    if direction == "L":
        for origin_idx, origin in enumerate(origins):
            if cycle_times[origin_idx] > 0:
                continue
            next_step = node_map[origin][0]
            if not next_step.endswith("Z"):
                all_done = False
            if next_step.endswith("Z"):
                print(f"{origin_idx} done in {steps} steps")
                cycle_times[origin_idx] = steps
            origins[origin_idx] = next_step
    else:
        for origin_idx, origin in enumerate(origins):
            if cycle_times[origin_idx] > 0:
                continue
            next_step = node_map[origin][1]
            if not next_step.endswith("Z"):
                all_done = False
            if next_step.endswith("Z"):
                print(f"{origin_idx} done in {steps} steps")
                cycle_times[origin_idx] = steps
            origins[origin_idx] = next_step

outcome = 1
for c_t in cycle_times:
    outcome = outcome * c_t // math.gcd(outcome, c_t)
print(outcome)
