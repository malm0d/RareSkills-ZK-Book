import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GF(np.array([1, 2]))

def L(v):
    return galois.lagrange_poly(x_common, v)

p1 = L(GF(np.array([6, 4])))
p2 = L(GF(np.array([3, 7])))
q1 = L(GF(np.array([3, 12])))
q2 = L(GF(np.array([9, 6])))

print(p1)
# 15x + 8 (mod 17)
print(p2)
# 4x + 16 (mod 17)
print(q1)
# 9x + 11 (mod 17)
print(q2)
# 14x + 12 (mod 17)

import random
u = random.randint(0, p)

# Random point: u
tau = GF(u)

# p1(x) * 2 + p2(x) * 4
lhs = p1(tau) * GF(2) + p2(tau) * GF(4)

# q1(x) * 2 + q2(x) * 2
rhs = q1(tau) * GF(2) + q2(tau) * GF(2)

# Assert equality -> true
assert lhs == rhs