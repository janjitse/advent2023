import sys
import numpy as np

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    input_array = f.read().strip().split("\n\n")

total = 0
total_b = 0
for block in input_array:
    block_np = np.array([[c for c in l] for l in block.split()])
    for col_idx in range(1, block_np.shape[1]):
        max_cols = min(col_idx, block_np.shape[1] - col_idx)
        orig_col = block_np[:, col_idx - max_cols : col_idx]
        reflected_col = np.flip(block_np[:, col_idx : col_idx + max_cols], axis=1)

        if np.all(orig_col == reflected_col):
            total += col_idx
        if np.sum(np.logical_not(orig_col == reflected_col)) == 1:
            total_b += col_idx
    for row_idx in range(1, block_np.shape[0]):
        max_rows = min(row_idx, block_np.shape[0] - row_idx)
        orig_row = block_np[row_idx - max_rows : row_idx, :]
        reflected_row = np.flip(block_np[row_idx : row_idx + max_rows, :], axis=0)

        if np.all(orig_row == reflected_row):
            total += row_idx * 100
        if np.sum(np.logical_not(orig_row == reflected_row)) == 1:
            total_b += row_idx * 100
print(total)
print(total_b)
