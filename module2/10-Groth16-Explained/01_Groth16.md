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
u_1(x), u_2(x), \dots, u_m(x) & \text{ m polynomials interpolated from the } m \text{ columns of } \mathbf{L} \\
v_1(x), v_2(x), \dots, v_m(x) & \text{ m polynomials interpolated from the } m \text{ columns of } \mathbf{R} \\
w_1(x), w_2(x), \dots, w_m(x) & \text{ m polynomials interpolated from the } m \text{ columns of } \mathbf{O} \\
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
[\Omega_{n-1}, \Omega_{n-2}, \dots, \Omega_{2}, \Omega_{1}, G_1] &= [\tau^{n-1}G_1, \tau^{n-2}G_1, \dots, \tau^2G_1, \tau G_1, G_1] && \text{srs for } \mathbb{G_1} \\
[\Theta_{n-1}, \Theta_{n-2}, \dots, \Theta_{2}, \Theta_{1}, G_1] &= [\tau^{n-1}G_2, \tau^{n-2}G_2, \dots, \tau^2G_2, \tau G_2, G_2] && \text{srs for } \mathbb{G_2} \\
[\Upsilon_{n-2}, \Upsilon_{n-3}, \dots, \Upsilon_{1}, \Upsilon_{0}] &= [\tau^{n-2}t(\tau)G_1, \tau^{n-3}t(\tau)G_1, \dots, \tau t(\tau)G_1, t(\tau)G_1] && \text{srs for } h(x)t(x) \text{ in } \mathbb{G_1} \\
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

## Part 1: Preventing Forgery - Intoducing $\alpha$ and $\beta$
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

### Attack 1: Forging $[A]_1$ and $[B]_2$, and Attempting to Derive $[C]_1$

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

### Attack 2: Forging $[C]_1$, and Attempting to Derive $[A]_1$ and $[B]_2$ (A Bilinear Diffie-Hellman Problem)

Suppose that a malicious prover randomly selects the scalar $c'$ and produces the elliiptic curve point $[C]_1$. This means that the malicious prover could explicitly compute $[C]_1 \bullet G_2$.

