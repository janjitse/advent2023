import sys
import math
import numpy as np
from sympy.abc import x, y, z
from sympy import solveset, solve
import sympy as s
from sympy.solvers.diophantine import diophantine


input_array = []

with open(sys.path[0] + "/input.txt", "r") as f:
    for line in f:
        input_array.append(line.strip())

hailstones = []

for stone in input_array:
    pos, vel = stone.split("@")
    pos_xyz = tuple(int(x) for x in pos.strip().split(","))
    vel_xyz = tuple(int(x) for x in vel.strip().split(","))
    hailstones.append((pos_xyz, vel_xyz))

test_area = (7, 27)
test_area = (200000000000000, 400000000000000)


def check_area(pos, vel, deltat, vel_cross):
    if (
        test_area[0] * vel_cross
        <= pos[0] * vel_cross + deltat * vel[0]
        <= test_area[1] * vel_cross
    ):
        if (
            test_area[0] * vel_cross
            <= pos[1] * vel_cross + deltat * vel[1]
            <= test_area[1] * vel_cross
        ):
            return True
    return False


times_crosses = 0
for hail_idx, (pos, vel) in enumerate(hailstones):
    for posp, velp in hailstones[hail_idx + 1 :]:
        vel_cross = int(np.cross(vel[:2], velp[:2]))
        if vel_cross == 0:
            continue
        t_velcross = np.cross((posp[0] - pos[0], posp[1] - pos[1]), velp[:2])
        tp_velcross = -np.cross((pos[0] - posp[0], pos[1] - posp[1]), vel[:2])
        if vel_cross > 0:
            if t_velcross >= 0 and tp_velcross >= 0:
                if check_area(pos, vel, int(t_velcross), vel_cross):
                    times_crosses += 1
        else:
            if t_velcross <= 0 and tp_velcross <= 0:
                if check_area(pos, vel, -int(t_velcross), -vel_cross):
                    times_crosses += 1
print(times_crosses)


hail1 = hailstones[0]
hail2 = hailstones[1]
hail3 = hailstones[2]
hail1 = [np.array(hail1[0], dtype="object"), np.array(hail1[1], dtype="object")]
hail2 = [np.array(hail2[0], dtype="object"), np.array(hail2[1], dtype="object")]
hail3 = [np.array(hail3[0], dtype="object"), np.array(hail3[1], dtype="object")]


def cross(vec1, vec2):
    return np.array(
        (
            vec1[1] * vec2[2] - vec1[2] * vec2[1],
            vec1[2] * vec2[0] - vec1[0] * vec2[2],
            vec1[0] * vec2[1] - vec1[1] * vec2[0],
        ),
        dtype="object",
    )


def cross2(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]


x00 = -cross(hail1[0], hail3[0]) - cross(hail2[0], hail1[0]) + cross(hail2[0], hail3[0])
x10 = -cross(hail1[1], hail3[0]) - cross(hail2[0], hail1[1])
x20 = -cross(hail2[1], hail1[0]) + cross(hail2[1], hail3[0])
x30 = -cross(hail1[0], hail3[1]) + cross(hail2[0], hail3[1])
x12 = -cross(hail2[1], hail1[1])
x13 = -cross(hail1[1], hail3[1])
x23 = cross(hail2[1], hail3[1])
print(f"{x00=}")
print(f"{x10=}")
print(f"{x20=}")
print(f"{x30=}")
print(f"{x12=}")
print(f"{x13=}")
print(f"{x23=}")


def is_perfect_square(n):
    trial = int(math.isqrt(n))
    return trial * trial == n


def check_t(t2, t3):
    pos2 = (
        hail2[0][0] + t2 * hail2[1][0],
        hail2[0][1] + t2 * hail2[1][1],
        hail2[0][2] + t2 * hail2[1][2],
    )
    pos3 = (
        hail3[0][0] + t3 * hail3[1][0],
        hail3[0][1] + t3 * hail3[1][1],
        hail3[0][2] + t3 * hail3[1][2],
    )
    t2_t3_v_rock = (
        (pos2[0] - pos3[0]),
        (pos2[1] - pos3[1]),
        (pos2[2] - pos3[2]),
    )
    return all([t % (t2 - t3) == 0 for t in t2_t3_v_rock])


