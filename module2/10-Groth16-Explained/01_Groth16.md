# Groth16 Explained
https://rareskills.io/post/groth16

The Groth16 algorithm enables a quadratic arithmetic program (QAP) to be computed by a prover over elliptic curve points derived in a trusted setup, and to be quickly checked by a verifier. It uses auxiliary elliptic curve points from the trusted setup to prevent forged proofs.

## Prerequisites
It assumes familiarity with all chapters discussed up to this point.

## Notation and Preliminaries
An [elliptic curve point](https://rareskills.io/post/elliptic-curves-finite-fields) belonging to the group $\mathbb{G_1}$ is referred to as: $[x]_1$. And an elliptic curve point belonging to the group $\mathbb{G_2}$ is referred to as: $[x]_2$.

An [elliptic curve bilinear pairing](https://rareskills.io/post/bilinear-pairing) between two elliptic curve points $[x]_1$ and $[x]_2$ is denoted as $[x]_1 \bullet [x]_2$ (which is the same as: $e([x]_1, [x]_2)$). 

A pairing produces an element in $\mathbb{G_{1 \ 2}}$ (in some places $\mathbb{G_{1 \ 2}}$ may be referred to as $\mathbb{G_T}$).

Vectors are denoted in lower case bold letters such as: $\mathbf{a}$.

Matrices are denoted in upper case bold letters such as: $\mathbf{L}$.

Field elements (informally referred to as scalars) are denoted in lower case letters such as: $d$, $n$, $m$, $l$, etc.

All arithmetic operations are occuring in a [finite field](https://rareskills.io/post/finite-fields), with a characteristic that equals to the order of the elliptic curve group. In other words, the field modulus in $\mathbb{F_p}$ is equal to the curve order in $\mathbb{F_q}$, i.e. $p = q$.

Given an [arithmetic circuit (ZK circuit)](https://rareskills.io/post/arithmetic-circuit), we convert it to a [Rank 1 Constraint System](https://rareskills.io/post/rank-1-constraint-system) in the form: $\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}$, where each matrix: $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$, have the same dimension: $n$ rows and $m$ columns, and the witness vector is $\mathbf{a}$. The number of constraints in the R1CS can also be thought of as $n$ as they are essentially the same.

Then we convert the R1CS into a [QAP](https://rareskills.io/post/quadratic-arithmetic-program) by interpolating the columns of the matrices by [Langrange interpolation](https://rareskills.io/post/python-lagrange-interpolation), where each column (column vector) of a matrix is taken as $y$ values, and they are interpolated over the $x$ values: $x = [1, 2, ..., n]$. Since $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ have $m$ columns, we end up with three sets of $m$ Lagrange interpolating polynomials where each polynomial has degree $\le n - 1$:

```math
\begin{array}{}
u_1(x), u_2(x), \dots, u_m(x) & \text{ m polynomials interpolated from the $m$ columns of $\mathbf{L}$ } \\
v_1(x), v_2(x), \dots, v_m(x) & \text{ m polynomials interpolated from the $m$ columns of $\mathbf{R}$ } \\
w_1(x), w_2(x), \dots, w_m(x) & \text{ m polynomials interpolated from the $m$ columns of $\mathbf{O}$ } \\
\end{array}
```

From this, we construct a balanced QAP with the formula:

```math
\sum_{i = 1}^{m}a_iu_i(x) \sum_{i = 1}^{m}a_iv_i(x) = \sum_{i = 1}^{m}a_iw_i(x) + h(x)t(x)
```

where $t(x)$, since we are interpolating over $x = [1, 2, ..., n]$, is defined as:

```math
t(x) = (x - 1)(x - 2)...(x - n)
```

and $h(x)$ by definition is:

```math
h(x) = \frac{\sum_{i = 1}^{m}a_iu_i(x) \sum_{i = 1}^{m}a_iv_i(x) - \sum_{i = 1}^{m}a_iw_i(x)}{t(x)}
```

If a third party creates a structured reference string (SRS) via a powers of tau ceremony (referred to as a [trusted setup](https://rareskills.io/post/trusted-setup)), then the prover can use the SRS to evaluate the sum terms in the QAP (generically: $\sum a_if_i(x)$) at the hidden point $\tau$ without knowing $\tau$ itself. Let the SRS be computed as follows:

```math
\begin{align*}
[\Omega_{n-1}, \Omega_{n-2}, \dots, \Omega_{2}, \Omega_{1}, G_1] &= [\tau^{n-1}G_1, \tau^{n-2}G_1, \dots, \tau^2G_1, \tau G_1, G_1] && \text{srs for $\mathbb{G_1}$} \\
[\Theta_{n-1}, \Theta_{n-2}, \dots, \Theta_{2}, \Theta_{1}, G_1] &= [\tau^{n-1}G_2, \tau^{n-2}G_2, \dots, \tau^2G_2, \tau G_2, G_2] && \text{srs for $\mathbb{G_2}$} \\
[\Upsilon_{n-2}, \Upsilon_{n-3}, \dots, \Upsilon_{1}, \Upsilon_{0}] &= [\tau^{n-2}t(\tau)G_1, \tau^{n-3}t(\tau)G_1, \dots, \tau t(\tau)G_1, t(\tau)G_1] && \text{srs for $h(x)t(x)$ in $\mathbb{G_1}$} \\
\end{align*}
```

Each SRS for $\mathbb{G_1}$ and $\mathbb{G_2}$ begins with the term for the polynomial term of degree $n - 1$, over $n$ terms. While the SRS for $h(x)t(x)$ begins with the term for the polynomial term of degree $n - 2$, over $n - 1$ terms. This allows the [QAP to be evaluated correctly on a trusted setup](https://rareskills.io/post/elliptic-curve-qap).

we refer to $f(\tau)$ as an arbitrary polynomial evaluated on a SRS via the inner product (note the witness $\mathbf{a}$ is not included here):

```math
\begin{align*}
f(\tau) &= \sum_{i = 1}^{m}f_i\Omega_i = \langle[f_d, f_{d-1}, \dots, f_{1}, f_{0}], [\Omega_d, \Omega_{d-1}, \dots, \Omega_{1}, G_1]\rangle \\[12pt]
f(\tau) &= \sum_{i = 1}^{m}f_1\Theta_i = \langle[f_d, f_{d-1}, \dots, f_{1}, f_{0}], [\Theta_d, \Theta_{d-1}, \dots, \Theta_{1}, G_2]\rangle
\end{align*}
```

Where $d$ is the degree of the polynomial, and $[f_d, f_{d-1}, \dots, f_{1}, f_{0}]$ are the coefficients of the polynomial.

The term $f(\tau)$ is shorthand for the above inner product expression, which produces an elliptic curve point. It does not mean that the prover knows what the value of $\tau$ is, since $\tau$ would have been discarded by the end of the trusted setup.

The prover can thus evaluate their QAP on the trusted setup by the following:

```math
\begin{align*}
[A]_1 &= \sum_{i = 1}^{m}a_iu_i(\tau) \\[10pt]
[B]_2 &= \sum_{i = 1}^{m}a_iv_i(\tau) \\[10pt]
[C]_1 &= \sum_{i = 1}^{m}a_iw_i(\tau) \\[10pt]
\end{align*}
```

The terms $[A]_1$ and $[C]_1$ represent polynomial commitments in $\mathbb{G_1}$, and $[B]_2$ represent a polynomial commitment in $\mathbb{G_2}$. A polynomial commitment simply means that the polynomial has been evaluated 