Since the prover already knows $c'$, they could attempt to find the scalars: $a'$ and $b'$ such that:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} \underbrace{[D]_{1 \ 2} + [C]_1 \bullet G_2}_{[\zeta]_{1 \ 2}}
\\[4pt]
[A]_1 \bullet [B]_2 \stackrel{?}{=} [\zeta]_{1 \ 2}
```

This requires the prover, given $[\zeta]_{1 \ 2}$, to come up with an $[A]_1$ and $[B]_2$ that produces $[\zeta]_{1 \ 2}$ in a bilinear pairing. That is, the prover has to figure out what the scalars $a'$ and $b'$ are.

Similar to the discrete logarith problem, we rely on unproven cyptographic assumptions that this computation: decomposing (breaking down) an element in $\mathbb{G_{1 \ 2}}$ into its respective $\mathbb{G_1}$ and $\mathbb{G_2}$ elements, is computationally infeasible.

In this case, the assumption that we cannot decompose $[\zeta]_{1 \ 2}$ into $[A]_1$ and $[B]_2$ is called the *Bilinear Diffie-Hellman Assumption*. You may optionally read up on the [Decisional Diffie-Hellman Assumption](https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption).

In practice, there is no known way to decompose $[\zeta]_{1 \ 2}$ into $[A]_1$ and $[B]_2$, and it is believed to be computationally infeasible.

<hr>

#### Side Quest: Exploring BDH and DDH

The Bilinear Diffie-Hellman (BDH) Assumption states that given the elliptic curve generators $P \in \mathbb{G_1}, Q \in \mathbb{G_2}$, and the scalars: $a, b, c$ which are **hidden** from you, it is computationally hard to compute: $e(P, Q)^{abc} \in \mathbb{G_{1 \ 2}}$. 

Formally, given the inputs: $P, aP, bP \in \mathbb{G_1}, Q, cQ \in \mathbb{G_2}$. And given the output: $e(P, Q)^{abc} \in \mathbb{G_{1 \ 2}}$. No efficient algorithm can solve this with non-negligible probability. There is no feasible way of knowing the scalars $a, b, c$ such that we can combine the exponents in the bilinear pairing to get the output - all we have are just elliptic curve points.

Finding the inverse of this pairing $e(P, Q)^{abc}$ would mean finding the hidden scalars, but this is essentially the discrete logarithm problem on elliptic curves.

In the same way, the Decisional Diffie-Hellman (DDH) Assumption also relies on the hardness of the discrete logarithm problem.

Consider a multiplicative cyclic group $\mathbb{G}$ with the order $q$ and the generator $g$. The DDH assumption states that given $g^a$ and $g^b$ for $a, b, \in \mathbb{Z_q}$, then it is hard to decide if $ab = a \times b$ because $g^{ab}$ looks like any other element in  $\mathbb{G}$.

Another way to look at this, if we have $(g^a, g^b, \mathbb{z})$ in $\mathbb{G}$, its hard to decide if $\mathbb{z} = g^{ab}$. This is a decisional problem, not a computational problem where we have to compute $g^{ab}$, we are just being asked if $\mathbb{z}$ is equal to $g^{ab}$ or not. If breaking the discrete logarithm is easy, then we could compute: $a = \log_{g}(g^a)$, and once we have $a$, we can then compute: $(g^b)^a = g^{ab}$. And we can then compare this with $\mathbb{z}$ to answer if $z = g^{ab}$.

We know that breaking the discrete logarithm problem is infeasible and therefore DDH assumes that $g^a$, $g^b$ and $g^{ab}$ are computationally indistinguishable.

<hr>

### Scalars $\alpha$ and $\beta$: How they are used in Groth16

So far, we have the verification equation:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [D]_{1 \ 2} + [C]_1 \bullet G_2
```

In practice, Groth16 doesn't use the term $[D]_{1 \ 2}$. Instead, the trusted setup generates two random scalars: $\alpha$ and $\beta$, and publishes in the structured reference string (SRS) the elliptic curve points: $[\alpha]_1$ and $[\beta]_2$ - which are computed as:

```math
\begin{align*}
[\alpha]_1 &= \alpha G_1 \\
[\beta]_2 &= \beta G_2
\end{align*}
```

What we refer to as $[D]_{1 \ 2}$ is simply the pairing: $[\alpha]_1 \bullet [\beta]_2$. And our updated verification formula is:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + [C]_1 \bullet G_2
```

### Re-deriving the Proving and Verification Formulas

To make the now updated verification formula "solvable", the QAP formula must be updated to incorporate $\alpha$ and $\beta$. That is, since we added $[\alpha]_1 \bullet [\beta]_2$ to the RHS of the equation, we need to balance it by adding $[\alpha]_1$ and $[\beta]_2$ to the LHS of the equation.

The original QAP formula is:

```math
\sum_{i = 1}^{m}a_iu_i(x) \sum_{i = 1}^{m}a_iv_i(x) = \sum_{i = 1}^{m}a_iw_i(x) + h(x)t(x)
```

Consider what happens if we add $\theta$ and $\eta$ to the sum terms on the LHS of the equation respectively:

```math
(\boxed{\theta} + \sum_{i=1}^{m}a_iu_i(x)) (\boxed{\eta} + \sum_{i=1}^{m}a_iv_i(x))
```

When we expand the above, we get:

```math
\boxed{\theta\eta} + \boxed{\theta}\sum_{i=1}^{m}a_iv_i(x) + \boxed{\eta}\sum_{i=1}^{m}a_iu_i(x) + \sum_{i=1}^{m}a_iu_i(x)\sum_{i=1}^{m}a_iv_i(x)
```

Notice that the rightmost term is essentially the original QAP expression. We can substitute that term using the QAP definition:

```math
\begin{align*}
\theta\eta + \theta\sum_{i=1}^{m}a_iv_i(x) + \eta\sum_{i=1}^{m}a_iu_i(x) \ + \ &\boxed{\sum_{i=1}^{m}a_iu_i(x)\sum_{i=1}^{m}a_iv_i(x)}
\\
&\text{becomes}
\\
\theta\eta + \theta\sum_{i=1}^{m}a_iv_i(x) + \eta\sum_{i=1}^{m}a_iu_i(x) \ + \ &\boxed{\sum_{i=1}^{m}a_iw_i(x) + h(x)t(x)} 
\end{align*}
```

Now, we get an "expanded" QAP with the following definition:

```math
(\theta + \sum_{i=1}^{m}a_iu_i(x))(\eta + \sum_{i=1}^{m}a_iv_i(x)) = \theta\eta + \theta\sum_{i=1}^{m}a_iv_i(x) + \eta\sum_{i=1}^{m}a_iu_i(x) + \sum_{i=1}^{m}a_iw_i(x) + h(x)t(x)
```

If we replace $\theta$ with $[\alpha]_1$, and $\eta$ with $[\beta]_2$, we will arrive at the updated verification formula:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + [C]_1 \bullet G_2
```