# solution = solveset(
#     x00 + x * x10 + y * x20 + z * x30 + x * y * x12 + x * z * x13 + y * z * x23,
#     [x, y, z],
# )
# for s in solution:
#     print(s)
t1s = s.Symbol("t1s", positive=True, integer=True)
t2s = s.Symbol("t2s", positive=True, integer=True)
t3s = s.Symbol("t3s", positive=True, integer=True)

solution = solve(
    x00
    + t1s * x10
    + t2s * x20
    + t3s * x30
    + t1s * t2s * x12
    + t1s * t3s * x13
    + t2s * t3s * x23,
    [t1s, t2s, t3s],
)
for s in solution:
    print(s)

t1 = 312937963270
t2 = 206089287849
t3 = 61443247226

for t3 in range(61443247226 - 10, 61443247226 + 10):
    if t3 % 1_000_000 == 0:
        print(t3)
    const_a = x10 + t3 * x13
    const_b = x00 + t3 * x30
    fac_a = x12
    fac_b = x20 + t3 * x23
    # print(f"{const_a=}")
    # print(f"{const_b=}")
    # print(f"{fac_a=}")
    # print(f"{fac_b=}")
    alpha0_12 = cross2(fac_a, fac_b)
    alpha1_12 = cross2(const_a, fac_b) + cross2(fac_a, const_b)
    alpha2_12 = cross2(const_a, const_b)
    alpha0_23 = cross2(fac_a[1:], fac_b[1:])
    alpha1_23 = cross2(const_a[1:], fac_b[1:]) + cross2(fac_a[1:], const_b[1:])
    alpha2_23 = cross2(const_a[1:], const_b[1:])

    discr21 = alpha1_12**2 - 4 * alpha0_12 * alpha2_12
    discr23 = alpha1_23**2 - 4 * alpha0_23 * alpha2_23
    print(f"{discr21=}")
    print(f"{discr23=}")
    if (
        discr21 > 0
        and discr23 > 0
        and is_perfect_square(discr21)
        and is_perfect_square(discr23)
    ):
        t21p = divmod(int(-alpha1_12 + math.isqrt(discr21)), int(2 * alpha0_12))
        t21m = divmod(int(-alpha1_12 - math.isqrt(discr21)), int(2 * alpha0_12))
        t23p = divmod(int(-alpha1_23 + math.isqrt(discr23)), int(2 * alpha0_23))
        t23m = divmod(int(-alpha1_23 - math.isqrt(discr23)), int(2 * alpha0_23))
    else:
        continue
    # print(t21p, t21m, t23p, t23m)

    if t21p[1] == 0 and t23p[1] == 0:
        if t21p[0] == t23p[0]:
            if t21p[0] > 0:
                t2 = t21p[0]
                if check_t(t2, t3):
                    break
    if t21p[1] == 0 and t23m[1] == 0:
        if t21p[0] == t23m[0]:
            if t21p[0] > 0:
                t2 = t21p[0]
                if check_t(t2, t3):
                    break
    if t21m[1] == 0 and t23p[1] == 0:
        if t21m[0] == t23p[0]:
            if t21m[0] > 0:
                t2 = t21m[0]
                if check_t(t2, t3):
                    break
    if t21m[1] == 0 and t23m[1] == 0:
        if t21m[0] == t23m[0]:
            if t21m[0] > 0:
                t2 = t21m[0]
                if check_t(t2, t3):
                    break
# t2 = solution[0][y]
# t3 = solution[0][z]
print(t2, t3)
# found = False
# min_dist_sq = 1e15
# min_dist_sol = (0, 0, 0)

# matrix = [
#     [
#         [0, x12[i] / 2, x13[i] / 2],
#         [x12[i] / 2, 0, x23[i] / 2],
#         [x13[i] / 2, x23[i] / 2, 0],
#     ]
#     for i in range(3)
# ]

# def deriv(t1, t2, t3):
#     derivatives = np.array(
#         [
#             x10 + t3 * x13 + t2 * x12,
#             x20 + t1 * x12 + t3 * x23,
#             x30 + t2 * x23 + t1 * x12,
#         ]
#     )
#     return np.dot(derivatives, func(t1, t2, t3))


