from py_ecc.bn128 import curve_order
# 21888242871839275222246405745257275088548364400416034343698204186575808495617
print(curve_order)

# The BN128 curve (a.k.a BN254) is used by the Ethereum precompiles to verify ZK proofs
# The equation is: y^2 = x^3 + 3 (mod p)
# [ p is an extremely large number ]

# IMPORTANT:
# Curve order = Number of points on the elliptic curve.
# Field modulus = The prime number defining the finite field (the modulo we do the curve over)
# [Curve order =/= Field modulus]


