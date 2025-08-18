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

The terms $[A]_1$ and $[C]_1$ represent polynomial commitments in $\mathbb{G_1}$, and $[B]_2$ represent a polynomial commitment in $\mathbb{G_2}$. A polynomial commitment simply means that the polynomial has been evaluated at the secret scalar value $\tau$ via the SRS, and the result is hidden in the exponent of a generator and encoded as an elliptic curve point.

The details of the above computations (of polynomial commitments) are discussed in [QAP over elliptic curves](https://rareskills.io/post/elliptic-curve-qap).

If the witness $\mathbf{a}$ is correct, it satisfies the QAP and the following equation will hold true:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [C]_1 \bullet G_2
```

## Motivation
From the previous chapter, we left off saying that a prover simply presenting: $([A]_1, [B]_2, [C]_2)$ is not a convincing enough argument to assume that the prover knows a witness $\mathbf{a}$ such that the QAP is balanced.

The prover is always assumed to be malicious.

The prover can simply invent the scalars: $a$, $b$, $c$, where $ab = c$, compute:

```math
[A]_1 = aG_1 \\
[B]_2 = bG_2 \\
[C]_1 = cG_1
```

and present them as elliptic curve points to the verifier.

The verifier will have no idea if $([A]_1, [B]_2, [C]_2)$ were the result of a satisified QAP or not.

We need to force the prover to be honest without introducing too much computational overhead. The first algorithm to accomplish this was ["Pinocchio: Nearly Practical Verifiable Computation"](https://eprint.iacr.org/2013/279.pdf). This was usable enough for ZCash to base the first version of their blockchain on it.

However, Groth16 was able to accomplish the same thing with much fewer steps, and the algorithm is still widely used today as no other algorithm since has produced as efficient an algorithm for the verification step (though other algorithms have eliminated the trusted setup or significantly reduced the amount of work for the prover).

Update for 2024: A paper rather triumphantly titled [“Polymath: Groth16 is not the limit”](https://eprint.iacr.org/2024/916) published in Cryptology demonstrates an algorithm that requires fewer verifier steps than Groth16. However, there are no known implementations of the algorithm at this time of writing.

## Preventing Forgery Part 1: Intoducing $\alpha$ and $\beta$
### An "Unsolvable" Verification Formula

Suppose we update our verification formula from:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [C]_2 \bullet G_2
```

to the following:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [D]_{1 \ 2} + [C]_1 \bullet G_2
```

**Note that the above is using additive notation for the $\mathbb{G_{1 \ 2}}$ group for convenience.**

Here, $[D]_{1 \ 2}$ is an element from $\mathbb{G_{1 \ 2}}$ and has an **unknown** discrete logarithm.

We now show that it is impossible for a verifier to provide a solution $([A]_1, [B]_2, [C]_1)$ to this equation without knowing the discrete logarithm of $[D]_{1 \ 2}$.

<hr>

#### Side Quest: Why Additive Notation over Multiplicative Notation

In the context of bilinear pairings, the target group $\mathbb{G_{1 \ 2}}$ is usually written multiplicatively.

In pairings, we have:

```math
e: G_1 \times G_2 \rightarrow G_{1 \ 2}
```

The pairing property is:

```math
e(aG_1, bG_2) = e(G_1, G_2)^{ab}
```

And the group law in $\mathbb{G_{1 \ 2}}$ is multiplication. (Remember that the LHS reflects additive group operations - scalar mulitplies of EC points), and the RHS reflects an element of a group where exponentiation makes sense i.e. a multiplicative group.

Switiching to additive notation is simply for convenience in writing the verification equation. Instead of $X \cdot Y$ meaning group multiplciation in $\mathbb{G_{1 \ 2}}$, we write $X + Y$ to mean the group operation. That is, $+$ is now the group law.

It is sensible to do this because the rest of the equation involves $\mathbb{G_1}$ and $\mathbb{G_2}$ elements in additive notation.

The updated verification equation that we have above would normally be written in multiplicative notation as:

```math
e([A]_1, [B]_2) \stackrel{?}{=} [D]_{1 \ 2} \cdot e([C]_1, G_2)
```

Observe that the "$+$" (group addition) in the original equation in additive notation is replaced with "$\cdot$" (group multiplication) in the multiplicatibe notation for $G_{1 \ 2}$. Scalars still multiply points in their respective groups: $[C]_1 \bullet G_2$ still means pairing $[C]_1$ with $G_2$.

Remember that elliptic curve math is always additive:

```math
P + Q, \quad a \cdot P
```

Staying with the additive notation keeps things consistent - we dont want the verification equation to be mixed with addition and multiplication symbols. Additionally, all groups: $G_1$, $G_2$, and $G_{1 \ 2}$ are abelian, and having just "$+$" just means the group law for whatever group they are in.

Most importantly, there is no loss of correctness. The math is identical - we can pick additive or multiplicative notation for any abelian group, including $G_{1 \ 2}$. If we write the group's binary operator as "$+$", then the identity is $0$, and inverses are $-x$; if we write the group's binary operator as "$\cdot$, then the identiy is $1$, and the inverses are $x^{-1}$. No matter which of the two binary operators we select, the underlying algebraic structure remains the same.

Normally, the convention is: elliptic curve groups $\rightarrow$ additive, and field multiplicative subgroup $\rightarrow$ multiplicative. Here, we align with $G_1$ and $G_2$ elliptic curve groups simply for readability, thus the additive notation.

<hr>

## Attack 1: Forging $[A]_1$ and $[B]_2$, and Attempting to Derive $[C]_1$

Suppose that a malicious prover randomly selects the scalars: $a'$ and $b'$, and produces the elliptic curve points: $[A]_1$ and $[B]_2$. The malicious prover then attempts to derive (forge) a $[C']_1$ that is compatible with the verifier's formula (i.e. makes the equation true). If the prover knew the discrete logs for $[A]_1$ and $[B]_2$ with respect to the know generators $G_1$ and $G_2$, then they could explicitly compute $[A]_1 \bullet [B]_2$.

Starting from:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [D]_{1 \ 2} + [C']_1 \bullet G_2
```

Subtract $[D]_{1 \ 2}$ from both sides (remember that "subtract" means inverse/addition in $\mathbb{G_{1 \ 2}}$)

```math
\begin{align*}
[A]_1 \bullet [B]_2 - [D]_{1 \ 2} &\stackrel{?}{=} [C']_1 \bullet G_2 \quad \text{(additive notation)}  \\[4pt]
e([A]_1, [B]_2) \cdot [D]_{1 \ 2}^{\ -1} &\stackrel{?}{=} e([C]_1, G_2) \quad \text{(multiplicative notation)}
\end{align*}
```

The LHS could be called: $[\chi]_{1 \ 2} = [A]_1 \bullet [B]_2 - [D]_{1 \ 2}$, and the above rewritten as:

```math
[\chi]_{1 \ 2} \stackrel{?}{=} [C']_1 \bullet G_2
```

To solve for $[C']_1$, a malicious prover could try to find the discrete logarithm of $\chi_{1 \ 2}$. But we know that this is not computationally feasible.

The malicious prover, assuming if they knew what $[\chi]_{1 \ 2}$ is, could also atttempt to solve for $[C']_1$ by finding the scalar $C'$ that satisfies the above. But this is the same as attempting to solve the discrete logarithm problem which is, again, computationally infeasible.

## Attack 2: Forging $[C]_1$, and Attempting to Derive $[A]_1$ and $[B]_2$ (A Bilinear Diffie-Hellman Problem)


