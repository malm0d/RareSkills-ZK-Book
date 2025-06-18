from libnum import has_sqrtmod_prime_power, sqrtmod_prime_power

# For modular square roots, the overarching idea is: x^2 = a (mod p)
# I.e. is there a field element that, when it squares itself, is congruent to another field element.
# If the above is true, then that field element is one of the solutions to the square root.

# the functions take arguments# has_sqrtmod_prime_power(n, field_mod, k), where n**k,
# but we aren't interested in powers in modular fields, so we set k = 1
# check if sqrt(8) mod 11 exists
print(has_sqrtmod_prime_power(8, 11, 1))
# False
# Because there is no field element in mod 11 where if we take the sqaure of it, yields 8

# check if sqrt(5) mod 11 exists
print(has_sqrtmod_prime_power(5, 11, 1))
# True
# Because there are field elements where, if we square them in mod 11, they yield 5

# compute sqrt(5) mod 11
print(list(sqrtmod_prime_power(5, 11, 1)))
# [4, 7]

assert (4 ** 2) % 11 == 5
assert (7 ** 2) % 11 == 5

# we expect 4 and 7 to be inverses of each other, because in "regular" math, the two solutions to a square root are sqrt and -sqrt
# This is also saying that these two are additive inverses of one another.
# [=> 4 behaves like -7, and 7 behaves like -4]
assert (4 + 7) % 11 == 0

