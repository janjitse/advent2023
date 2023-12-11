import sys
import numpy as np
from queue import PriorityQueue

from typing import Tuple
from dataclasses import field, dataclass


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Tuple[int, int] = field(compare=False)


input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

pipe_array = np.array([[c for c in line] for line in input_array])
visited = np.zeros_like(pipe_array, dtype="bool")
start_point = np.nonzero(pipe_array == "S")
visited_queue = PriorityQueue()
starting_point = PrioritizedItem(0, (start_point[0][0], start_point[1][0]))
visited_queue.put(starting_point)

directions = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "S": [(1, 0), (-1, 0), (0, 1), (0, -1)],
}


def is_compatible(dir, pipe):
    if pipe == "|":
        if dir[0] != 0:
            return True
    if pipe == "-":
        if dir[1] != 0:
            return True
    if pipe == "L":
        if dir[0] == 1 or dir[1] == -1:
            return True
    if pipe == "J":
        if dir[0] == 1 or dir[1] == 1:
            return True
    if pipe == "7":
        if dir[0] == -1 or dir[1] == 1:
            return True
    if pipe == "F":
        if dir[0] == -1 or dir[1] == -1:
            return True
    return False


max_dist = 0


while not visited_queue.empty():
    next_item = visited_queue.get(starting_point)
    loc = (next_item.item[0], next_item.item[1])
    if visited[loc[0], loc[1]]:
        continue
    visited[loc[0], loc[1]] = True
    element = pipe_array[loc[0], loc[1]]
    priority = next_item.priority

    max_dist = max(priority, max_dist)
    for dir in directions[element]:
        if (
            0 <= loc[0] + dir[0] < pipe_array.shape[0]
            and 0 <= loc[1] + dir[1] < pipe_array.shape[1]
        ):
            next_elem = pipe_array[loc[0] + dir[0], loc[1] + dir[1]]
            if is_compatible(dir, next_elem):
                new_elem = PrioritizedItem(
                    priority + 1, (loc[0] + dir[0], loc[1] + dir[1])
                )
                visited_queue.put(new_elem)

print(max_dist)

for l in visited:
    print("".join("X" if c else "." for c in l))

visited_blown = visited.repeat(3, axis=1)
visited_blown = visited_blown.repeat(3, axis=0)

visited_mapping = {
    "|": np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype="bool"),
    "-": np.array([[False, False, False], [True, True, True], [False, False, False]]),
    "L": np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]], dtype="bool"),
    "J": np.array([[0, 1, 0], [1, 1, 0], [0, 0, 0]], dtype="bool"),
    "7": np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]], dtype="bool"),
    "F": np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]], dtype="bool"),
}

start_loc = starting_point.item
compatible_dirs = []
for dir in directions["S"]:
    if (
        0 <= start_loc[0] + dir[0] < pipe_array.shape[0]
        and 0 <= start_loc[1] + dir[1] < pipe_array.shape[1]
    ):
        next_elem = pipe_array[start_loc[0] + dir[0], start_loc[1] + dir[1]]
        if is_compatible(dir, next_elem):
            compatible_dirs.append(dir)
inv_map = {tuple(v): k for k, v in directions.items()}
start_type = inv_map[tuple(compatible_dirs)]
print(start_type)
pipe_array[start_loc[0], start_loc[1]] = start_type
for line_idx, line in enumerate(visited):
    for col_idx, col in enumerate(line):
        if col:
            visited_blown[
                line_idx * 3 : line_idx * 3 + 3, col_idx * 3 : col_idx * 3 + 3
            ] = visited_mapping[pipe_array[line_idx, col_idx]]

for l in visited_blown:
    print("".join("X" if c else "." for c in l))

flood_fill_queue = PriorityQueue()
start = PrioritizedItem(0, (0, 0))
directions_flood = [(0, 1), (0, -1), (-1, 0), (1, 0)]

flood_fill_queue.put(start)


while not flood_fill_queue.empty():
    next_item = flood_fill_queue.get()
    loc = (next_item.item[0], next_item.item[1])
    if visited_blown[loc[0], loc[1]]:
        continue
    visited_blown[loc[0], loc[1]] = True
    priority = next_item.priority

    for dir in directions_flood:
        if (
            0 <= loc[0] + dir[0] < visited_blown.shape[0]
            and 0 <= loc[1] + dir[1] < visited_blown.shape[1]
        ):
            if not visited_blown[loc[0] + dir[0], loc[1] + dir[1]]:
                new_elem = PrioritizedItem(
                    priority + 1, (loc[0] + dir[0], loc[1] + dir[1])
                )
                flood_fill_queue.put(new_elem)

interior_elems = 0


for l in visited_blown:
    print("".join("X" if c else "." for c in l))

for line_idx, line in enumerate(visited):
    for col_idx, col in enumerate(line):
        if not col:
            line_blown = line_idx * 3 + 1
            col_blown = col_idx * 3 + 1
            if not visited_blown[line_blown, col_blown]:
                interior_elems += 1
print(interior_elems)
