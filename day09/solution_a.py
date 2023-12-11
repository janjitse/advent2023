import sys
import numpy as np

input_array = []

with open(sys.path[0] + "/input_large.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

total = 0
total_previous = 0
for line in input_array:
    values = np.array([int(d) for d in line.split()], dtype="O")
    subseq_values = [values]
    while np.any(subseq_values[-1]) and subseq_values[-1].shape[0] > 1:
        subseq_values.append(subseq_values[-1][1:] - subseq_values[-1][:-1])
    expected = 0
    previous = 0
    for value in subseq_values[::-1]:
        expected = expected + value[-1]
        previous = value[0] - previous
    total_previous += previous
    total += expected
print(f"total predicted: {total}")
print(f"total history: {total_previous}")
