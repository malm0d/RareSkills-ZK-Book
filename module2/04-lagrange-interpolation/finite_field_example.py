import galois
import numpy as np

GF17 = galois.GF(17)

xs = GF17(np.array([1, 2, 3, 4]))
ys = GF17(np.array([4, 8, 2, 1]))

p = galois.lagrange_poly(xs, ys)

print(p)
# 11x^3 + 14x^2 + 4x + 9

assert p(1) == GF17(4)
# p(1) = 38 = 4 (mod 17)

assert p(2) == GF17(8)
# p(2) = 161 = 8 (mod 17)

assert p(3) == GF17(2)
# p(3) = 444 = 2 (mod 17)

assert p(4) == GF17(1)
# p(4) = 953 = 1 (mod 17)