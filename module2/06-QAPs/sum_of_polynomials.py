import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GF(np.array([1, 2, 3]))

def L(v):
    return galois.lagrange_poly(x_common, v)

# Arbitray vectors
# Note that we are dealing with field elements of GF(17)
v1 = GF(np.array([4, 8, 2]))
v2 = GF(np.array([1, 6, 12]))
v3 = GF(np.array([7, 4, 10]))
v4 = GF(np.array([3, 15, 9]))

assert L(v1 + v2) == L(v1) + L(v2)
assert L(v3 + v4) == L(v3) + L(v4)
assert L(v1 + v4) == L(v1) + L(v4)
assert L(v2 + v3) == L(v2) + L(v3)