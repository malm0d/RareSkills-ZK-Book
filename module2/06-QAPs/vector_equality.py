import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GF(np.array([1,2,3]))

def L(v):
    return galois.lagrange_poly(x_common, v)

w = L(GF(np.array([2,4,8])))

print(w)