import sys
import re
from operator import gt, lt
from copy import deepcopy

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    workflow, ratings = f.read().strip().split("\n\n")

rules = dict()
for rule in workflow.split("\n"):
    rule_name, rule_cont, _ = re.split("{|}", rule)
    rule_list = rule_cont.split(",")
    rules_parsed = []
    for r in rule_list:
        if ":" in r:
            cond, dest = r.split(":")
            if ">" in cond:
                check, quality = cond.split(">")
                quality = int(quality)
                gate = (check, gt, quality, ">")
                rules_parsed.append((gate, dest))
            if "<" in cond:
                check, quality = cond.split("<")
                quality = int(quality)
                gate = (check, lt, quality, "<")
                rules_parsed.append((gate, dest))
        else:
            gate = tuple()
            rules_parsed.append((gate, r))
    rules[rule_name] = rules_parsed

rating_list = []
for r in ratings.split():
    rating_item = dict()
    r_p = r[1:-1]
    quality_value = r_p.split(",")
    for q in quality_value:
        q_p, q_value = q.split("=")
        rating_item[q_p] = int(q_value)
    rating_list.append(rating_item)

accepted_value = 0

for item in rating_list:
    cur_rule = "in"
    while True:
        # print(f"Checking {item} at rule {cur_rule}")
        for r in rules[cur_rule]:
            if len(r[0]) > 0:
                if r[0][1](item[r[0][0]], r[0][2]):
                    new_dest = r[1]
                    break
            else:
                new_dest = r[1]
        if new_dest == "R":
            # print(f"Rejected {item} at rule {cur_rule} for {r}")
            break
        if new_dest == "A":
            # print(f"Accepted at rule {cur_rule}: {item}")
            accepted_value += sum(item.values())
            break
        else:
            cur_rule = new_dest
print(accepted_value)

# Depth first recursive search
initial_restrictions = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}


def recurse(cur_rule, restrictions):
    possibilities = 0
    for r in rules[cur_rule]:
        if len(r[0]) < 1:
            if r[1] == "A":
                total = 1
                for v in restrictions.values():
                    total *= v[1] - v[0] + 1
                possibilities += total
            elif r[1] == "R":
                break
            else:
                possibilities += recurse(r[1], restrictions)
        else:
            new_restrictions = deepcopy(restrictions)
            if r[0][3] == ">":
                new_restrictions[r[0][0]][0] = max(
                    r[0][2] + 1, new_restrictions[r[0][0]][0]
                )
                restrictions[r[0][0]][1] = min(r[0][2], restrictions[r[0][0]][1])

            if r[0][3] == "<":
                new_restrictions[r[0][0]][1] = min(
                    r[0][2] - 1, new_restrictions[r[0][0]][1]
                )
                restrictions[r[0][0]][0] = max(r[0][2], restrictions[r[0][0]][0])
            if new_restrictions[r[0][0]][0] > new_restrictions[r[0][0]][1]:
                continue
            else:
                if r[1] == "A":
                    total = 1
                    for v in new_restrictions.values():
                        total *= v[1] - v[0] + 1
                    possibilities += total
                elif r[1] != "R":
                    possibilities += recurse(r[1], new_restrictions)
                if restrictions[r[0][0]][0] > restrictions[r[0][0]][1]:
                    break
    return possibilities


print(recurse("in", initial_restrictions))
