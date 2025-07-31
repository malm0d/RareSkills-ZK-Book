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

Remember that when the order of the finite field is equal to the order of the elliptic curve group, every operation in the finite field has a homomorphic equivalent in the elliptic curve group. **Addition (and scalar multiplication) in a finite field is homomorphic to addition (and scalar multiplication) in an elliptic curve group**. Or in other words: Elliptic curves over finite fields homomorphically encrypt addition (and repeated addition) in a finite field.

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
- $+$ denotes addition in $\mathbb{F_p}$.
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

We have effectively computed $g(\tau)$ without knowing what $\tau$ is, since $\tau$ is hidden in the SRS.

Notice that we have $0$ in the slot for the coefficeint of the $x^3$ term as the polynomial is only of degree $=2$ (there is no $x^3$ term).

Because of the homomorphism $\phi$ we discussed earlier in the article, when we evaluated $g(x)$ at the secret scalar $\tau$, we computed the polynomial $g(\tau)$ "in the exponent" of the elliptic curve group. That is:

```math
\begin{align*}
g(\tau) &= 4\Omega_2 + 7\Omega_1 + 8G_1 \\[4pt]
g(\tau)G_1&= 4\tau^2G_1 + 7\tau G_1 + 8G1 
\end{align*}
```

The result of the polynomial evaluation $g(\tau)$ is in fact a scalar, but it is hidden in the elliptic curve point $g(\tau)G_1$. That is to say, the evaluation at $g(\tau)G_1$ is an elliptic curve point, and $g(\tau)$ is the discrete log with respect to the generator point $G_1$.

While we are able to compute the point $g(\tau)G_1$ using the SRS, it is infeasible for us to recover the scalar $g(\tau)$ itself because solving the discrete log problem is extremely difficult.

This is also called a trusted setup, because although we don't know what the discrete log $g(\tau)$ is, the person who created the SRS does. This could lead to leaking information down the line, so we are technically trusting that the entity creating the trusted setup deletes $\tau$ and in no way remebers it.

```python
from py_ecc.bn128 import G1, multiply, add
from functools import reduce

def inner_product(coeffs, points):
    return reduce(add, map(multiply, points, coeffs))

## Trusted setup
tau = 88
degree = 3

# SRS = tau^3, tau^2, tau, 1
# range(start, stop(not inclusive), step)
# range(3, -1, -1) = [3, 2, 1, 0]
srs = [multiply(G1, tau**i) for i in range(degree, -1, -1)]

## Evaluate
# p(s) = 4x^2 + 7x + 8
coeffs = [0, 4, 7, 8]
```

## Verifying a Trusted Setup was Generated Properly
Given a SRS, how do we know that it follows the descending structure $[x^d, x^{d-1}, ..., x, 1]$, or more specifically:

```math
[\Omega_d, \Omega_{d-1}, ..., \Omega_1, G_1] \quad (\text{or }
[\tau^d, \tau^{d-1}, ..., \tau, 1])
```

And that it wasn't randomly (and haphazardly) chosen?

Remember what we learned about the property of an elliptic curve [bilinear pairing](https://rareskills.io/post/bilinear-pairing):

```math
e(G,\, G)^{ab} = e(aG_1, bG_2) = e(abG_1, G_2) = e(G_1, abG_2)
```

If the party doing the trusted setup provides $\Theta=\tau G_2$, we can validate that the SRS is indeed in successive powers of $\tau$. We can use the following:

```math
e(\Theta, \Omega_i) \stackrel{?}{=} e(G_2, \Omega_{i+1})
```

Where $e$ is a bilinear pairing. Intuitively, we are computing $\tau \cdot \tau^i$ on the left hand side of the equality and $1 \cdot \tau^{i+1}$ on the right hand side of the equality. The above can be further expressed as such:

```math
\begin{align*}
e(\Theta, \Omega_i) &\stackrel{?}{=} e(G_2, \Omega_{i+1}) \\[4pt]
e(\tau G_2, \tau^iG_1) &\stackrel{?}{=} e(G_2, \tau^{i+1}G_1) \\[4pt]
e(G_2, G_1)^{\tau \cdot \tau^i} &\stackrel{?}{=} e(G_2, G_1)^{\tau^{i+1}} \\[4pt]
e(G_2, G_1)^{\tau^{1 + i}} &\stackrel{?}{=} e(G_2, G_1)^{\tau^{i+1}}
\end{align*}
```

By virtue of the homomorphism between addition in a finite field and addition in an elliptic curve group, we are effectively comparing exponents:

```math
\tau^{1+i} \stackrel{?}{=} \tau^{i + 1}
```

This ensures that $\Omega_i \cdot \tau = \Omega_{i+1}$. That is, each $\Omega_i$ is $\tau^iG_1$.

Therefore to validate that $\Theta$ and $\Omega_1$ have the same discrete logarithms (where $\Omega_1 = \tau G_1$), we can check the bilinear pairings:

```math
e(\Theta, G_1) \stackrel{?}{=} e(G_2, \Omega_1) \\[4pt]
e(\tau G_2, G_1) \stackrel{?}{=} e(G_2, \tau G_1) \\[4pt]
e(G_2, G_1)^\tau \stackrel{?}{=} e(G_2, G_1)^\tau
```

## Generating a SRS as part of a Multiparty Computation (Powers of $\tau$ Ceremony)
It is not a good enough assumption that the party that generated the SRS actually deleted the secret scalar $\tau$.

The following describes the algorithm for multiple parties to collaboratively create the SRS; and as long as one of them is honest (i.e. deletes $\tau$), then the discrete logs of the SRS will never be known.

Alice generates the SRS: ($[\Omega_n, \Omega_{n-1}, ..., \Omega_2, \Omega_1, G_1], \Theta$), where $\Theta = \tau G_2$, and then passes it to Bob.

Bob verifies that the SRS is indeed in successive powers of $\tau$ by performing the bilinear pairing checks as described earlier.

Next, Bob selects his own secret scalar: $\gamma$. Then, using the SRS he just verified, Bob - adhering to the structure of the SRS, computes:

```math
([\gamma^n\Omega_n, \ \gamma^{n-1}\Omega_{n-1}, \ ..., \ \gamma^2\Omega_2, \ \gamma\Omega_1, \ G_1], \ \gamma\Theta)
```

Which translates to:

```math
([(\gamma\tau)^nG_1, \ (\gamma\tau)^{n-1}G_1, \ ..., \ (\gamma\tau)^2G_1, \ (\gamma\tau)G_1, \ G_1], \ (\gamma\tau)G_2)
```

This effectively results in the discrete logs of the SRS to be:

```math
([(\gamma\tau)^n, \ (\gamma\tau)^{n-1}, \ ..., \ (\gamma\tau)^2G_1, \ (\gamma\tau), \ 1], \ (\gamma\tau))
```

If Alice or Bob deletes $\tau$ or $\gamma$, then the discrete logs of the SRS can never be recoverable.

This is just an example showing two parties involved in the generation of the SRS, in reality, there can be as many parties involved in the process as needed. This multiparty computation is often informally referred to as the **powers of $\tau$ ceremony**.

## The Use of a Trusted Setup in ZK-SNARKs
Evaluating a polynomial on a structured reference string doesn’t reveal information about the polynomial to the verifier, and the prover doesn’t know what point they are evaluating on. We will see later that this scheme helps prevent the prover from cheating and helps keep their witness zero knowledge.