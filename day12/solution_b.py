import sys
from functools import lru_cache

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())


@lru_cache
def nr_compatible(springs, numbers):
    # print(springs, numbers)
    if len(numbers) == 0:
        if "#" in springs:
            return 0
        else:
            return 1
    if len(springs) < sum(numbers) + len(numbers) - 1:
        return 0
    n = numbers[0]
    total_possible = 0
    for i in range(len(springs) - n + 1):
        if "#" in springs[:i]:
            break
        if i + n < len(springs) and springs[i + n] == "#":
            continue
        if not "." in springs[i : i + n]:
            total_possible += nr_compatible(springs[i + n + 1 :], numbers[1:])
    return total_possible


total_sum = 0
for line in input_array:
    springs, numbers = line.split()
    number_l = tuple([int(i) for i in numbers.split(",")] * 5)
    springs = "?".join([springs] * 5)
    total_sum += nr_compatible(springs, number_l)
print(total_sum)
