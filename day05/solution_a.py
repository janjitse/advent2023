import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    almanac = f.read().strip().split("\n\n")

start_pos_str = almanac[0].split(":")[1].strip()
positions = set([int(b) for b in start_pos_str.split()])

for almanac_page in almanac[1:]:
    range_descr = almanac_page.split("\n")[1:]
    new_positions = set()
    found = set()
    for r in range_descr:
        dest_start, source_start, rang = [int(t) for t in r.split()]
        for pos in positions:
            if source_start <= pos < source_start + rang:
                new_pos = pos - source_start + dest_start
                new_positions.add(new_pos)
                found.add(pos)
    for remain_pos in positions - found:
        new_positions.add(remain_pos)
    positions = new_positions
print(min(positions))

start_ranges_raw = [int(b) for b in start_pos_str.split()]
ranges = sorted(
    [
        (s, s + start_ranges_raw[2 * idx + 1])
        for idx, s in enumerate(start_ranges_raw[::2])
    ]
)

for almanac_page in almanac[1:]:
    range_descr = almanac_page.split("\n")[1:]
    map_name = almanac_page.split("\n")[0]
    source_ranges_map = []
    for r in range_descr:
        dest_start, source_start, rang = (int(t) for t in r.split())
        source_ranges_map.append(
            (source_start, source_start + rang - 1, dest_start - source_start)
        )
    source_ranges_map = sorted(source_ranges_map)
    additional_elements = []
    if source_ranges_map[0][0] > 0:
        additional_elements.append((0, source_ranges_map[0][0] - 1, 0))
    for idx, (source_start, _, _) in enumerate(source_ranges_map[1:], 1):
        if source_ranges_map[idx - 1][1] < source_start - 1:
            additional_elements.append(
                (source_ranges_map[idx - 1][1] + 1, source_start - 1, 0)
            )
    source_ranges_map = sorted(source_ranges_map + additional_elements)
    dest_ranges = []
    for start, end in ranges:
        for source_start, source_end, offset in source_ranges_map:
            if start >= source_start and start <= source_end:
                dest_ranges.append((start + offset, min(source_end, end) + offset))
                if end <= source_end:
                    break
                start = source_end + 1
        if start > source_ranges_map[-1][1]:
            dest_ranges.append((start, end))
    # Merge the found ranges for an extra optimization
    ranges = []
    dest_ranges = sorted(dest_ranges)
    start = dest_ranges[0][0]
    end = dest_ranges[0][1]
    for idx, (s, e) in enumerate(dest_ranges[:-1]):
        if end + 1 >= dest_ranges[idx + 1][0]:
            end = max(dest_ranges[idx + 1][1], end)
        else:
            ranges.append((start, end))
            start = dest_ranges[idx + 1][0]
            end = dest_ranges[idx + 1][1]
    ranges.append((start, end))

print(ranges[0][0])
