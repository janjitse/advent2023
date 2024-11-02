import sys
from queue import Queue
from math import gcd


class Node:
    def __init__(self, type_n, dest):
        self.destinations = dest
        self.source = None
        self.type = type_n
        self.state = None


input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

modules = {}
for l in input_array:
    name_t, dest = l.split(" -> ")
    if name_t.startswith("%"):
        m_type = "flipflop"
        name = name_t[1:]
        state = "off"
    elif name_t.startswith("&"):
        m_type = "conjunction"
        name = name_t[1:]
        state = {}
    else:
        m_type = "broadcast"
        name = name_t
        state = "same"
    dest_list = [d for d in dest.split(", ")]
    modules[name] = [m_type, dest_list, state]
print(modules)

modules["output"] = ["other", [], "none"]

conjunctions = {
    name: state[2] for name, state in modules.items() if state[0] == "conjunction"
}
for m in modules:
    for d in modules[m][1]:
        if d in conjunctions:
            modules[d][2][m] = False

print(conjunctions)
flipflops = {
    name: state[2] for name, state in modules.items() if state[0] == "flipflop"
}
print(flipflops)

print(modules["kz"])
all_flip_flops_off = False
pulse_counter = {"low": 0, "high": 0}
buttons_pressed = 0
rx_pulsed = 0
cycles = {d: [] for d in modules["kz"][2]}
print(cycles)
# while not all_flip_flops_off:
for i in range(10_000):
    for c in conjunctions:
        if not all(conjunctions[c].values()):
            if c in modules["kz"][2]:
                print(c, buttons_pressed, modules[c])
    if rx_pulsed > 0:
        break
    pulses = Queue()
    initial_pulse = ("button", "low", "broadcaster")
    buttons_pressed += 1
    if buttons_pressed % 1_000 == 0:
        print(buttons_pressed)
    pulses.put(initial_pulse)
    while not pulses.empty():
        source, signal, dest = pulses.get()
        if buttons_pressed <= 1000:
            pulse_counter[signal] += 1
        # print(f"{source}, {signal}, {dest}")
        if dest in modules:
            new_type, dest_l, state = modules[dest]
        elif dest == "rx":
            if signal == "low":
                rx_pulsed += 1
            continue
        if new_type == "broadcast":
            for d in dest_l:
                pulses.put((dest, signal, d))
        elif new_type == "flipflop":
            if signal == "high":
                continue
            if signal == "low":
                if state == "on":
                    modules[dest][2] = "off"
                    flipflops[dest] = "off"
                    for d in dest_l:
                        pulses.put((dest, "low", d))
                else:
                    modules[dest][2] = "on"
                    flipflops[dest] = "on"
                    for d in dest_l:
                        pulses.put((dest, "high", d))
        elif new_type == "conjunction":
            if signal == "high":
                modules[dest][2][source] = True
            else:
                modules[dest][2][source] = False

            if all(modules[dest][2].values()):
                output = "low"
            else:
                output = "high"
                if dest in modules["kz"][2]:
                    print(dest, buttons_pressed, modules[dest])
                    cycles[dest].append(buttons_pressed)
            for d in dest_l:
                pulses.put((dest, output, d))

    # all_flip_flops_off = all([f == "off" for f in flipflops.values()])

print(cycles)
print(rx_pulsed)
print(pulse_counter)
print(buttons_pressed)
print(pulse_counter["high"] * pulse_counter["low"])

lcm = 1
for v in cycles.values():
    lcm *= v[0] // gcd(v[0], lcm)
print(lcm)
