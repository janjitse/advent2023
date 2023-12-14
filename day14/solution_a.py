import sys
import numpy as np

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

total_array = np.array([[c for c in l] for l in input_array])


def move_north(array):
    for line_idx, line in enumerate(array):
        for col_idx, col in enumerate(line):
            if col == "O":
                filled_sites = np.where(array[:line_idx, col_idx] != ".")[0]
                if filled_sites.size > 0:
                    max_north = filled_sites[-1] + 1
                else:
                    max_north = 0
                array[line_idx, col_idx] = "."
                array[max_north, col_idx] = "O"
    return array


def move_west(array):
    for col_idx in range(array.shape[1]):
        for line_idx in range(array.shape[0]):
            if array[line_idx, col_idx] == "O":
                filled_sites = np.where(array[line_idx, :col_idx] != ".")[0]
                if filled_sites.size > 0:
                    max_west = filled_sites[-1] + 1
                else:
                    max_west = 0
                array[line_idx, col_idx] = "."
                array[line_idx, max_west] = "O"

    return array


def move_south(array):
    for line_idx in range(array.shape[0] - 1, -1, -1):
        for col_idx in range(array.shape[1]):
            if array[line_idx, col_idx] == "O":
                filled_sites = np.where(array[line_idx + 1 :, col_idx] != ".")[0]

                if filled_sites.size > 0:
                    max_south = filled_sites[0] + line_idx
                else:
                    max_south = array.shape[0] - 1
                array[line_idx, col_idx] = "."
                array[max_south, col_idx] = "O"
    return array


def move_east(array):
    for col_idx in range(array.shape[1] - 1, -1, -1):
        for line_idx in range(array.shape[0]):
            if array[line_idx, col_idx] == "O":
                filled_sites = np.where(array[line_idx, col_idx + 1 :] != ".")[0]
                if filled_sites.size > 0:
                    max_east = filled_sites[0] + col_idx
                else:
                    max_east = array.shape[1] - 1
                array[line_idx, col_idx] = "."
                array[line_idx, max_east] = "O"
    return array


def calc_weight(array):
    total_weight = 0
    for row_idx, row in enumerate(array[::-1], 1):
        for col in row:
            if col == "O":
                total_weight += row_idx
    return total_weight


print(calc_weight(move_north(total_array)))


def hash_a(array):
    return hash(array.tobytes())


def cycle(array):
    array = move_north(array)
    array = move_west(array)
    array = move_south(array)
    array = move_east(array)
    return array.copy(), hash_a(array)


array = total_array.copy()

recur_dict = {}
nr_iterations = 1_000_000_000

for c in range(nr_iterations):
    array, hashed = cycle(array)
    weight = calc_weight(array)

    if hashed in recur_dict:
        if len(recur_dict[hashed]) > 2:
            break
        recur_dict[hashed].append((c, weight))
    else:
        recur_dict[hashed] = [(c, weight)]

for v in recur_dict.values():
    if len(v) > 1:
        period = v[-1][0] - v[-2][0]
        if nr_iterations % period == (v[-1][0] + 1) % period:
            print(v[-1][1])
            break
