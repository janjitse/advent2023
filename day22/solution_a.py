import sys
from itertools import product
import numpy as np
from functools import lru_cache


input_array = []

with open(sys.path[0] + "/input_smallchallenge.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

bricks = []
max_coords = [0, 0, 0]
for l in input_array:
    brick_start, brick_end = l.split("~")
    brick_start_xyz = brick_start.split(",")
    brick_end_xyz = brick_end.split(",")
    xyz = [[], [], []]

    for i in range(3):
        max_coords[i] = max(
            max_coords[i], int(brick_start_xyz[i]), int(brick_end_xyz[i])
        )
        xyz[i] = [
            s
            for s in range(
                min(int(brick_start_xyz[i]), int(brick_end_xyz[i])),
                max(int(brick_start_xyz[i]), int(brick_end_xyz[i])) + 1,
            )
        ]
    brick = list(product(*xyz))
    bricks.append(brick)


bricks_sorted = sorted(bricks, key=lambda x: x[0][2])
bucket_settled = np.zeros(
    (max_coords[0] + 1, max_coords[1] + 1, max_coords[2] + 1), dtype=int
)
bucket_settled[:, :, 0] = -1
# fall down
max_settled = np.zeros((max_coords[0] + 1, max_coords[1] + 1), dtype=int)
new_bricks = []
for brick_idx, brick in enumerate(bricks_sorted, 1):
    max_drop = 0
    min_orig = max_coords[2]
    for xyz in brick:
        max_drop = max(max_settled[xyz[0], xyz[1]], max_drop)
        min_orig = min(min_orig, xyz[2])
    brick = [(xyz[0], xyz[1], xyz[2] - min_orig + max_drop + 1) for xyz in brick]
    for xyz in brick:
        max_settled[xyz[0], xyz[1]] = max(max_settled[xyz[0], xyz[1]], xyz[2])
        bucket_settled[xyz[0], xyz[1], xyz[2]] = brick_idx
    new_bricks.append(brick)
can_be_disintegrated = 0
sole_supporting_bricks = set()
supported_by = dict()

for brick_idx, brick in enumerate(new_bricks, 1):
    supporting = set()
    for xyz in brick:
        support = bucket_settled[xyz[0], xyz[1], xyz[2] - 1]
        if support > 0 and support != brick_idx:
            supporting.add(support)

    if len(supporting) == 1:
        sole_supporting_bricks = sole_supporting_bricks.union(supporting)
    supported_by[brick_idx] = supporting

print(len(bricks) - len(sole_supporting_bricks))


@lru_cache
def find_root(cur_item, removed):
    if len(supported_by[cur_item]) == 0:
        return set([cur_item])
    if cur_item == removed:
        return set([removed])
    roots = set()
    for d in supported_by[cur_item]:
        roots = roots.union(find_root(d, removed))
    return roots


total_fall_down = 0
for s in sole_supporting_bricks:
    s_root = set([s])
    fall_down = 0
    for t in range(1, len(bricks) + 1):
        if t == s:
            continue
        roots = find_root(t, s)
        if roots == s_root:
            fall_down += 1
    total_fall_down += fall_down

print(total_fall_down)
