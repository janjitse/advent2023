import sys
import numpy as np
from collections import deque

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

mirror_array = np.array([[c for c in l] for l in input_array])


def bounds_check(pos, shape, dir, done):
    if 0 <= pos[0] < shape[0]:
        if 0 <= pos[1] < shape[1]:
            if (pos, dir) not in done:
                return True
    return False


mirror_map = {
    ".": lambda x: [x],
    "/": lambda x: [(-x[1], -x[0])],
    "\\": lambda x: [(x[1], x[0])],
    "|": lambda x: [(1, 0), (-1, 0)],
    "-": lambda x: [(0, 1), (0, -1)],
}


def energize_array(start_pos, start_dir):
    next_stack = deque([(start_pos, start_dir)])
    done = set()
    energized_array = np.zeros_like(mirror_array, dtype=np.int32)
    while next_stack:
        (pos, dir) = next_stack.popleft()
        energized_array[*pos] = 1
        next_dir_list = mirror_map[mirror_array[*pos]](dir)
        for next_dir in next_dir_list:
            next_pos = (pos[0] + next_dir[0], pos[1] + next_dir[1])
            if bounds_check(next_pos, mirror_array.shape, next_dir, done):
                next_stack.append((next_pos, next_dir))
                done.add((next_pos, next_dir))
    return np.sum(energized_array)


max_energized = 0
energy_a = energize_array((0, 0), (0, 1))

print(energy_a)
for start_row in range(mirror_array.shape[0]):
    energy = energize_array((start_row, 0), (0, 1))
    max_energized = max(energy, max_energized)
    energy = energize_array((start_row, mirror_array.shape[1] - 1), (0, -1))
    max_energized = max(energy, max_energized)

for start_col in range(mirror_array.shape[1]):
    energy = energize_array((0, start_col), (1, 0))
    max_energized = max(energy, max_energized)
    energy = energize_array((mirror_array.shape[0] - 1, start_col), (-1, 0))
    max_energized = max(energy, max_energized)


print(max_energized)
