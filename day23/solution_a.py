import sys
import numpy as np
from graphlib import TopologicalSorter
import networkx as nx
import graphviz
from queue import Queue

sys.setrecursionlimit(999999)

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

forest = np.array([[c for c in line] for line in input_array])
start_pos_x = np.where(forest[0] == ".")[0][0]
start_pos = (0, start_pos_x)
end_pos_x = np.where(forest[-1] == ".")[0][0]
end_pos = (forest.shape[0] - 1, end_pos_x)

print(end_pos)


def check_comp(pos, dir):
    if forest[pos[0], pos[1]] == ".":
        return True
    if forest[pos[0], pos[1]] == ">" and dir == (0, 1):
        return True
    if forest[pos[0], pos[1]] == "<" and dir == (0, -1):
        return True
    if forest[pos[0], pos[1]] == "v" and dir == (1, 0):
        return True
    if forest[pos[0], pos[1]] == "^" and dir == (0, -1):
        return True
    return False


def check_comp2(pos):
    if forest[pos[0], pos[1]] != "#":
        return True
    return False


directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]


def recurse(pos, path, prev_dir):
    max_length = 0
    any_possible = False
    if pos == end_pos:
        return (len(path), True)
    for d in directions:
        if d == prev_dir:
            continue
        new_pos = (pos[0] + d[0], pos[1] + d[1])
        if 0 <= new_pos[0] < forest.shape[0]:
            if 0 <= new_pos[1] < forest.shape[1]:
                if new_pos not in path:
                    if check_comp(new_pos, d):
                        new_path = path | {new_pos}
                        length, possible = recurse(new_pos, new_path, (-d[0], -d[1]))
                        if possible:
                            max_length = max(max_length, length)
                            any_possible = True
    return max_length, any_possible


# length, _ = recurse(start_pos, frozenset(), (-1, 0))
# print(length)

graph = dict()


for line_idx, line in enumerate(forest):
    for col_idx, c in enumerate(line):
        if c in [".", ">", "<", "v", "^"]:
            graph[(line_idx, col_idx)] = []
            for d in directions:
                new_pos = (line_idx + d[0], col_idx + d[1])
                if 0 <= new_pos[0] < forest.shape[0]:
                    if 0 <= new_pos[1] < forest.shape[1]:
                        if forest[new_pos[0], new_pos[1]] in [".", ">", "<", "v", "^"]:
                            graph[(line_idx, col_idx)].append(new_pos)

max_k = 0
for e in graph:
    max_k = max(max_k, len(graph[e]))

reduced_graph = dict()

q = Queue()

q.put(start_pos)
visited = set()

while not q.empty():
    cur = q.get()
    visited.add(cur)
    reduced_graph_edges = {}
    for d in graph[cur]:
        trial = d
        prev_trial = cur
        weight = 1
        while len(graph[trial]) == 2:
            weight += 1
            for next_e in graph[trial]:
                if next_e != prev_trial:
                    prev_trial = trial
                    trial = next_e
                    break
        reduced_graph_edges[trial] = {"weight": weight}
        if trial not in visited:
            q.put(trial)
    reduced_graph[cur] = reduced_graph_edges


counter = 0


def recurse_graph(pos, path, prev_pos):
    global counter
    max_length = 0
    any_possible = False
    if pos == end_pos:
        path_lengths = [x["weight"] for x in path.values()]
        return (sum(path_lengths), True)
    for next_pos, weight in reduced_graph[pos].items():
        if next_pos == prev_pos:
            continue
        counter += 1
        if next_pos not in path:
            path[next_pos] = weight
            length, possible = recurse_graph(next_pos, path, pos)
            del path[next_pos]
            if possible:
                max_length = max(max_length, length)
                any_possible = True
    return max_length, any_possible


# length, _ = recurse_graph(start_pos, dict(), (-1, -1))
# print(length)
# print(counter)

# graphx = nx.DiGraph(reduced_graph)
# print(graphx)

# print(graphx.is_planar(graphx))
# print(reduced_graph)

visualization = np.array([[" " for c in l] for l in forest])
for key in sorted(reduced_graph.keys(), key=lambda x: x[0]):
    visualization[key[0], key[1]] = "#"


for k in range(visualization.shape[0] - 1, -1, -1):
    if np.all(visualization[k, :] == " "):
        visualization = np.delete(visualization, k, axis=0)

for k in range(visualization.shape[1] - 1, -1, -1):
    if np.all(visualization[:, k] == " "):
        visualization = np.delete(visualization, k, axis=1)

for l in visualization:
    print("".join(l))

ts = TopologicalSorter(graph=reduced_graph)
print(list(ts.static_order()))
