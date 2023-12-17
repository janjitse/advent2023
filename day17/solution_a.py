import sys
import numpy as np
from queue import PriorityQueue
from collections import namedtuple

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

heat_map = np.array([[int(c) for c in l] for l in input_array])

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

other_directions = {
    (0, 1): [(1, 0), (-1, 0)],
    (0, -1): [(1, 0), (-1, 0)],
    (1, 0): [(0, 1), (0, -1)],
    (-1, 0): [(0, 1), (0, -1)],
}
max_cons = 10
min_cons = 4

min_dist = [
    [{dir: 1_000_000_000 for dir in directions} for _ in range(heat_map.shape[1])]
    for _ in range(heat_map.shape[0])
]

Item = namedtuple(
    "Item",
    ["dist", "pos", "dir"],
)

todo = PriorityQueue()

initial = Item(0, (0, 0), (1, 0))
initial2 = Item(0, (0, 0), (0, 1))

todo.put(initial)
todo.put(initial2)

counter = 0

while not todo.empty():
    counter += 1
    cur = todo.get()
    cur_min = min_dist[cur.pos[0]][cur.pos[1]][cur.dir]
    if cur.dist >= cur_min:
        continue
    min_dist[cur.pos[0]][cur.pos[1]][cur.dir] = min(cur_min, cur.dist)
    for dir in other_directions[cur.dir]:
        for step in range(min_cons, max_cons + 1):
            next_pos = (cur.pos[0] + step * dir[0], cur.pos[1] + step * dir[1])
            if (
                0 <= next_pos[0] < heat_map.shape[0]
                and 0 <= next_pos[1] < heat_map.shape[1]
            ):
                dist = sum(
                    [
                        heat_map[cur.pos[0] + s * dir[0], cur.pos[1] + s * dir[1]]
                        for s in range(1, step + 1)
                    ]
                )
                if cur.dist + dist < min_dist[next_pos[0]][next_pos[1]][dir]:
                    todo.put(Item(cur.dist + dist, next_pos, dir))

print(min(min_dist[-1][-1].values()))
print(f"Took {counter} iterations")
