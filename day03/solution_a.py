import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

symbol_pos = set()
gear_pos = dict()
for line_idx, line in enumerate(input_array):
    for col_idx, col in enumerate(line):
        if col not in "0123456789.":
            symbol_pos.add((line_idx, col_idx))
        if col == "*":
            gear_pos[(line_idx, col_idx)] = [0, 1]

total_parts = 0
total_gear_ratio = 0

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
for line_idx, line in enumerate(input_array):
    parse_nr = False
    gear_nr = 0
    gear_ratio = 1
    adj_gear_pos = (-1, -1)
    part_adjacent = False
    nr_so_far = ""
    for col_idx, col in enumerate(line):
        if col in "0123456789":
            if parse_nr:
                nr_so_far += col
            if not parse_nr:
                nr_so_far += col
                parse_nr = True
            for dir in directions:
                if (dir[0] + line_idx, dir[1] + col_idx) in symbol_pos:
                    part_adjacent = True
                if (dir[0] + line_idx, dir[1] + col_idx) in gear_pos:
                    if adj_gear_pos != (-1, -1) and adj_gear_pos != (
                        dir[0] + line_idx,
                        dir[1] + col_idx,
                    ):
                        print("WAT")
                    if adj_gear_pos != (dir[0] + line_idx, dir[1] + col_idx):
                        adj_gear_pos = (dir[0] + line_idx, dir[1] + col_idx)
                        gear_pos[adj_gear_pos][0] += 1
                        gear_nr = gear_pos[adj_gear_pos][0]

        else:
            if parse_nr:
                if part_adjacent:
                    # print(int(nr_so_far))
                    total_parts += int(nr_so_far)
                # print(gear_nr)
                if gear_nr == 1:
                    gear_pos[adj_gear_pos][1] *= int(nr_so_far)
                if gear_nr == 2:
                    gear_pos[adj_gear_pos][1] *= int(nr_so_far)
                    total_gear_ratio += gear_pos[adj_gear_pos][1]
                gear_nr = 0
                adj_gear_pos = (-1, -1)
                parse_nr = False
                part_adjacent = False
                nr_so_far = ""
    if parse_nr and part_adjacent:
        total_parts += int(nr_so_far)
        if gear_nr == 1:
            gear_pos[adj_gear_pos][1] *= int(nr_so_far)
        if gear_nr == 2:
            gear_pos[adj_gear_pos][1] *= int(nr_so_far)
            total_gear_ratio += gear_pos[adj_gear_pos][1]
print(total_parts)
print(total_gear_ratio)
