# R1CS to QAP Over a Finite Field in Python
https://rareskills.io/post/r1cs-to-qap

Say, we are encoding the [arithmetic circuit](https://rareskills.io/post/arithmetic-circuit):

```math
z = x^4 - 5y^2x^2
```

Converted to a [Rank 1 Constraint System](https://rareskills.io/post/rank-1-constraint-system), it becomes:

```math
\begin{align*}
v_1 &= x * x \\
v_2 &= v_1 * v_1 \quad \quad // \ x^4 \\
v_3 &= -5y*y \\
z - v_2 &= v_3 * v_1 \quad \quad // \ -5y^2x^2
\end{align*}
```

We need to pick a [finite field](https://rareskills.io/post/finite-fields) (where the field modulus is a prime, i.e. a prime field) in which all arithmetic will take place. When we later combine this with [elliptic curves](https://rareskills.io/post/elliptic-curves-finite-fields), **the order of the prime field MUST be equals to the order of the elliptic curve (the field modulus and curve order must be equal)**.

<hr>

This is a critical alignment required when integrating arithmetic circuits (expressed as R1CS/QAP) with elliptic curve cryptography, particularly in zk-SNARKs.

The constraints in the R1CS are defined over a finite field $\mathbb{F_p}$, where $p$ is a prime number. That is, in the R1CS/QAP, all arithmetic is performed $\mod p$.

In zk-SNARKs, the proof is often embedded into an elliptic curve group, e.g. BN254. This group has a curve order (number of points on the curve), which is another prime number $q$. In other words, the elliptic curve is defined over a finite field $\mathbb{F_q}$. That means all elliptic curve operations (point addition and point multiplication) are performed $\mod q$. 

(As a reminder, the elliptic curve itself is NOT a finite field, but its point operations rely on the underlying finite field).

The R1CS, and by extension the QAP's, polynomial evaluations and proofs are carried out in $\mathbb{F_p}$, but all elliptic curve operations are carried out in $\mathbb{F_q}$. Thus for these two to be compatible, the field modulus of the R1CS/QAP must equal the elliptic curve's group order:

```math
p = q
```

Consider the simple circuit defined over $\mathbb{F_5}$:

```math
z = x^2 \mod 5
```

Assume that we use an elliptic curve group with order $q = 7$.

When a prover picks $x = 2$, the prover computes: $z = 4 \mod 5$. And the prover tries to embed $z = 4$ into the elliptic curve's $\mathbb{F_7}$ field. The verifier expects $z$ to be in $\mathbb{F_7}$ but the prover's $z$ is ambiguous since it is computed in $\mathbb{F_5}$. 

If the verifier is expecting $z = 4 \mod 7$, and it accepts the prover's $z$, it would be assuming that $z = 4 \mod 7$ (which is a false positive). Because if the prover had used another representation (e.g. $z = 9 \equiv 4 \mod 5$), the verifier would have seen this as $z = 9 \equiv 2 \mod 7$ and rejected the proof.

This ultimately makes the verification fail or becomes insecure due to field mismatch $p \neq q$.

<hr>

Not matching the two moduli is a very common mistake.

But for this example, we will pick a small prime number to make this manageable. We will use the prime number $79$ as the field modulus.

Given the R1CS, we need to convert it to the form:

```math
\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}
```

First, we define our witness $\mathbf{a}$ based on the terms present in the R1CS:

```math
\mathbf{a} = 
\begin{bmatrix}
1 & z & x & y & v_1 & v_2 & v_3
\end{bmatrix}
```

Next, we define our matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ to represent the coefficients in the R1CS as follows. Remember that each column corresponds to a term in the witness $\mathbf{a}$.

```math
\begin{align*}

\mathbf{L} &=
\begin{bmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & -5 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1
\end{bmatrix}
\\

\mathbf{R} &=
\begin{bmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 
\end{bmatrix}
\\

\mathbf{O} &=
\begin{bmatrix}
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 \\
0 & 1 & 0 & 0 & 0 & -1 & 0 
\end{bmatrix}

\end{align*}
```

In Python:

```python
import numpy as np

# a = [1, z, x, y, v1, v2, v3]
L = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, -5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
])

R = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
])

O = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, -1, 0],
])
```

To verify that we constructed the R1CS correctly (its very easy to mess up when doing manually) we create a valid witness and do the matrix multiplication. The matrix multiplication here is standard matrix multiplication.

```python
x = 4
y = -2
v1 = x * x
v2 = v1 * v1
v3 = -5*y * y
z = v3 * v1 + v2    # z = -5(y^2)(x^2) + x^4

a = np.array([1, z, x, y, v1, v2, v3])

assert all(np.equal(
    np.matmul(L, a) * np.matmul(R, a),
    np.matmul(O, a)
    )), "not equal"
```

## Finite Field Arithmetic in Python
