from py_ecc.bn128 import G1, multiply, add

# *** Basic zero knowledge proofs with elliptic curves ***
# Example:
# Claim -> "I know two values x and y, such that x + y = 15".
# Proof -> I multiply x by G1, and y by G1, and give those to the verifier as A and B respectively.
# Verifier -> Multiply 15 by G1, and check that A + B == (15)G1.

# Prover
secret_x = 5
secret_y = 10

x = multiply(G1, secret_x)
y = multiply(G1, secret_y)

proof = (x, y, 15)

# Verifier
if add(proof[0], proof[1]) == multiply(G1, proof[2]):
    print("statement is true")
else:
    print("statement is false")

# The verifier would not know what x and y are, but they can verify that x and y add up to 15
# in elliptic curve space, thus `secret_x` and `secret_y` add up to 15 as finite field elements.