Where:

```math
\underbrace{([\alpha]_1 + \sum_{i=1}^{m}a_iu_i(\tau))}_{[A]_1} \underbrace{([\beta]_2 + \sum_{i=1}^{m}a_iv_i(\tau))}_{[B]_2} = [\alpha]_1 \bullet [\beta]_2 + \underbrace{(\alpha\sum_{i=1}^{m}a_iv_i(\tau) + \beta\sum_{i=1}^{m}a_iu_i(\tau) + \sum_{i=1}^{m}a_iw_i(\tau) + h(\tau)t(\tau))}_{[C]_1} \bullet G_2
```

**[** FYI: in $[C]_1$, we don't do $[\alpha]_1 \sum a_if_i(\tau)$ because that would incorrectly multiply an elliptic curve group element with a scalar "in the wrong space". The only valid way to turn a scalar into a group element is to multiply it by the elliptic curve's generator point. That is: $\alpha\sum_{i=1}^{m}a_iv_i(\tau)$ and its counterparts in the $[C]_1$ block are scalars in $\mathbb{F_p}$, which are evaluated first, added together, and only then multiplied with the generator point $G_1$ (through the powers of $\tau$ in the SRS) to become a commitment in $\mathbb{G_1}$. **]**

At this point, the prover could compute $[A]_1$ and $[B]_2$ without knowing the actual values of $\tau$, $\alpha$, or $\beta$. Given that the SRS includes powers of $\tau$ encoded as elliptic curve points (e.g. $\Omega_i = \tau^iG_1$) and the elliptic curve points ($[\alpha]_1$, $[\beta]_2$), the prover would compute $[A]_1$ and $[B]_2$ as:

```math
\begin{align*}
[A]_1 &= [\alpha]_1 + \sum_{i=1}^{m}a_iu_i(\tau)
\\
[B]_2 &= [\beta]_2 + \sum_{i=1}^{m}a_iv_i(\tau)
\end{align*}
```

Again, we stress that writing $a_iu_i(\tau)$ does mean that the prover knows $\tau$. It would have been discarded after the trusted setup. The prover is using the $\mathbb{G_1}$ SRS: $[\tau^{n-1}G_1, \tau^{n-2}G_1, \dots, \tau^2G_1, \tau G_1, G_1]$ to compute $u_i(\tau)$ for $i = 1, 2, \dots, m$ for $[A]_1$, and the $\mathbb{G_2}$ SRS: $[\tau^{n-1}G_2, \tau^{n-2}G_2, \dots, \tau^2G_2, \tau G_2, G_2]$ to compute $v_i(\tau)$ for $i = 1, 2, \dots, m$ for $[B]_2$.

HOWEVER, as you may have noticed, since the values of the scalars $\alpha$ and $\beta$ are unknown, it is currently impossible for the prover to compute $[C]_1$. 

