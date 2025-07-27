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

But for this example, we will pick a small prime number to make this manageable. We will use the prime number $79$ as the field modulus $\mathbb{F_{79}}$.

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
The next step is to convert all items ($\mathbf{L}$, $\mathbf{R}$, $\mathbf{O}$, $\mathbf{a}$) into field arrays. Doing modular arithmetic in Numpy is tricky but we can use the `galois` library to help us do so.

```python
import galois

p = 79
GF = galois.GF(79)
```

We cannot have operations such as: `GF(-1)` otherwise it will throw an exception. Thus when any of our items have a negative value, we have to **convert the negative number to its congruent representation in the finite field**.

To convert negative numbers to their congruent representation in the finite field, we can add the field modulus to them. And to avoid "overflowing" positive values, that is to ensure that our values stay within the valid range of the prime field $\mathbb{F_{p}}$ ($0$ to $p - 1$), we take the modulus with the field modulus.

Note that we have established that the **field modulus and curve order are equal** at this point. So when we say "add the field modulus" and "take the modulus with the field modulus", its the same as saying "add the curve order" and "take the modulus with the curve order".

```python
L = (L + 79) % 79
R = (R + 79) % 79
O = (O + 79) % 79
```

The new values in matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ in $\mod 79$ are thus:

```math
\begin{align*}

\mathbf{L} &=
\begin{bmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 74 & 0 & 0 & 0 \\
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
0 & 1 & 0 & 0 & 0 & 78 & 0 
\end{bmatrix}

\end{align*}
```

We can now (safely) convert the matrices into field arrays, simply by wrapping them with `GF`. We will also need to do the same for the witness $\mathbf{a}$ since it contains negative values.

```python
L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

x = GF(4)
y = GF((-2 + 79) % 79)
v1 = x * x
v2 = v1 * v1
v3 = GF((-5 + 79) % 79)*y * y
z = v3 * v1 + v2    # z = -5(y^2)(x^2) + x^4

witness = GF(np.array([1, z, x, y, v1, v2, v3]))

assert all(np.equal(
    np.matmul(L_galois, witness) * np.matmul(R_galois, witness),
    np.matmul(O_galois, witness)
)), "not equal"
```

## Polynomial Interpolation in Finite Fields
Next, we need to turn each of the columns of matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ into a list of (galois) Lagrange interpolating polynomials (in the finite field) that interpolate the columns. The points we interpolate are $x = [1, 2, 3, 4]$, since we have 4 rows (4 constraints in the R1CS).

Each matrix will yield 7 polynomials since there are 7 columns in the matrices.

Note that the $x$ values also need to be converted to field elements.

```python
def interpolate_column(col):
    xs = GF(np.array([1, 2, 3, 4]))
    return galois.lagrange_poly(xs, col)

# `np.apply_along_axis(func1d, axis, arr, ....)`
# `axis` = 0 means apply the function down the columns
# apply_along_axis is the same as doing a for loop over the columns and collecting the results in an array
U_polynomials = np.apply_along_axis(interpolate_column, 0, L_galois)
V_polynomials = np.apply_along_axis(interpolate_column, 0, R_galois)
W_polynomials = np.apply_along_axis(interpolate_column, 0, O_galois)

# U_polynomials = u1(x), u2(x), ... u7(x)
# V_polynomials = v1(x), v2(x), ... v7(x)
# W_polynomials = w1(x), w2(x), ... w7(x)
```

If we look at the contents of the matrices, we should expect the first 2 polynomials of `U_polynomials` and `V_polynomials` to be zero since those columns are zero vectors. Likewise, we should also expect the first polynomial of `W_polynomials` to be zero for the same reason.

```python
print(U_polynomials[:2])
print(V_polynomials[:2])
print(W_polynomials[:1])

# [Poly(0, GF(79)), Poly(0, GF(79))]
# [Poly(0, GF(79)), Poly(0, GF(79))]
# [Poly(0, GF(79))]
```

The term `Poly(0, GF(79))` is simply a polynomial where all coefficients are zero (a.k.a the zero polynomial or the zero vector polynomial).

The reader is encouraged to evaluate the polynomials in the R1CS at the $x$ values to see they interpolate the matrix values correctly

## Computing $h(x)$
Since the R1CS has 4 constraints, we know that:

```math
t(x) = (x - 1)(x - 2)(x - 3)(x - 4)
```
By way of reminder, the following is the formula for a QAP. The vector $\mathbf{a}$ is the witness:

