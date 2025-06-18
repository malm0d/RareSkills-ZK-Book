from py_ecc.bn128 import G1, field_modulus, curve_order, multiply, add

# Can you prove you know x such that 23x = 161 ?

# Prover
secret_x = 7

commitment_x = multiply(G1, secret_x)

# Verifier
# Prove that (23)xG = 161G
proof = (commitment_x, 23, 161)
if multiply(proof[0], proof[1]) == multiply(G1, proof[2]):
    print("statement is true")
else:
    print("statement is false")

# *** Security Assumptions ***
# For the above scheme to be secure, it is assumed that if we publish a point such as `multiply(G1, x)`,
# an attacker cannot infer from the (x, y) value created what the original value for `x` was. This is the
# discrete logarithm assumption. And this is why the prime number we compute the formula over needs to be
# large so that an attacker cannot guess by brute force.
# That is, given C = x * G
# We turn our secret x into an elliptic curve point by adding G to itself x times.
# Given only G and C, an attacker needs to figure out what x is - this is the discrete logarithm problem.
# For general elliptic curve groups, the fastest public algorithm (pollard-p, etc) still needs about r^(1/2)
# group operations, where r is the group order (2^254). This much work is infeasible for any hardware.
# There is no known trick that uses any (xG, yG) of the point to figure out the scalar, that is (xG, yG) 
# only tell you that this is a point on the elliptic curve. If r had small factors, the attacker could break
# the problem in each small subgroup and recombine the answers (Pohlig–Hellman). Making r prime blocks that 
# shortcut.
# I.e. if r was only 100 (a non-prime i.e. composite), then 100 = 4 * 25, someone can solve the 4 part 
# and then the 25 part separately and then combine the answer.
# Thus it is important that r is prime so it blocks this.
#
# There are mores sophisticated algorithms, like the baby step giant step algorithm that can outperform brute force.
# Note: The BN128 comes from the assumption that it has 128 bits of security. The elliptic curve is computed in a
# finite field of 254 bits, but it is believed to have 128 bits of security since there are better algorithms than
# naive brute force to compute the discrete logarithm. When we say 128 bits of security, it means that the best
# known attack needs about 2^128 elementary group operations

# *** True Zero Knowledge ***
# The esxample A + B = 15G is not truly ZK. If an attacker guesses A and B, they can verify thier guess by comparing
# the generated elliptic curve point to the one we have. The solution to this will be addressed in another chapter.

# *** Treating elliptic curves over finite fields as a magic black box ***
# Just like how we dont need to know how a hash function works under the hood to use it, we dont need to know the
# implementation details of adding elliptic curve points and multiplying them with a scalar.
# However, we do need to know the rules that they follow, i.e. the rules of cyclic groups:
# -> Adding elliptic curve points is closed: it produces another elliptic curve point
# -> Adding elliptic curve points is associative
# -> There exists an identity element: the point of infinity
# -> Each element has an inverse (additive inverse) that when added, produces the identity element
#
# As long as you understand this, you can add, multiply, and invert to your heart’s content without doing anything 
# invalid. Each of these operations has a corresponding function in the py_ecc library.
#
# This is most important thing to remember for this lesson:
# Elliptic curves over finite fields (the group) HOMOMORPHICALLY encrypt addition in a finite field.