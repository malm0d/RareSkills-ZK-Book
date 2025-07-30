# Trusted Setup
https://rareskills.io/post/trusted-setup

A trusted setup is a mechanism zk-SNARKs use to evaluate a polynomial at a **secret value (secret scalar)**.

Given a polynomial $f(x)$, observe that it can be evaluated by computing the **inner product** (dot product) of the polynomial coefficients with successive powers of $x$.

For example, if the polynomial $f(x)$ was a degree $3$ polynomial:

```math
f(x) = 3x^3 + 2x^2 + 5x + 10
```

Then the coefficients are: $[3, 2, 5, 10]$, and we can compute the polynomial as:

```math
f(x)=\langle[3,2,5,10],[x^3,x^2,x, 1]\rangle
```

The key is to represent the successive powers of $x$ as a vector of polynomial terms ($x$ terms) in **descending order** starting from the degree of the polynomial (regardless of whether each successive $x$ term is present in the original polynomial, i.e. if $d = 5$, then it should be $[x^5, x^4, x^3, x^2, x, 1]$). Note that $1$ is actually $x^0$.

In other words, if we want to evaluate the polynomial $f(x)$ at $x = 2$, we could view the evaluation of $f(2)$ as:

```math
f(2) = 3(2)^3 + 2(2)^2 + 5(2) + 10 \\[4pt]
\text{or} \\[4pt]
\begin{align*}
f(2) &= \langle[3,2,5,10],[2^3,2^2,2,1]\rangle \\
&= \langle[3,2,5,10],[8,4,2,1]\rangle \\
&= (3 \cdot 8) + (2 \cdot 4) + (5 \cdot 2) + (10 \cdot 1)
\end{align*}
```

Now, if we introduce a secret scalar: $\tau$, and do the same computation, we'd get:

```math
[\tau^3, \tau^2, \tau, 1]
```

In elliptic curve cryptography, all operations are performed on points of an elliptic curve group. The "discrete log" of a point $P$ with respect to the generator of the elliptic curve group $G$ is the scalar $k$ such that $P = kG$. The discrete log problem is thus computationally hard and infeasible to solve. At this point, if we were to compute $f(\tau)$ directly, this would directly reveal what the actual value for $\tau$ is.

Remember that when the order of the finite field is equal to the order of the elliptic curve group, every operation in the finite field has a homomorphic equivalent in the elliptic curve group. **Arithmetic (addition/scalar multiplication) in a finite field is homomorphic to arithmetic (addition/scalar multiplication) in an elliptic curve group**. Or in other words: Elliptic curves over finite fields homomorphically encrypt addition (and repeated addition) in a finite field.

That is, if we compute: $\tau G_1$, we are effectively encoding $\tau$ in the exponent of $G_1$.

```math
\begin{align*}
\phi(a + b) \mod p &= (a + b)G_1 \\
&= (a)G_1 \oplus (b)G_1 \\
&= \phi(a) \oplus \phi(b)
\end{align*}
```

Where:
- $a, b \in \mathbb{F_p}$ (scalars, which also includes $\tau \in \mathbb{F_p}$).
-  $G_1$ is the generator for the elliptic curve group $G_1$.
- $+$ denotes addition (arithmetic) in $\mathbb{F_p}$.
- $\oplus$ denotes point addition on the elliptic curve group.

Thus, when we multiply each of the points in $[\tau^3, \tau^2, \tau, 1]$ with a generator point of a cryptographic elliptic curve group (e.g. $G_1$), we'd get the result:

```math
\begin{align*}
[\Omega_3, \Omega_2, \Omega_1, G_1] &= [(\tau^3 \cdot G_1), (\tau^2 \cdot G_1), (\tau \cdot G_1), (1 \cdot G_1)] \\
&= [\tau^3G_1,\tau^2G_1,\tau G_1,G_1]
\end{align*}
```

On a side note, we can thus derive something more generic:

```math
[\Omega_d, \ \Omega_{d-1}, \ \Omega_{d-2}, ..., \ \Omega_1, \ G_1] = [\tau^d G_1, \ \tau^{d-1} G_1, \ \tau^{d-2} G_1, \ ..., \ \tau G_1, \ G_1]
```

Where each $\Omega_i$ should be an elliptic curve point $\tau^iG_1$.

The ordered list of elements: $[\Omega_3, \Omega_2, \Omega_1, G_1]$ is known as the **structured reference string (SRS)**. With this SRS, anyone can evaluate a degree $= 3$ polynomial (or less) on the scalar $\tau$.

For instance, if we have a degree $= 2$ polynomial $g(x) = 4x^2 + 7x + 8$, we can evaluate $g(\tau)$ by taking the inner product of the SRS with the polynomial coefficients:

```math
\begin{align*}
g(\tau) &= \langle[0, 4, 7, 8], [\Omega_3, \Omega_2, \Omega_1, G_1]\rangle \\
&= 4\Omega_2 + 7\Omega_1 + 8G_1 \\
&= 4\tau^2G_1 + 7\tau G_1 + 8G1 
\end{align*}
```

We have effectively computed $g(\tau)$ without knowing what $\tau$ is since it is hidden in the SRS.