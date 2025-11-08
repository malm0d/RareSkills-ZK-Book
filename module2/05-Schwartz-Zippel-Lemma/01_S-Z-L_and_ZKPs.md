# Schwartz-Zippel Lemma and its applications to Zero Knowledge Proofs
https://www.rareskills.io/post/schwartz-zippel-lemma

Nearly all ZK-Proof algorithms (e.g. Groth16, Halo2, PLONK, e.t.c) rely on the Schwartz-Zippel Lemma to achieve succintness.

The Schwartz-Zippel Lemma states that, if we are given two polynomials: 
```math
P(x) \quad \text{and} \quad Q(x)
```

with polynomial degrees: $d_P$ for $P(x)$, and $d_Q$ for $Q(x)$, and if $P(x) \neq Q(x)$, then the number of points where $P(x)$ and $Q(x)$ intersect is $\le \max(d_P, d_Q)$.

This is not the final definition yet, we will come back to it.

Consider the following examples.

## Example polynomials and the Schwartz-Zippel Lemma

### A Straight Line Crossing a Parabola

Consider the polynomials $P(x) = x$ and $Q(x) = x^2$. The two polynomials intersect each other at $x = 0$ and $x = 1$. 

![ss-line-parabola](/module2/05-Schwartz-Zippel-Lemma/schwartz-zippel-x-x2-example.png)

$P(x)$ is a degree $1$ polynomial, while $Q(x)$ is degree $2$ polynomial. Notice that the intersect at $2$ points, which is the maximum degree between the two polynomials: $\le \max(d_P, d_Q)$.

### A Degree 3 Polynomial and a Degree 1 Polynomial
Consider the degree $3$ polynomial $P(x) = x^3$ and the degree $1$ polynomial $Q(x) = x$. The polynomials intersect each other at $x = -1$, $x = 0$, and $x = 1$.

![ss-d3-d1](/module2/05-Schwartz-Zippel-Lemma/schwartz-zippel-x-x3-example.png)

Just like before, the number of intersections between the two polynomials is bounded by the maximum degree of the polynomials, which is $3$ for this example.

## Schwartz-Zippel Lemma and Polynomials in a Finite Field
The Schwartz-Zippel Lemma holds for polynomials in a finite field. That is, all computations involving the polynomials are done in modular arithmetic: $\text{mod} \ p$, where $p$ is a PRIME number.

### Polynomial Equality Testing
We can test that two polynomials are equal by checking if all their coefficients are equal, but this takes $O(d)$ time where $d$ is the degree of the polynomials.

Meaning, if two degree $\le d$ polynomials:
```math
P(x) = a_0 + a_1x + a_2x^2 + ... + a_dx^d \\
Q(x) = b_0 + b_1x + b_2x^2 + ... + b_dx^d
```

are stored by their coefficients, we can prove equality simply by comparing each pair $(a_i, b_i)$, so the work is $O(d)$.

Instead, we can evaluate both polynomials at a randomly chosen point $u$, and compare their results. If $P(u) = Q(u)$, then it is extremely likely that $P(x) = Q(x)$.

And this would be in $O(1)$ time.

That is, in a finite field $\mathbb{F}_{p}$, where $p$ is a prime, we pick a random value $u$ from $[0, p)$ (from $0$ up to but not including $p$). Then we evalute:

```math
y_P = P(u) \quad \text{and} \quad y_Q = Q(u)
```

Then, if $y_P \neq y_Q$, then $P(x)$ and $Q(x)$ are definitely not equal.

But if $y_P = y_Q$, then ONE of two things must be true:

1. $P(x) = Q(x)$ (the polynomials are identical).

2. $P(x) \neq Q(x)$, but $u$ is one of the $d$ points ($d = \max(d_P, d_Q)$) where the polynomials intersect.
    
    - $u$ is a root of the polynomial $H(x) = P(x) - Q(x)$
    - Recall that a polynomial of degree $d$ can have at most $d$ roots.