Since the prover has $[\alpha]_1$ and $\sum_{i=1}^{m}a_iu_i(\tau)$, a naive thought would be that a bilinear pairing function can be used to "fake" the value of $\alpha$. That is, they might attempt to do something like: $(e(G_1, G_2)^{\alpha})^{\sum_{i=1}^{m}a_iu_i(\tau)} = e(G_1, G_2)^{\alpha\sum_{i=1}^{m}a_iv_i(\tau)}$, making it seem they have the right value. The problem here is, $e(G_1, G_2)^{\alpha\sum_{i=1}^{m}a_iv_i(\tau)}$ lies in the $\mathbb{G_{1 \ 2}}$ target group. 

Remember, the prover needs a $\mathbb{G_1}$ point for $[C]_1$ (it has to be a commitment in $\mathbb{G_1}$). As such, the prover cannot pair $[\alpha]_1$ with $\sum a_iu_i(\tau)$, and $[\beta]_2$ with $\sum a_iv_i(\tau)$ because those will just create $\mathbb{G_{1 \ 2}}$ points.

### Adjusting the Trusted Setup

Instead, the trusted setup needs to precompute $m$ polynomials for the $\sum$ terms in the problematic $C$ term of the expanded QAP. 

```math
\alpha\sum_{i=1}^{m}a_iv_i(\tau) + \beta\sum_{i=1}^{m}a_iu_i(\tau) + \sum_{i=1}^{m}a_iw_i(\tau)
```

Note here that there is a distinction between $C$ and $[C]_1$. Writing $C$ means that we still manipulating the polynomials evaluated at $\tau$. It is only when the scalars in $C$ are exponentiated onto a elliptic curve then we call the result $[C]_1$.

With some algebraic manipulation, we can combine the sum terms into a single sum:

```math
= \sum_{i=1}^{m}(\alpha a_iv_i(\tau) + \beta a_iu_i(\tau) + a_iw_i(\tau))
```

And then factor out $a_i$:

```math
= \sum_{i=1}^{m}a_i\boxed{(\alpha v_i(\tau) + \beta u_i(\tau) + w_i(\tau))}
```

From here, the trusted setup can create $m$ linear combinations of polynomials evaluated at $\tau$ from the boxed term above. The prover can then use those evaluated polynomials - which would be scalars committed to the elliptic curve group $\mathbb{G_1}$, to compute the sum. The exact details are shown in the next section.

## Trusted Setup Steps

Concretely, the trusted setup computes the following:

```math
\begin{align*}
\tau, \alpha, \beta &\leftarrow \text{random secret scalars}
\\[1pt]
[\alpha]_1 &\leftarrow \alpha \text{ commited in } \mathbb{G_1}
\\[1pt]
[\beta]_2 &\leftarrow \beta \text{ commited in } \mathbb{G_2}
\\[1pt]
[\tau^{n-1}G_1, \tau^{n-2}G_1, \dots, \tau^{2}G_1, \tau G_1, G_1] &\leftarrow \text{srs for } \mathbb{G_1} \ (\Omega_i \ \text{terms})
\\[1pt]
[\tau^{n-1}G_2, \tau^{n-2}G_2, \dots, \tau^{2}G_2, \tau G_2, G_2] &\leftarrow \text{srs for } \mathbb{G_2} \ (\Theta_i \ \text{terms})
\\[1pt]
[\tau^{n-2}t(\tau)G_1, \tau^{n-3}t(\tau)G_1, \dots, \tau^{2}t(\tau)G_1, \tau t(\tau)G_1, t(\tau)G_1] &\leftarrow \text{srs for } h(x)t(x) \text{ in } \mathbb{G_1} \ (\Upsilon_i \ \text{terms})
\\[1pt]
[\Psi_1]_1 &\leftarrow \text{for } (\alpha v_1(\tau) + \beta u_1(\tau) + w_1(\tau))G_1
\\[1pt]
[\Psi_2]_1 &\leftarrow \text{for } (\alpha v_2(\tau) + \beta u_2(\tau) + w_2(\tau))G_1
\\[1pt]
\vdots
\\[1pt]
[\Psi_m]_1 &\leftarrow \text{for } (\alpha v_m(\tau) + \beta u_m(\tau) + w_m(\tau))G_1
\end{align*}
```

