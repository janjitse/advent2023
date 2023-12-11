import sys
import math

input_array = []

with open(sys.path[0] + "/input_small.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

times = [int(t) for t in input_array[0].split(":")[1].strip().split()]
distances = [int(t) for t in input_array[1].split(":")[1].strip().split()]

nr_ways = []

for t, d in zip(times, distances):
    cur_nr = 0
    for time_press_down in range(t):
        distance_traveled = (t - time_press_down) * time_press_down
        if distance_traveled > d:
            cur_nr += 1
    nr_ways.append(cur_nr)


total = 1
for n in nr_ways:
    total *= n
print(total)

total_time = int("".join(str(t) for t in times))
total_distance = int("".join(str(d) for d in distances))
# (total_time - time_press_down) * time_press_down - total_distance == 0
# total_time * time_press_down - time_press_down**2 - total_distance
# time_press_down = -total_time +/- sqrt(total_time**2 + 4* total_distance)/ -2
start_solutions = 0.5 * (-total_time - math.sqrt(total_time**2 - 4 * total_distance))
end_solutions = 0.5 * (-total_time + math.sqrt(total_time**2 - 4 * total_distance))

print(total_time)
print(total_distance)
print(end_solutions)
total_solutions = int(math.sqrt(total_time**2 - 4 * total_distance))
print(int(math.floor(start_solutions)) - int(math.ceil(end_solutions)))
