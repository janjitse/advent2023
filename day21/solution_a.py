import sys
import numpy as np

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

garden = np.array([[c for c in line] for line in input_array])

garden_width = garden.shape[1]
garden_height = garden.shape[0]
print(garden_width)
print(garden_height)

s_pos = np.where(garden == "S")
start_pos = (s_pos[0][0], s_pos[1][0])


prev_step = set()
prev_step.add(start_pos)
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

pos_dict = {start_pos: set([(0, 0)])}
print(pos_dict)
patterns = {
    (0, 0): [],
    (0, 1): [],
    (0, -1): [],
    (1, 0): [],
    (-1, 0): [],
    (1, 1): [],
    (1, -1): [],
    (-1, 1): [],
    (-1, -1): [],
    # (0, 2): [],
    # (0, -2): [],
    # (2, 0): [],
    # (2, 1): [],
    # (2, 2): [],
    # (1, 2): [],
}
for steps in range(400):
    new_pos_dict = dict()
    for p, copies in pos_dict.items():
        for d in directions:
            next_trial = p[0] + d[0], p[1] + d[1]
            if (
                garden[next_trial[0] % garden_height, next_trial[1] % garden_width]
                != "#"
            ):
                if 0 <= next_trial[0] < garden_height:
                    if 0 <= next_trial[1] < garden_width:
                        new_copies = copies
                        new_pos = next_trial
                    elif next_trial[1] < 0:
                        new_copies = {(p[0], p[1] - 1) for p in copies}
                        new_pos = (next_trial[0], next_trial[1] % garden_width)
                    elif next_trial[1] >= garden_height:
                        new_pos = (next_trial[0], next_trial[1] % garden_width)
                        new_copies = {(p[0], p[1] + 1) for p in copies}
                    else:
                        new_pos = None
                elif next_trial[0] < 0:
                    if 0 <= next_trial[1] < garden_width:
                        new_copies = {(p[0] - 1, p[1]) for p in copies}
                        new_pos = (next_trial[0] % garden_height, next_trial[1])
                    elif next_trial[1] < 0:
                        new_copies = {(p[0] - 1, p[1] - 1) for p in copies}
                        new_pos = (
                            next_trial[0] % garden_height,
                            next_trial[1] % garden_width,
                        )
                    elif next_trial[1] >= garden_height:
                        new_pos = (
                            next_trial[0] % garden_height,
                            next_trial[1] % garden_width,
                        )
                        new_copies = {(p[0] - 1, p[1] + 1) for p in copies}
                    else:
                        new_pos = None
                elif next_trial[0] >= garden_height:
                    if 0 <= next_trial[1] < garden_width:
                        new_copies = {(p[0] + 1, p[1]) for p in copies}
                        new_pos = (next_trial[0] % garden_height, next_trial[1])
                    elif next_trial[1] < 0:
                        new_copies = {(p[0] + 1, p[1] - 1) for p in copies}
                        new_pos = (
                            next_trial[0] % garden_height,
                            next_trial[1] % garden_width,
                        )
                    elif next_trial[1] >= garden_height:
                        new_pos = (
                            next_trial[0] % garden_height,
                            next_trial[1] % garden_width,
                        )
                        new_copies = {(p[0] + 1, p[1] + 1) for p in copies}
                    else:
                        new_pos = None
                else:
                    new_pos = None
                if new_pos:
                    new_pos_dict[new_pos] = new_pos_dict.get(new_pos, set()).union(
                        new_copies
                    )
    pos_dict = new_pos_dict
    for block in patterns:
        patterns[block].append(
            (
                steps + 1,
                sum([len([p for p in c if p == block]) for c in pos_dict.values()]),
            )
        )


pattern_start = dict()
start = dict()

for block in patterns:
    print(patterns[block])
    for step, val in patterns[block]:
        if val == 1:
            start[block] = step
        if val == 7553:
            pattern_start[block] = step
            break
print(pattern_start)
print(start)

total_steps = 26501365

total_vis = 0


interior_even_blocks = 0
interior_odd_blocks = 0
partial_blocks = []
start_straight = 66
size_edges = 131
for block_type in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
    for x in range(1, (total_steps - start_straight) // size_edges + 2):
        initial_start = 132
        start_blocks = (
            total_steps - initial_start - (x - 1) * size_edges
        ) // size_edges + 1
        initial_end = 260

        end_blocks = max(
            (total_steps - initial_end - x * size_edges) // size_edges + 1, 0
        )
        even_full_blocks = min(end_blocks // 2 + (x + 1) % 2, end_blocks)
        odd_full_blocks = end_blocks - even_full_blocks
        for t in range(start_blocks - end_blocks):
            time_since_entry = (
                total_steps
                - (start_blocks - t - 1) * size_edges
                - initial_start
                - (x - 1) * size_edges
            )
            partial_blocks.append(((block_type), time_since_entry))

        interior_even_blocks += even_full_blocks
        interior_odd_blocks += odd_full_blocks

# Straight lines through the middle:
for block_type in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    initial_start = start_straight
    start_blocks = (total_steps - initial_start) // size_edges + 1
    initial_end = 260
    end_blocks = max((total_steps - initial_end) // size_edges + 1, 0)
    even_full_blocks = min((end_blocks - 1) // 2 + (x + 1) % 2, end_blocks)
    odd_full_blocks = end_blocks - even_full_blocks
    for t in range(start_blocks - end_blocks):
        time_since_entry = (
            total_steps - (start_blocks - t - 1) * size_edges - initial_start
        )
        partial_blocks.append(((block_type), time_since_entry))
    interior_even_blocks += even_full_blocks
    interior_odd_blocks += odd_full_blocks

total = (
    interior_even_blocks * 7553 * ((total_steps + 1) % 2)
    + interior_even_blocks * 7541 * (total_steps % 2)
    + (interior_odd_blocks + 1) * 7553 * (total_steps % 2)
    + (interior_odd_blocks + 1) * 7541 * ((total_steps + 1) % 2)
)
print(f"full block total = {total}")

for p in partial_blocks:
    # print(patterns[p[0]][start[p[0]] - 1 :])
    # print(p[1])
    total += patterns[p[0]][start[p[0]] - 1 :][p[1]][1]
print(total)