We introduce the notation $[\Psi_i]_1$ to denote the $i$-th precomputed group element in $\mathbb{G_1}$ corrresponding to the linear combination of polynomials in $C$ evaluated at $\tau$ and commited in $\mathbb{G_1}$: $(\alpha v_i(\tau) + \beta u_i(\tau) + w_i(\tau))G_1$; which the trusted setup provides to allow the generation of the $[C]_1$ term.

The trusted setup thus publishes:

```math
([\alpha]_1, [\beta]_2, \text{srs}_{\mathbb{G_1}}, \text{srs}_{\mathbb{G_2}}, \text{srs}_{h(x)t(x)}, [\Psi_1]_1, [\Psi_2]_1, \dots, [\Psi_m]_1)
```

## Prover Steps

Before, the $[C]_1$ term would have been:

```math
[C]_1 = \sum_{i=1}^{m}a_i\boxed{(\alpha v_i(\tau) + \beta u_i(\tau) + w_i(\tau))} + h(\tau)t(\tau)
```

Which contains the secret scalars $\alpha$ and $\beta$, and would hence be impossible for the prover to compute. With the new $[\Psi_i]_1$ terms provided in the trusted setup, the prover can now compute:

```math
\begin{align*}
[A]_1 &= [\alpha]_1 + \sum_{i=1}^{m}a_iu_i(\tau)
\\
[B]_2 &= [\beta]_2 + \sum_{i=1}^{m}a_iv_i(\tau)
\\
[C]_1 &= \sum_{i=1}^{m}a_i[\Psi_i]_1 + h(\tau)t(\tau)
\end{align*}
```

## Verifier Steps

The verifier computes:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + [C]_1 \bullet G_2
```

## Supporting Public Inputs

In Groth16, some parts of the witness $\mathbf{a}$ must be public inputs for the verifier to check. The witness is all variables that satisfy the constraint system in Groth16 - this is the private data that the prover knows. The public input is part of the computation that everyone can know, for instance, the merkle root stored in a smart contract which everyone can use to verify information.

Groth16 lets us prove: "I know a witness $\mathbf{a}$ such that $(\text{some public input}, a)$ satisfies the circuit."

If the witness is completely private - that is the verifier does not see any part of it, then the statement that's being proved would be trivial. A prover could claim that they know the witness that satisfies a circuit, but if the verifier has no idea what the circuit is being evaluated on, then the claim is meaningless. The public inputs serve to anchor the proof to a specific claim.

So far, the verifier formula does not support public inputs - i.e. making a portion of the witness public.

By convention, the public portions of the witness are usually **the first $\ell$ elements of the witness vector $\mathbf{a}$**. To make those elements public, the prover simply reveals them:

```math
[a_1, a_2, \dots, a_{\ell}]
```

For the verifier to test that the values in the witness $\mathbf{a}$ were actually used, the verifier must carry out some of the computation that the prover was originally (supposed to be) doing.

**Now, the prover specifically computes:**

```math
\begin{align*}
[A]_1 &= [\alpha]_1 + \sum_{i=1}^{m}a_iu_i(\tau)
\\
[B]_2 &= [\beta]_2 + \sum_{i=1}^{m}a_iv_i(\tau)
\\
[C]_1 &= \sum_{i= \ \ell+1}^{m}a_i[\Psi_i]_1 + h(\tau)t(\tau)
\end{align*}
```

Notice that only the computation of $[C]_1$ changed. Now, the prover computes $[C]_1$ with $a_i$ and $[\Psi_i]_1$ **starting from terms $\ell + 1$ to $m$, that is, from $i = \ell + 1, \dots, m$.**

Then the verifier computes $[X]_1$, which is **the first $\ell$ terms of that sum term in $[C]_1$**:

```math
[X]_1 = \sum_{i=1}^{\ell}a_i[\Psi_i]_1
```

And the verification equation is now:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + [X]_1 \bullet G_2 + [C]_1 \bullet G_2
```

