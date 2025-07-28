import numpy as np
import galois

p = 79
GF = galois.GF(p)

# a = [1, z, x, y, v1, v2, v3]
L = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, -5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
])

R = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
])

O = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, -1, 0],
])

L = (L + p) % p
R = (R + p) % p
O = (O + p) % p

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)


x = GF(4)
y = GF((-2 + p) % p)
v1 = x * x
v2 = v1 * v1
v3 = GF((-5 + p) % p)* y * y
z = v3 * v1 + v2

witness = GF(np.array([1, z, x, y, v1, v2, v3]))

assert all(np.equal(
    np.matmul(L_galois, witness) * np.matmul(R_galois, witness),
    np.matmul(O_galois, witness)
)), "Not equal"

def interpolate_column(col):
    xs = GF(np.array([1, 2, 3, 4]))
    return galois.lagrange_poly(xs, col)

u_polynomials = np.apply_along_axis(
    interpolate_column,
    0,
    L_galois
)

v_polynomials = np.apply_along_axis(
    interpolate_column,
    0,
    R_galois
)

w_polynomials = np.apply_along_axis(
    interpolate_column,
    0,
    O_galois
)

print(u_polynomials[:2])
print(v_polynomials[:2])
print(w_polynomials[:1])
print()

for poly in u_polynomials:
    print(poly)
print()


for poly in w_polynomials:
    print(poly)
print()

