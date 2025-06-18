# *** Elliptic Curve Point Multiplication ***
# EC point multiplication is repeated point addition.
# E.g. 135G => Point doubling and caching from G to 128G, then 128G + 4G + 2G + G.

# *** Python BN128 Library ***
# The library the EVM implementation pyEVM uses for the elliptic curve precompiles is py_ecc
from py_ecc.bn128 import G1, multiply, add, eq, neg

print(G1)
# G1 point: (1, 2)

print(add(G1, G1))
# (1368015179489954701390400359078579693043519447331113978918064868415326638035, 
# 9918110051302171585080402603319702774565515993150576347155970296011118125764)

print(multiply(G1, 2))
#(1368015179489954701390400359078579693043519447331113978918064868415326638035, 
# 9918110051302171585080402603319702774565515993150576347155970296011118125764)

assert eq(add(G1, G1), multiply(G1, 2))
# True

# 10G + 11G = 21G
assert eq(add(multiply(G1, 10), multiply(G1, 11)), multiply(G1, 21))
# True

# Adding a point to itself results in the same value as “multiplying” a point by 2. 
# The two points above are clearly the same point. The tuple is still an (x, y) pair, just over a very large domain.
# Point values are extremely large for a good reason as we want to prevent attackers from taking an elliptic curve point
# (the group) and computing the field element (finite field) that generated it. If the order of our cyclic group is too
# small, then the attacker can just brute force it. Small group orders make solving the Discrete log problem easy, since
# security depends on the difficulty of reversing scalar multiplication i.e. finding k given Q = kP, and the inability 
# to efficiently map curve points back to field elements.

# The following code generates the first 1000 points on the BN128 curve:
import matplotlib.pyplot as plt
from py_ecc.bn128 import G1, multiply, neg
import math
import numpy as np
xs = []
ys = []
for i in range(1,1000):
    xs.append(i)
    ys.append(int(multiply(G1, i)[1]))
    xs.append(i)
    ys.append(int(neg(multiply(G1, i))[1]))
plt.scatter(xs, ys, marker='.')
plt.show()

# Compared to the previous plot, this example used a larger field modulus and a different point
# for the generator (G).