<hr>

#### Side Quest: Mathematically, how does $[X]_1 \bullet G_2$ and $[C]_1 \bullet G_2$ add up?

We had split the original sum term in $[C]_1$ into the following:

```math
\sum_{i=1}^{m}a_i[\Psi_i]_1 = \underbrace{\sum_{i=1}^{\ell}a_i[\Psi_i]_1}_{\text{public part, as } [X]_1} + \underbrace{\sum_{i = \ \ell+1}^{m}a_i[\Psi_i]_1}_{\text{private part, kept as } [C]_1}
```

This is the same as saying: $[X]_1 + [C]_1 \in \mathbb{G_1}$.

In the new verification equation, we can simply add $[X]_1 \bullet G_2$ to $[C]_1 \bullet G_2$ because algebraically, we are reconstructing the same bilinear pairing we had before splitting. 

That is, if we feed $[X]_1$ and $[C]_1$ into a pairing, we get:

```math
e([X]_1 + [C]_1, G_2)
```

The bilinearity of the pairing allows us to split the sum and then recombine the results by multiplying (or "adding" in additive notation) in the target group. That is, the group law in the source group ($+$) corresponds to multiplication in the target group ($\cdot$).

This means, for $P, P' \in \mathbb{G_1}$ and $Q \in \mathbb{G_2}$:

```math
\begin{align*}
e(P + P', Q) &= e(P, Q) \cdot e(P', Q) \quad \text{(multiplicative notation)} \\
&= e(P, Q) + e(P', Q) \quad \text{(additive notation)}
\end{align*}
```

Thus by bilinearity:

```math
\begin{align*}
e([X]_1 + [C]_1, G_2) &= e([X]_1, G_2) \cdot e([C]_1, G_2) \\
&= e([X]_1, G_2) + e([C]_1, G_2)
\end{align*}
```

And this matches what we see:

```math
[X]_1 \bullet G_2 + [C]_1 \bullet G_2
```

To be more explicit about the above:

```math
\begin{align*}
[C]_1 \bullet G_2 &= e \biggl(\sum_{i=1}^{m}a_i[\Psi_i]_1, G_2 \biggr) 
\\[12pt]
&= e \biggl(\sum_{i=1}^{\ell}a_i[\Psi_i]_1 + \sum_{i = \ \ell+1}^{m}a_i[\Psi_i]_1, G_2 \biggr)
\\[12pt]
&= e \biggl(\sum_{i=1}^{\ell}a_i[\Psi_i]_1, G_2 \biggr) + e \biggl(\sum_{i = \ \ell+1}^{m}a_i[\Psi_i]_1, G_2 \biggr)
\\[16pt]
&= [X]_1 \bullet G_2 + [C]_1 \bullet G_2
\end{align*}
```

<hr>

## Part 2: Separating the Public Inputs from the Private Inputs with $\gamma$ and/or $\delta$

### Forging proofs by misusing $\Psi_i$ for $i \le \ell$

The assumption in the verification equation:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + [X]_1 \bullet G_2 + [C]_1 \bullet G_2
```

Is that the prover is only using $\Psi_{\ell + 1}$ to $\Psi_m$ to compute $[C]_1$. However this does not stop a dishonest prover from using $\Psi_1$ to $\Psi_{\ell}$ to compute $[C]_1$, leading to a forged proof.

For example, we expand $[X]_1$ and $[C]_1$ under the hood:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + \underbrace{\sum_{i=1}^{\ell}a_i[\Psi_i]_1}_{[X]_1} \bullet G_2 + \underbrace{(\sum_{i= \ \ell+1}^{m}a_i[\Psi_i]_1 + h(\tau)t(\tau))}_{[C]_1} \bullet G_2
```

Suppose, and without loss of generality that:

