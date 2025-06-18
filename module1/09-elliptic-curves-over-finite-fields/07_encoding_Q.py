from py_ecc.bn128 import G1, curve_order, field_modulus, G1, add, multiply, eq

# *** Encoding Rational Numbers ***
# Using regular integers in division always results in some precision loss
# For example, the following breaks:
# assert (5/2)G + (1/2)G == (3)G
assert eq(add(multiply(G1, 5 / 2), multiply(G1, 1 / 2)), multiply(G1, 3))

# Recall that in finite fields, we can compute rational numbers without rounding or approximating by using
# the multiplicative inverse. In a finite field, every non-zero element has a unique multiplicative inverse.
# I.e. (1/n) is simply the multiplicative inverse of n.
# Thus, (5/2) can be encoded as: 5 * mul_inv(2).
#
# In Python: pow(base, exponent, modulus)
five_over_two = (5 * pow(2, -1, curve_order)) % curve_order # (5/2) mod curve_order
one_half = pow(2, -1, curve_order) # (1/2) mod curve_order

# Essentially 5/2 = 2.5 and 2.5 + 0.5 = 3, but we are doing this in a finite field
# Now the assertion passes: (5/2)G + (1/2)G == (3)G
assert eq(add(multiply(G1, five_over_two), multiply(G1, one_half)), multiply(G1, 3))

