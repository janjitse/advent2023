import sys
import numpy as np

input_array = []

with open(sys.path[0] + "/aoc-2023-day-11-challenge-3.in", "r") as f:
    for line in f:
        input_array.append(line.strip())

galaxy_array = np.array([[c for c in line] for line in input_array])

row_empty = [0 for _ in range(galaxy_array.shape[0])]
col_empty = [0 for _ in range(galaxy_array.shape[1])]


for row_idx in range(galaxy_array.shape[0]):
    if np.all(galaxy_array[row_idx, :] == "."):
        row_empty[row_idx] = 1

for col_idx in range(galaxy_array.shape[1]):
    if np.all(galaxy_array[:, col_idx] == "."):
        col_empty[col_idx] = 1


galaxy_loc2 = np.nonzero(galaxy_array == "#")
galaxy_loc2 = list(zip(*galaxy_loc2))

print(len(galaxy_loc2))
for exp_rate in [2, int(1e6)]:
    new_locs = []
    for loc in galaxy_loc2:
        expansion_row = sum(row_empty[: loc[0]]) * (exp_rate - 1)
        expansion_col = sum(col_empty[: loc[1]]) * (exp_rate - 1)
        new_loc = (loc[0] + expansion_row, loc[1] + expansion_col)
        new_locs.append(new_loc)

    total_dist = 0
    new_locs_s_row = sorted(new_locs, key=lambda x: x[0])
    new_locs_s_col = sorted(new_locs, key=lambda x: x[1])
    nr_locs = len(new_locs_s_row)

    prev_dist_row = sum(int(x[0]) - int(new_locs_s_row[0][0]) for x in new_locs_s_row)
    prev_dist_col = sum(int(x[1]) - int(new_locs_s_col[0][1]) for x in new_locs_s_col)

    total_dist = prev_dist_row + prev_dist_col
    for idx in range(1, nr_locs):
        next_dist_row = prev_dist_row - (nr_locs - idx) * (
            int(new_locs_s_row[idx][0]) - int(new_locs_s_row[idx - 1][0])
        )
        next_dist_col = prev_dist_col - (nr_locs - idx) * (
            int(new_locs_s_col[idx][1]) - int(new_locs_s_col[idx - 1][1])
        )

        total_dist += next_dist_row
        total_dist += next_dist_col
        prev_dist_row = next_dist_row
        prev_dist_col = next_dist_col

    print(total_dist)
