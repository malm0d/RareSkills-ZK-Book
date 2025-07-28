import numpy as np
import galois
from functools import reduce

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

def inner_product_polynomials_with_witness(polys, witness):
    mul_ = lambda x, y: x * y
    sum_ = lambda x, y: x + y
    # reduce(func, iterable[])
    return reduce(sum_, map(mul_, polys, witness))

term1_ux = inner_product_polynomials_with_witness(u_polynomials, witness)

term2_vx = inner_product_polynomials_with_witness(v_polynomials, witness)

term3_wx = inner_product_polynomials_with_witness(w_polynomials, witness)

#t = (x - 1)(x - 2)(x - 3)(x - 4)
t = galois.Poly([1, 78], field=GF) * galois.Poly([1, 77], field=GF) * galois.Poly([1, 76], field=GF) * galois.Poly([1, 75], field=GF)

# Floor division with `t`
h = (term1_ux * term2_vx - term3_wx) // t

print(term1_ux) # 78x^3 + 76x^2 + 28x + 59
print(term2_vx) # 11x^3 + 77x^2 + 20x + 54
print(term3_wx) # 3x^3 + 40x^2 + 20x + 32
print(t)        # x^4 + 69x^3 + 35x^2 + 29x + 24
print(h)        # 68x^2 + 17x + 59

assert term1_ux * term2_vx == term3_wx + (h * t), "Division has a remainder"