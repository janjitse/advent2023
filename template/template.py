import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())
