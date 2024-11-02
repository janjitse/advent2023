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


def is_perfect_square(n):
    trial = int(math.isqrt(n))
    return trial * trial == n


matrix_A = [
    [
        [0, x12[i] / 2, x13[i] / 2],
        [x12[i] / 2, 0, x23[i] / 2],
        [x13[i] / 2, x23[i] / 2, 0],
    ]
    for i in range(3)
]


def det3(matrix):
    result = (
        matrix[0][0] * (matrix[1][1] * matrix[1][1] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[2][0] * matrix[1][1])
    )
    return result


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


matrix = np.array(matrix_A, dtype="object")
cofactor_matrix = np.zeros_like(matrix)
for z in range(3):
    for x in range(3):
        for y in range(3):
            submatrix = np.delete(np.delete(matrix[z, :, :], x, axis=0), y, axis=1)
            print(submatrix.shape)
            cofactor = det2(submatrix)
            cofactor_matrix[z, y, x] = (-1) ** (x + y) * cofactor

print(cofactor_matrix)
print(s.Matrix(matrix[0]))


matrix_S = [
    s.Matrix(
        [
            [0, x12[i], x13[i]],
            [x12[i], 0, x23[i]],
            [x13[i], x23[i], 0],
        ]
    )
    / 2
    for i in range(3)
]
for m in matrix_S:
    eig = m.eigenvals()
    for k in eig:
        print(s.N(k))