Remember that the Schwartz-Zippel Lemma is done in a finite field $p$. Thus if $d \ll p$, then situation 2 is unlikely to occur - to the point of being negligible.

When we take the difference between two polynomials, we are finding the point where the two polynomials are equal. Specifically, if the difference polynomial is $P(x) - Q(x) = H(x)$:

- The roots of $H(x)$ are exactly the $x$ values where $P(x) = Q(x)$ ($x$ values where $H(x) = 0$).

And if the difference is a non-zero polynomial of degree $d$, then by the Schwartz-Zippel Lemma, $P(x)$ and $Q(x)$ can agree at at most
$d$ points (when evaluated over a field):

- The Fundamental Theorem of Algebra states: A non-zero polynomial of degree $d$ has at most $d$ roots.
- This directly means:
  - If H(x) = P(x) - Q(x) is degree $d$ and not the zero polynomial, then $H(x)$ has at most $d$ roots.
  - Since roots of $H(x)$ are where $P(x) = Q(x)$, the polynomials can agree at most $d$ times.

### Probability of Error from the Schwartz-Zippel Lemma
Situation 2 is extremely unlikely to occur, and the following explains why we can consider its occurrence negligible.

In a prime finite field $\mathbb{F}_{p}$, there are exactly $p$ distinct field elements. Thus the field modulus determines the size of the field (i.e. $|\mathbb{F}_{p}|$).

If $P(x) \neq Q(x)$, then the polynomial $H(x) = P(x) - Q(x)$ is a non-zero polynomial of degree at most $d = \max(d_P, d_Q)$. A non-zero polynomial of degree $d$ can have at most $d$ roots (points where $H(x) = 0$). 

By the Fundamental Theorem of Algebra (for finite fields), this means $H(x)$ can have at most $d$ roots in $\mathbb{F}_{p}$.

The probability of a RANDOMLY chosen $u$, where $u \in \mathbb{F}_{p}$, is essentially $\frac{d}{p}$. Think of it as we have $d$ "bad" choices (roots where $P(u) = Q(u)$) out of $p$ total choices. Specifically, the probability is:

```math
Pr[P(u) = Q(u) | P \neq Q] \le \frac{d}{p}
```

Which means for a random $u$ (one of the roots) the Schwartz-Zippel Lemma can give a "false" verdict, but this can happen for at most $d$ out of the $p$ possible field elements.

For example, if the field $\mathbb{F}_{p}$ has $p \approx 2^{254}$ (slightly smaller than a `uint256` type in Solidity), and if the polynomials are not more than 1 million degress large, then the probability of randomly picking a point where they intersect is:

```math
\frac{1\times 10^6}{2^{254}} \approx \frac{2^{20}}{2^{254}} \approx \frac{1}{2^{234}} \approx \frac{1}{10^{70}}
```

Thus it is extremely unlikely that we will randomly pick a point where the polynomials will intersect - if the polynomials are not equal.

## A More Formal Description of the Schwartz-Zippel Lemma
As a way of summarizing the chapter thus far, we can describe the Schwartz-Zippel Lemma a little more formally as the following.

Given two DISTINCT polynomials $P(x)$ and $Q(x)$ of degrees $d_P$ and $d_Q$ respectively, over a finite field $\mathbb{F}$, the number of points $u \in \mathbb{F}$ where $P(u) = Q(u)$ is $\le \max(d_P, d_Q)$.

In other words if $P(x) \neq Q(x)$, they can agree on at most $\max(d_P, d_Q)$ points.

Or another way to put it, the Schwartz-Zippel Lemma effectively says that: if two distinct polynomials $P(x)$ and $Q(x)$ evaluate to the same value at a randomly chosen point $u$, then they are almost certainly identical (with an error probability of $\frac{d}{|\mathbb{F}{p}|}$, where $d \le \max(d_P,d_Q)$).

## Using the Schwartz-Zippel Lemma to Test if Two Vectors are Equal
We can combine Lagrange Interpolation with the Schwartz-Zippel Lemma to test if two vectors are equal.

