import sys

input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

total = 0
for l in input_array:
    digit = ""
    for c in l:
        if "0" <= c <= "9":
            digit += c
    final_digit = digit[0] + digit[-1]
    total += int(final_digit)

print(total)

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

total = 0
for l in input_array:
    digit = []
    for i, c in enumerate(l):
        if "0" <= c <= "9":
            digit.append(int(c))
        for k in digits:
            if l[i:].startswith(k):
                digit.append(digits[k])
                break
    final_digit = 10 * digit[0] + digit[-1]
    total += final_digit

print(total)
