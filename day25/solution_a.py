import sys
import networkx as nx
from random import sample

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

graph = dict()
graphx = nx.Graph()
for l in input_array:
    source, others = l.split(":")
    otherlist = others.split()
    graph[source] = otherlist
    for t in otherlist:
        graphx.add_edge(source, t, capacity=1.0)


print(graphx)
print(nx.number_connected_components(graphx))
s = sample(list(graphx), 1)[0]
for t in graphx:
    if s == t:
        continue

    cut = nx.minimum_edge_cut(graphx, s=s, t=t)
    if len(cut) == 3:
        print(s, t, cut)

        graphx.remove_edges_from(cut)

        break

print([len(g) for g in nx.connected_components(graphx)])
size_conn = [len(g) for g in nx.connected_components(graphx)]
start = 1
for s in size_conn:
    start *= s
print(start)
