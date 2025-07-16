import galois
import numpy as np
import random

p = 103
GF = galois.GF(p)

#Common set of x values
x_common = GF(np.array([1, 2, 3]))

# Arbitrary vectors
A = GF(np.array([4,8,19]))
B = GF(np.array([4,8,19]))

# Lagrange interpolating polynomials
fx = galois.lagrange_poly(x_common, A)
gx = galois.lagrange_poly(x_common, B)

# Pick u from [0, p)
u = random.randint(0, p)

# f(u) = g(u)
lhs = fx(u)
rhs = gx(u)

# Only one check required
assert lhs == rhs

#----------------------------------------

# Arbitrary vectors that are not equal
C = GF(np.array([5, 13, 29]))
D = GF(np.array([7, 17, 23]))

# Lagrange interpolating polynomials
cx = galois.lagrange_poly(x_common, C)
dx = galois.lagrange_poly(x_common, D)

# f(u) = g(u)
lhs_ = cx(u)
rhs_ = dx(u)

assert lhs_ != rhs_