```math
\begin{align*}
\mathbf{a} &= [1, 2, 3, 4, 5] \\
\ell &= 3
\end{align*}
```

This means that the public part of the witness is $[1, 2, 3]$ and the private part of the witness is $[4, 5]$.

The final verification equation would be as follows:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + \underbrace{(1\Psi_1 + 2\Psi_2 + 3\Psi_3)}_{[X]_1} \bullet G_2 + \underbrace{(4\Psi_4 + 5\Psi_5)}_{[C]_1} \bullet G_2
```

Nothing stops a dishonest prover from creating the public part of the witness as $[1, 2, 0]$ instead of $[1, 2, 3]$, and moving the zero-ed out portion of the public part into the private part of the witness, i.e. the private part would be $[3, 4, 5]$ instead of $[4, 5]$.

As such, the dishonest prover's computation of $[C]_1$ then uses $\Psi_{\ell}$:

```math
[A]_1 \bullet [B]_1 \stackrel{?}{=} [\alpha]_1 \bullet [\beta]_2 + \underbrace{(1\Psi_1 + 2\Psi_2 + \boxed{0\Psi_3})}_{[X]_1} \bullet G_2 + \underbrace{(\boxed{3\Psi_3} + 4\Psi_4 + 5\Psi_5)}_{[C]_1} \bullet G_2
```

The equation above is valid since adding $[X]_1$ and $[C]_1$ still produces: $(1\Psi_1 + 2\Psi_2 + 3\Psi_3 + 4\Psi_4 + 5\Psi_5) \bullet G_2$, and the pairing check would pass; but the witness does not necessarily satisfy the original constraints.

**[** A verifier expects to check a proof about public inputs $[1, 2, 3]$, but in reality, the prover provided a proof about public inputs $[1, 2, 0]$. Passing the pairing check in this instance would mean that the verifier is convinced of the wrong statement. That is, the verifier believes the proof is about the statement with public inputs $[1, 2, 3]$, but the proof given is actually consistent with the statement with public inputs $[1, 2, 0]$, thereby believing a false claim. The value $3$, which should have been known to the verifier, was shifted into the private part of the witness where the verifier has no visibility. The prover has forged a valid-looking proof for a false statement, or in other words, generated a proof that verifies correctly but does not correspond to the claimed public inputs. **]**

Therefore, we need to prevent the prover from using $\Psi_1$ to $\Psi_{\ell}$ (in whole or in part) as part of their computation of $[C]_1$.

### Introducing $\gamma$ and/or $\delta$

To avoid the problem with having a dishonest prover using $\Psi_1$ to $\Psi_{\ell}$, the trusted setup introduces a new scalar: $\gamma$ and(or) $\delta$, to force $\Psi_{\ell + 1}$ to $\Psi_m$ to be separate from $\Psi_1$ to $\Psi_{\ell}$. 

To do this, **the tusted setup divides (multiplies by the [modular inverse](https://rareskills.io/post/finite-fields#multiplicative-inverse))**:

- **The private terms of the witness (that constitute $[C]_1$, the sum the prover computes) by $\delta$;** *and/or*

- **The public terms of the witness (that constitute $[X]_1$, the sum the verifier computes) by $\gamma$.**

Since the $h(\tau)t(\tau)$ term is embedded in $[C]_1$, those terms also need to be divided by $\delta$. If either $\delta$ and $\gamma$ (in their commitments) have an unknown discrete logarithm, then the forgery described earlier along possible other methods of forgery are avoided. This method was used in Zcash's Sapling based [trusted setups](https://github.com/ebfull/phase2/blob/master/src/lib.rs#L808), where $\gamma$ is simply left to $G_2$ (as $[\gamma]_2$), and $\delta$ is still updated from $G_2$ (as $[\delta]_2$) to a random value at the later stages of the trusted setup.

Another way to look at $\gamma$ and\or $\delta$, is that private inputs are now scaled by $1/\delta$, and public inputs are now scaled by $1/\gamma$. That means the prover's private terms of the witness in $[C]_1$ exist in the span of $\{[\Psi_i]_1 / \delta\}$ for $i = \ell + 1, \dots, m$; and the verifier's public terms of the witness in $[X]_1$ exist in the span of $\{[\Psi_i]_1 / \gamma \}$ for $i = 1, \dots, \ell$.

Now the prover cannot freely move terms from the public part of the witness into the private part of the witness, since that would require rebalancing $\gamma$ and $\delta$. More so if $\delta$ or $\gamma$ are unknown, then the prover cannot algebraically manipulate both sides of the witness to forge proofs, e.g. taking a public term and multiplying it by $\delta/\gamma$ to make it look like a private term. This is the same as trying to solve the discrete logarithm problem.

The **updated trusted setup supporting public inputs** is now the following:

```math
\begin{align*}
\tau, \alpha, \beta, \gamma, \delta &\leftarrow \text{random secret scalars}
\\[4pt]
[\alpha]_1 &\leftarrow \alpha \text{ commited in } \mathbb{G_1}
\\[4pt]
[\beta]_2 &\leftarrow \beta \text{ commited in } \mathbb{G_2}
\\[4pt]
[\gamma]_2 &\leftarrow \gamma \text{ commited in } \mathbb{G_2}
\\[4pt]
[\delta]_2 &\leftarrow \delta \text{ commited in } \mathbb{G_2}
\\[4pt]
[\tau^{n-1}G_1, \tau^{n-2}G_1, \dots, \tau^{2}G_1, \tau G_1, G_1] &\leftarrow \text{srs for } \mathbb{G_1} \ (\Omega_i \ \text{terms})
\\[4pt]
[\tau^{n-1}G_2, \tau^{n-2}G_2, \dots, \tau^{2}G_2, \tau G_2, G_2] &\leftarrow \text{srs for } \mathbb{G_2} \ (\Theta_i \ \text{terms})
\\[4pt]
[\frac{\tau^{n-2}t(\tau)G_1}{\delta}, \frac{\tau^{n-3}t(\tau)G_1}{\delta}, \dots, \frac{\tau^{2}t(\tau)G_1}{\delta}, \frac{\tau t(\tau)G_1}{\delta}, \frac{t(\tau)G_1}{\delta}] &\leftarrow \text{srs for } h(x)t(x) \text{ in } \mathbb{G_1} \ (\Upsilon_i \ \text{terms})
\\[12pt]
&\boxed{\text{for public portion of the witness: } [X]_1 \ (\text{scaled by } 1/\gamma)}
\\[12pt]
[\Psi_1]_1 &= \frac{\alpha v_1(\tau) + \beta u_1(\tau) + w_1(\tau)G_1}{\gamma}
\\[8pt]
[\Psi_2]_1 &= \frac{\alpha v_2(\tau) + \beta u_2(\tau) + w_2(\tau)G_1}{\gamma}
\\[1pt]
\vdots
\\[1pt]
[\Psi_{\ell}]_1 &= \frac{\alpha v_{\ell}(\tau) + \beta u_{\ell}(\tau) + w_{\ell}(\tau)G_1}{\gamma}
\\[12pt]
&\boxed{\text{for private portion of the witness: } [C]_1 \ (\text{scaled by } 1/\delta)}
\\[12pt]
[\Psi_{\ell+1}]_1 &= \frac{\alpha v_{\ell+1}(\tau) + \beta u_{\ell+1}(\tau) + w_{\ell+1}(\tau)G_1}{\delta}
\\[8pt]
[\Psi_{\ell+2}]_1 &= \frac{\alpha v_{\ell+2}(\tau) + \beta u_{\ell+2}(\tau) + w_{\ell+2}(\tau)G_1}{\delta}
\\[1pt]
\vdots
\\[1pt]
[\Psi_{m}]_1 &= \frac{\alpha v_{m}(\tau) + \beta u_{m}(\tau) + w_{m}(\tau)G_1}{\delta}
\end{align*}
```