# def func(t1, t2, t3):
#     sol = (
#         x00
#         + t1 * x10
#         + t2 * x20
#         + t3 * x30
#         + t1 * t2 * x12
#         + t1 * t3 * x13
#         + t2 * t3 * x23
#     )
#     return sol
# matrix = np.array(matrix)
# cofactor_matrix = np.zeros_like(matrix)
# for z in range(3):
#     for x in range(3):
#         for y in range(3):
#             submatrix = np.delete(np.delete(matrix[z, :, :], x, axis=0), y, axis=1)
#             cofactor = np.linalg.det(submatrix)
#             cofactor_matrix[z, y, x] = (-1) ** (x + y) * cofactor

# t_s = np.array([0, 0, 0], dtype=np.float64)
# counter = 0
# print(x00)
# print(x10)
# print(x20)
# print(x30)
# while not np.all(func(t_s[0], t_s[1], t_s[2]) == 0):
#     counter += 1
#     if counter > 100:
#         break

#     # coord = np.argmax(abs(der))
#     der = deriv(*t_s)
#     print(f"{der=}")
#     t_s -= 0.001 * der
#     print(func(t_s[0], t_s[1], t_s[2]))
#     # for coord in range(3):
#     #     print(f"{der=}")
#     #     print(func(t_s[0], t_s[1], t_s[2]))
#     #     print(t_s)
#     #     if der[coord] > 0 and t_s[coord] > 0:
#     #         t_s[coord] -= 1
#     #     elif der[coord] < 0:
#     #         t_s[coord] += 1
#     #     else:
#     #         continue


# print(t_s)

# for t1 in range(10):
#     subsol = x00 + t1 * x10
#     for t2 in range(10):
#         subsubsol = subsol + t2 * x20 + t1 * t2 * x12
#         dir = x30 + t1 * x13 + t2 * x23
#         t3 = [0, 0, 0]
#         # print(t1, t2)
#         # print(dir)
#         # print(subsubsol)
#         # for i in range(3):
#         #     if dir[i] != 0:
#         #         t3[i] = -subsubsol[i]
#         #     else:
#         #         t3[i] == -1
#         # print(t3)
#         if int(dir[1]) * int(subsubsol[0]) == int(dir[0]) * int(subsubsol[1]):
#             if int(dir[2]) * int(subsubsol[1]) == int(dir[1]) * int(subsubsol[2]):
#                 print(t1, t2, -subsubsol[0] / dir[0])
#                 found = True
#                 break
#         # for t3 in range(1000):
#         #     sol
#         #     # sol = (
#         #     #     x00
#         #     #     + t1 * x10
#         #     #     + t2 * x20
#         #     #     + t3 * x30
#         #     #     + t1 * t2 * x12
#         #     #     + t1 * t3 * x13
#         #     #     + t2 * t3 * x23
#         #     # )
#         #     # print(sol)
#         #     if (
#         #         math.sqrt(int(sol[0]) ** 2 + int(sol[1]) ** 2 + int(sol[2]) ** 2)
#         #         < min_dist_sq
#         #     ):
#         #         min_dist_sq = math.sqrt(
#         #             int(sol[0]) ** 2 + int(sol[1]) ** 2 + int(sol[2]) ** 2
#         #         )
#         #         min_dist_sol = (t1, t2, t3)
#         #     if np.all(sol == 0):
#         #         print(t1, t2, t3)
#         #         found = True
#         #         break

#         if found:
#             break
#     if found:
#         break

# pos1 = (
#     hail1[0][0] + t1 * hail1[1][0],
#     hail1[0][1] + t1 * hail1[1][1],
#     hail1[0][2] + t1 * hail1[1][2],
# )
pos2 = (
    hail2[0][0] + t2 * hail2[1][0],
    hail2[0][1] + t2 * hail2[1][1],
    hail2[0][2] + t2 * hail2[1][2],
)
pos3 = (
    hail3[0][0] + t3 * hail3[1][0],
    hail3[0][1] + t3 * hail3[1][1],
    hail3[0][2] + t3 * hail3[1][2],
)
t2_t3_v_rock = (
    (pos2[0] - pos3[0]),
    (pos2[1] - pos3[1]),
    (pos2[2] - pos3[2]),
)
p_rock = (
    pos2[0] - t2 * t2_t3_v_rock[0] // (t2 - t3),
    pos2[1] - t2 * t2_t3_v_rock[1] // (t2 - t3),
    pos2[2] - t2 * t2_t3_v_rock[2] // (t2 - t3),
)
print([i / (t2 - t3) for i in t2_t3_v_rock])
print(p_rock)
print(sum(p_rock))