```math
\underbrace{\sum_{i = 1}^{m}a_iu_i(x)}_{\text{term 1 }(\mathbf{La})} \underbrace{\sum_{i = 1}^{m}a_iv_i(x)}_{\text{term 2 }(\mathbf{Ra})} = \underbrace{\sum_{i = 1}^{m}a_iw_i(x)}_{\text{term 3 }(\mathbf{Oa})} + h(x)t(x)
```

Each of the terms is taking the inner product (dot product) of the witness with the column-interpolating polynomials. That is, each of the summation terms are effectively the inner product between 
$[a_1, ..., a_m]$ and $[u_1(x), ..., u_m(x)]$.

Which is essentially:

```math
a_1u_1(x) + a_2u_2(x) + ... + a_mu_m(x)
```

And each term evaluates into a polynomial itself. For example:

```math
\mathbf{La} \rightarrow \sum_{i = 1}^{m}a_iu_i(x) = a_1u_1(x) + ... + a_mu_m(x) = u(x)
```

```python
def inner_product_polynomials_with_witness(polys, witness):
    mul_ = lambda x, y: x * y
    sum_ = lambda x, y: x + y
    return reduce(sum_, map(mul_, polys, witness))

term_1 = inner_product_polynomials_with_witness(U_polynomials, witness)

term_2 = inner_product_polynomials_with_witness(V_polynomials, witness)

term_3 = inner_product_polynomials_with_witness(W_polynomials, witness)
```

Note that `mul_` is an anonymous function that multiplies two elements component-wise, and `sum_` is an anonymous function that adds two elements together. The final `reduce` statement basically computes the pairwise product of each element in `polys` and `witness`, and then aggregates the products into a single value.

To compute for $h(x)$, we simply solve for it. We cannot compute $h(x)$ unless we have a valid witness, otherwise there will be a remainder.

```math
h(x) = \frac{u(x)v(x) - w(x)}{t(x)}
```

```python
# t = (x - 1)(x - 2)(x - 3)(x - 4)

t = galois.Poly([1, 78], field = GF) *
    galois.Poly([1, 77], field = GF) *
    galois.Poly([1, 76], field = GF) * 
    galois.Poly([1, 75], field = GF)

# Floor division with `t`
h = (term_1 * term_2 - term_3) // t
```

Note that `Poly([1, 78])` translates to $1 \cdot x^1 + 78 \cdot x^0 = x + 78$. And in $\mathbb{F_{79}}$, $78 \equiv -1 \mod 79$. Thus `Poly([1, 78])` is $(x - 1)$.

Unlike [poly1d from numpy](https://numpy.org/doc/stable/reference/generated/numpy.poly1d.html), the `galois` library won't indicate if there is a remainder, so we need to check if the QAP formula still holds true:

```math
u(x)v(x) = w(x) + h(x)t(x)
```

```python
assert term_1 * term_2 == term_3 + h * t, "Division has a remainder"
```

The check above is very similar to what the verifier will check for.

The scheme above will NOT work when we evaluate the polynomials on a **hidden point** from a trusted setup. However, the computer doing the trusted setup will still have to execute many of the computations above.

In this example, the QAP is simplified and polynomials are evaluated at a public point. This would not be secure because a malicious prover can forge proofs by crafting polynomials that satisfy the QAP formula only at the public point but not universally. Having a hidden point forces the prover to honestly evaluate the polynomials everywhere.

<hr>

A hidden point is referring to a secret value (secret scalar) used to generate structured reference strings, which contains encrypted evaluations of the public point. For instance if $s$ is the public point, then an encrypted valuation of $s$ would be $g^s$ where $g$ is a generator from a cyclic finite abelian elliptic curve group. The eventual idea is such that instead of checking:

```math
A(s) \bullet B(s) = C(s) \bullet G_2
```

The verifier uses pairing-friendly elliptic curves to validate:

```math
e(g_{1}^{\ A(s)}, g_{2}^{\ B(s)}) = e(g_{1}^{\ C(s)}, g_2) \cdot e(g_{1}^{\ h(s)}, g_2^{t(s)})
```

Which can be represented as:

```math
[A(s)]_1 \bullet [B(s)]_2 = [C(s)]_1 \bullet [1]_2 + [h(s)]_1 \bullet [t(s)]_2
```

And, if $h(s)t(s)$ is absorbed into $C(s)$, is simpliefied and reduced to:

```math
[A]_1 \bullet [B]_2 = [C]_1 \bullet [1]_2
```

**More of this in the next 2 chapters.**

<hr>