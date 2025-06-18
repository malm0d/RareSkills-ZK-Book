# *** HOMOMORPHISM between modular addition and elliptic curve addition ***
# Addition in a finite field is HOMOMORPHIC to addition among elliptic curve points (when their order is equal).
# Because of the discrete logarithm, another party can add elliptic curve points together without knowing which 
# field elements generated those points.

# *** Implementation details about the HOMOMORPHISM between modular addition and elliptic curve addition ***
# Recall:
# Field modulus => The prime number defining the finite field (the modulus we do the curve over)
# Curve order => The number of points on the elliptic curve
# These are NOT the same!
#
# Case in point:
# If we start with the point R, and we add the curve order o, we will get R back. BUT, if we add the
# field modulus F instead, we wil get a different point.
from py_ecc.bn128 import G1, curve_order, field_modulus, G1, add, multiply, eq

print(G1) 
# (1, 2)
print(curve_order)
# o = 21888242871839275222246405745257275088548364400416034343698204186575808495617
print(field_modulus)
# F = 21888242871839275222246405745257275088696311157297823662689037894645226208583

x = 5 # chosen randomly

# This passes [5G = (5 + o)G]
assert eq(multiply(G1, x), multiply(G1, x + curve_order))

# This fails [5G =/= (5 + F)G]
# assert eq(multiply(G1, x), multiply(G1, x + field_modulus))

# The implication of the above is that: (x + y) mod curve_order == xG + yG
x = 2 ** 300 + 21
y = 3 ** 50 + 11

print(x + y)
# 2037035976334486086268445688409378161051468393665936250636140449355099197751028558772167657

# (x + y)G == xG + yG
assert eq(multiply(G1, (x + y)), add(multiply(G1, x), multiply(G1, y)))

# Even though the (x + y) operation will "overflow" the curve order, it does not matter. Just like in 
# a finite field, this behaviour is expected. The elliptic curve multiplication is implicitly executing
# the operation as taking the modulus before doing the multiplication.
# In fact, we don’t even need to do the modulus if we only care about positive numbers, the following 
# identity also holds:
# ((x + y) % curve_order)G == xG + yG
assert eq(multiply(G1, (x + y) % curve_order), add(multiply(G1, x), multiply(G1, y)))
# And by extension, it proves that: 
# ((x + y) % curve_order)G == (x + y)G
assert eq(multiply(G1, (x + y) % curve_order), multiply(G1, (x + y)))
#
# BUT, if we do the finite math modulo with the wrong number (some number other than the curve order), 
# the equality will break if we “overflow”:
x = 2 ** 300 + 21
y = 3 ** 50 + 11 # these values are large enough to overflow:
assert eq(multiply(G1, (x + y) % (curve_order - 1)), add(multiply(G1, x), multiply(G1, y)))
# This breaks.
