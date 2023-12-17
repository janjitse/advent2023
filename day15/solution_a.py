import sys
import re
from collections import OrderedDict

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())


def hashmap(label):
    cur_value = 0
    for s in label:
        cur_value += ord(s)
        cur_value *= 17
        cur_value = cur_value % 256
    return cur_value


for l in input_array:
    total = 0
    split_list = l.split(",")
    for split in split_list:
        total += hashmap(split)
    print(total)


box = dict()
label_box_map = dict()

for l in input_array:
    split_list = l.split(",")
    for split in split_list:
        labels = re.split("-|=", split)
        label = labels[0]
        instr = split[len(labels[0])]
        label_h = hashmap(label)
        if instr == "=":
            focal_length = int(labels[1])
            if label_h in box:
                box[label_h][label] = focal_length
            else:
                box[label_h] = OrderedDict()
                box[label_h][label] = focal_length
            label_box_map[labels[0]] = label_h
        if instr == "-":
            if label in label_box_map:
                box_nr = label_box_map[label]
                box[label_h].pop(label)
                label_box_map.pop(label)
    total_focus_power = 0
    for box_nr, box_contents in box.items():
        for idx, (_, foc_length) in enumerate(box_contents.items()):
            total_focus_power += (box_nr + 1) * (idx + 1) * foc_length
    print(total_focus_power)
