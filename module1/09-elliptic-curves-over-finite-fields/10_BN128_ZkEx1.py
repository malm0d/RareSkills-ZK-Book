from py_ecc.bn128 import G1, curve_order, multiply, add

# As a (very important) hint, multiplying a number by a constant is the same thing as repeated addition.
# Repeated addition is the same thing as elliptic curve scalar multiplication. Thus, if x is an elliptic
# curve point, we can multiply it by a scalar 9 as multiply(x, 9). This is consistent with our statement
# that we cannot multiply elliptic curve points – we are actually multiplying an elliptic curve point by
# a scalar, not another point.

# It is an exercise for the reader to do something more sophisticated, like prove knowledge of a solution
# to a linear system of equations.

# Note that in the py_ecc library, any scalar passed to multiply() is taken "mod curve_order" because
# curve_order * G1 = O (point at infinity). Thus to represent any: -n mod curve_order, we take
# curve_order - n (when 0 < n < curve_order).

# Prove knowledge of the following linear system of equations with 2 unknowns:
# 7x + 4y = 75
# 2x - 1y = 0

# Prover
secret_x = 5
secret_y = 10

commitment_x = multiply(G1, secret_x) # xG
commitment_y = multiply(G1, secret_y) # yG

# Verifier
# The verifier essentially needs to prove: 3xG + 4yG = 75G and 2xG - yG = 0G
equation1 = add(multiply(commitment_x, 7), multiply(commitment_y, 4))
equation2 = add(multiply(commitment_x, 2), multiply(commitment_y, curve_order - 1))
if equation1 == multiply(G1, 75) and equation2 == multiply(G1, 0):
    print("statements are true")
else:
    print("statements are false")

# FYI, multiply(G1, 0) yields the indentity (point of infinity).
# Since multiply(G1, k) means add G1 to itself k times, multiply(G1, 1) just means G1, and thus
# if with multiply(G1, 0), it just means we are not adding anything, which leaves us at the identity.

# The homomorphism: phi(a) + phi(b) = phi(a + b) is translated to (a)G + (b)G = (a + b)G
# Take any whole number (mod r), turn it into an elliptic-curve point by multiplying it with the generator G,
# adding numbers first or mapping them first and then adding the points, gives the same result.”