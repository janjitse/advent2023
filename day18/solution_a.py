import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())


dir_dict = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
dir2_dict = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


corners = [[], []]
turns = [[], []]
cur_cor = [(0, 0), (0, 0)]
for c, c_c in zip(corners, cur_cor):
    c.append(c_c)
prev_dir = [(0, 0), (0, 0)]
first_dir = [None, None]
edge_amount = [0, 0]
for l in input_array:
    direction_a, amount_a, color = l.split()
    amount = [int(amount_a), int(color[2:-2], 16)]
    direction_b = int(color[-2])
    dir = [dir_dict[direction_a], dir2_dict[direction_b]]
    for idx, (a, d, c, t, p_d) in enumerate(zip(amount, dir, corners, turns, prev_dir)):
        new_corner = (
            cur_cor[idx][0] + a * d[0],
            cur_cor[idx][1] + a * d[1],
        )
        edge_amount[idx] += a - 1
        if p_d[0] * d[1] > 0 or p_d[1] * d[0] < 0:
            t.append("L")
        elif p_d[0] * d[1] < 0 or p_d[1] * d[0] > 0:
            t.append("R")
        c.append(new_corner)
        cur_cor[idx] = new_corner
        prev_dir[idx] = d
        if first_dir[idx] is None:
            first_dir[idx] = d

for idx in range(2):
    if dir[idx][0] * first_dir[idx][1] > 0 or dir[idx][1] * first_dir[idx][0] < 0:
        turns[idx] = ["L"] + turns[idx]
    else:
        turns[idx] = ["R"] + turns[idx]

for idx in range(2):
    area = 0
    for idx_c, cor in enumerate(corners[idx][1:], 1):
        prev_cor = corners[idx][idx_c - 1]
        area += cor[0] * prev_cor[1] - prev_cor[0] * cor[1]
    left_corners = sum([1 for l in turns[idx] if l == "L"])
    right_corners = sum([1 for l in turns[idx] if l == "R"])
    corner_amount = left_corners + 3 * right_corners

    print(abs(area) // 2 + corner_amount // 4 + edge_amount[idx] // 2)