Usually, when checking for vector equality, we would iterate through the $n$ components of the vectors and check that they are equal. That is, given two vectors $[a_1, ..., a_n]$ and $[b_1, ..., b_n]$ to check if the vectors are equal, we compare all the corresponding components:

```math
a_1 = b_1, \ ..., \ a_n = b_n
```

Instead, if we used a common set of $x$ values, say: $[1, 2, ..., n]$ to interpolate the two vectors:

1. We can interpolate a polynomial for each vector. We will get polynomials $f(x)$ and $g(x)$.
2. Pick a random point $u$, where $u \notin [1, 2, ..., n]$.
3. Evaluate each polynomial at $u$.
4. Check if $f(u) = g(u)$

Although computing the polynomials is more work, the final check is much cheaper.

The key idea here is to convert vectors into polynomials using Langrange interpolation, then use the Schwartz-Zippel Lemma to test their equality.

Here's a more detailed breakdown of the above.

Given two vectors of length $n$:

```math
A = [a_1, a_2, ..., a_n] \\
B = [b_1, b_2, ..., b_n]
```

We treat these vectors as sets of points on polynomials. That is, we pair each value from the common set of $x$ values $[1, 2, ..., n]$ to each vector index in $A$ and $B$. This makes the components from vectors $A$ and $B$ become $y$ values. Now we have two sets of $n$ points:

```math
A = (1, a_1), (2, a_2), ..., (n, a_n) \\
B = (1, b_1), (2, b_2), ..., (n, b_n)
```

Using Lagrange interpolation, we can compute the two Lagrange interpolating polynomials that passes through all points in set $A$ and set $B$ respectively.

- $f(x)$: Passes through all points $(i, a_i)$ for vector $A$
- $g(x)$: Passes through all points $(i, b_i)$ for vector $B$

And by Lagrange interpolation, both $f(x)$ and $g(x)$ will be polynomials of degree $d \le (n-1)$ since they fit $n$ points.

We pick a random value for $u$. Ideally, $u$ should be outside the interpolation points (i.e. $u \notin [1, 2, ..., n]$) so we can avoid trivial matches

Next, we compute $f(u)$ and $g(u)$ to evaluate the polynomials. Then we compare $f(u)$ and $g(u)$

- If $f(u) \neq g(u)$, then the vectors are not equal.
- If $f(u) = g(u)$, then the vectors are equal with an error probability $\le \frac{d}{p}$

### Example in Python
```python
import galois
import numpy as np
import random

p = 103
GF = galois.GF(p)

#Common set of x values
x_common = GF(np.array([1, 2, 3]))

# Arbitrary vectors
A = GF(np.array([4,8,19]))
B = GF(np.array([4,8,19]))

# Lagrange interpolating polynomials
fx = galois.lagrange_poly(x_common, A)
gx = galois.lagrange_poly(x_common, B)

# Pick u from [0, p)
u = random.randint(0, p)

# f(u) = g(u)
lhs = fx(u)
rhs = gx(u)

# Only one check required
assert lhs == rhs

#----------------------------------------

# Arbitrary vectors that are not equal
C = GF(np.array([5, 13, 29]))
D = GF(np.array([7, 17, 23]))

# Lagrange interpolating polynomials
cx = galois.lagrange_poly(x_common, C)
dx = galois.lagrange_poly(x_common, D)

# f(u) = g(u)
lhs_ = cx(u)
rhs_ = dx(u)

assert lhs_ != rhs_
```

## Using the Schwartz-Zippel Lemma in ZK Proofs
The  end goal is for the prover to send a small string of data to the verifier such that the verifier can quickly check.

Most of the time, a ZK proof is essentially a polynomial evaluated at a random point.

The difficulty we have to solve is that we do not know if the polynomial is evaluated honestly. Somehow, we have to trust that the prover is not lying when they evaluate $f(u)$.

But before getting to that, we need to learn how to represent an entire arithmetic circuit as a small set of polynomials evaluated at a random point, which is the motivation for [Quadratic Arithmetic Programs](https://rareskills.io/post/quadratic-arithmetic-program) (next chapter).