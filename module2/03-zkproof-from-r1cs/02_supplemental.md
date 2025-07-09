# Elliptic Curves Over Finite Fields

## The Field Modulus and Curve Order in Elliptic Curve Over Finite Fields
We saw in [Elliptic Curve Over Finite Fields](https://www.rareskills.io/post/elliptic-curves-finite-fields) that the field modulus ($p$) is not the same as the curve order ($n$).

That is:

$$
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
$$

While

$$
n = 21888242871839275222246405745257275088548364400416034343698204186575808495617
$$

In elliptic curve cryptography, these two moduli have specific roles to play and should not be confused.

### Field Modulus (or the Finite Field Modulus) $p$
When we define a curve over a finite field:

$$
y^2 = x^3 + ax + b \quad (\text{mod} \ p)
$$

All point coordinates (x, y) are elements of the finite field ($F_p$). This means that all arithmetic (add/subtract/multiply/divide) is done in $\text{mod} \ p$; that is, point adding, point doubling is all in $\text{mod} \ p$.

Using a finite field makes the discrete-log problem truly discrete, because over $F_p$, it is extremely difficult to make any approximation on the hidden scalars.

The field modulus also helps to set the bit-length of coordinates and of cryptographic keys, i.e. controlling the key length.

The field modulus "stores" scalars before they are applied to elliptic curve points, ensuring that they are valid in the field where the curve lives. Scalars are effectively field elements.

In some sense, the field modulus defines the finite field in which the elliptic curve points live and makes the arithmetic exact.

Used when preparing scalars (e.g., converting constraints to field elements).

### Curve Order $n$
The curve order of an elliptic curve over $F_p$, is the TOTAL NUMBER OF POINTS, including the point of infinity. These points usually form a cyclic abelian group. It is used for scalar multiplication.

In a way, it defines how many points are valid for cryptographic operations, by providing a large cyclic group for EC discrete-log problems thus making it extremely difficult.

In cryptography, we usually pick $G$ of (prime) order $n$.

The curve order defines the cyclic subgroup used for cryptography:

- $G$ has order $n$ (i.e. $nG = O$ which is the identity)

- Scalars (private keys) reduce $\text{mod} \ n$:
$$
kG = (k \ \text{mod} \ n)G
$$

A private key is an integer $d$ chosen uniformly from $[1, n - 1]$. And the corresponding public key is $Q = dG$.

The curve order ensures scalar multiplication stays within bounds.

Used when applying scalars to points (e.g., computing public keys).

## In an R1CS
Given that we have a system of equations in an R1CS.

- The field modulus $p$ converts integers to finite field elements.
    - The coefficients in an R1CS are mapped into the elliptic curve's finite field ($\text{mod} \ p$).
    - Effectively wrapping all arithmetic correctly in the field.
    - This generates SCALARS that can be used for elliptic curve operations.

- Scalar multiplication (in $\text{mod} \ n$) helps apply the constraints to witness values.
    - The scalars that represent the R1CS constraints multiply by EC points (in the witness) to enforce R1CS constraints and preserve relationships.


### Homomorphism
This is possible due to the additive homomorphism of elliptic curve scalar multiplication.

$$
[a]G + [b]G = [a + b]G
$$

Where $a[G]$ denotes scalar multiplication. The curve preserves the linear relationships.

Our R1CS is built from linear equations. The homomorphism from intergers to field elements to elliptic curve points preserves the linear relationships, allowing the verifier to check constraints without knowing the witness values.

|                        | Field Modulus ($p$)                          | Curve Order ($n$)                          |
|------------------------|----------------------------------------------|--------------------------------------------|
| **Purpose**            | Prepares scalars for EC operations.          | Governs cyclic subgroup for private keys.|
| **Homomorphism**       | Preserves linearity in scalar arithmetic.    | Preserves group structure in ec point operations.|