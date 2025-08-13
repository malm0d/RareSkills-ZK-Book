# Evaluating a Quadratic Arithmetic Program on a Trusted Setup
https://rareskills.io/post/elliptic-curve-qap

Evaluating a [Quadratic Arithmetic Program (QAP)](https://rareskills.io/post/quadratic-arithmetic-program) on a trusted setup enables a prover to demonstrate that a QAP is satisfied without revealing the witness while using a constant sized proof. In pairing based SNARKs, the proof is typically made of elliptic curve points.

Specifically, the QAP polynomials are evaluated at an unknown point (or secret scalar) $\tau$.

The QAP equation:

```math
\sum_{i = 1}^{m}a_iu_i(x) \sum_{i=1}^{m}a_iv_i(x) = \sum_{i=1}^{m}a_iw_i(x) + h(x)t(x)
```

will be balanced if and only if the witness $\mathbf{a}$ satisfies the equation; and will be unbalanced with overwhelming probability otherwise.

The scheme shown in this chapter is not a secure ZK proof, but it is a stepping stone to the next chapter on Groth16.

## A Concrete Example
To make this less abstract, assume that the matrices of the [R1CS](https://rareskills.io/post/rank-1-constraint-system): $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ have the dimensions $3$ rows $\times$ $4$ columns. That is, $n = 3$ and $m = 4$.

```math
\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}
```

Since we have $n = 3$ rows (which reflects 3 constraints in the R1CS), we would be interpolating over the points $x = [1, 2, 3]$ when we carry out Lagrange interpolation; and by Lagrange interpolation, our interpolating polynomials will be at most degree $n - 1 = 2$. And since we have $m = 4$ columns for each matrix, then each matrix will yield $4$ interpolating polynomials, giving us a total of $12$ polynomials from the R1CS.

Based on the above, our QAP will thus be:

```math
\sum_{i = 1}^{4}a_iu_i(x) \sum_{i=1}^{4}a_iv_i(x) = \sum_{i=1}^{4}a_iw_i(x) + h(x)t(x)
```

## Notation and Preliminaries
The elliptic curve generator point for the elliptic curve group $\mathbb{G_1}$ is notated as: $G_1$. And the elliptic curve generator point for the elliptic curve group $\mathbb{G_2}$ is notated as: $G_2$.

An element in $\mathbb{G_1}$ is notated as $[X]_1$. And an element in $\mathbb{G_2}$ is notated as $[X]_2$. When there is ambiguity with the subscripts referring to indices (items) in a list, we say $X \in \mathbb{G_1}$ or $X \in \mathbb{G_2}$.

An [elliptic curve pairing (bilinear pairing)](https://rareskills.io/post/bilinear-pairing) between two elliptic curve points is denoted as $[X]_1 \bullet [Y]_2$.

For a matrix $\mathbf{L}$, let $\mathbf{L}_{(*,\ j)}$ denote all rows (*) and the $j$-th column of the matrix.

Let $\mathcal{L}(\mathbf{L}_{(*,\ j)})$ denote the interpolating polynomial obtained from running Lagrange interpolation on the $j$-th column of $\mathbf{L}$, using the set of $x = [1, 2, 3]$ (which we established earlier). And the values of the $j$-th column would thus represent the $y$ values.

Let the polynomial $p_{i,j}$ denote the $i$-th polynomial of the matrix (i.e. the polynomial interpolated from $i$-th column vector of the matrix), and the $j$-th coefficient power (i.e. the polynomial term of degree $j$). Note that if $j = 0$, it refers to a polynomial term of degree $0$ which yields $x^0 = 1$.

Since $m = 4$ columns, we obtain the following 4 polynomials from matrix $\mathbf{L}$:

```math
\begin{align*}
u_1(x) = \mathcal{L}(\mathbf{L}_{(*,1)}) =u_{1,2}x^2 + u_{1,1}x+u_{1,0}\\
u_2(x) = \mathcal{L}(\mathbf{L}_{(*,2)}) =u_{2,2}x^2 + u_{2,1}x+u_{2,0}\\
u_3(x) = \mathcal{L}(\mathbf{L}_{(*,3)}) =u_{3,2}x^2 + u_{3,1}x+u_{3,0}\\
u_4(x) = \mathcal{L}(\mathbf{L}_{(*,4)}) =u_{4,2}x^2 + u_{4,1}x+u_{4,0}\\
\end{align*}
```

And the following 4 polynomials from matrix $\mathbf{R}$:

```math
\begin{align*}
v_1(x) = \mathcal{L}(\mathbf{R}_{(*,1)}) =v_{1,2}x^2 + v_{1,1}x+v_{1,0}\\
v_2(x) = \mathcal{L}(\mathbf{R}_{(*,2)}) =v_{2,2}x^2 + v_{2,1}x+v_{2,0}\\
v_3(x) = \mathcal{L}(\mathbf{R}_{(*,3)}) =v_{3,2}x^2 + v_{3,1}x+v_{3,0}\\
v_4(x) = \mathcal{L}(\mathbf{R}_{(*,4)}) =v_{4,2}x^2 + v_{4,1}x+v_{4,0}\\
\end{align*}
```

And the following 4 polynomials from matrix $\mathbf{O}$:

```math
\begin{align*}
w_1(x) = \mathcal{L}(\mathbf{O}_{(*,1)}) =w_{1,2}x^2 + w_{1,1}x+w_{1,0}\\
w_2(x) = \mathcal{L}(\mathbf{O}_{(*,2)}) =w_{2,2}x^2 + w_{2,1}x+w_{2,0}\\
w_3(x) = \mathcal{L}(\mathbf{O}_{(*,3)}) =w_{3,2}x^2 + w_{3,1}x+w_{3,0}\\
w_4(x) = \mathcal{L}(\mathbf{O}_{(*,4)}) =w_{4,2}x^2 + w_{4,1}x+w_{4,0}\\
\end{align*}
```

Again, the QAP for our example is:

```math
\sum_{i=1}^4a_iu_i(x)\sum_{i=1}^4a_iv_i(x) = \sum_{i=1}^4a_iw_i(x) + h(x)t(x)
```

And since the R1CS has 3 constraints, and we are interpolating with the set $x = [1, 2, 3]$, then we know that $t(x)$ is:

```math
t(x) = (x - 1)(x - 2)(x - 3)
```

And by definition, $h(x)$ is:

```math
h(x) = \frac{\sum_{i=1}^4a_iu_i(x)\sum_{i=1}^4a_iv_i(x) - \sum_{i=1}^4a_iw_i(x)}{t(x)}
```

## Degree of Polynomials in the QAP wrt the Size of the R1CS
We can make a couple of general observations about the degrees of the polynomials derived from the R1CS.
- By Lagrange interpolation, the degree of polynomials $u(x)$ and $v(x)$ can be at most degree $= n - 1$ because they were interpolated over $n$ points, where $n$ is the number of rows (constraints) in the R1CS.

- The degree of polynomial $w(x)$ can be as low as degree $= 0$ if the sum of its polynomials $w_1(x) + w_2(x) + ... + w_m(x)$, where $m$ is number of columns, adds up to the zero polynomial. That is, the coefficients additively cancel each other out.

- $t(x)$ is degree $n$ by definition.

- Multiplying polynomials adds their degrees together, and dividing polynomials subtract their degrees.

Therefore, $h(x)$ will be at most degree $\le n-2$ because from the QAP formula:

```math
\underbrace{n-1}_{degree \ u(x)} + \underbrace{n-1}_{degree \ v(x)} - \underbrace{n}_{degree \ t(x)} = \underbrace{n - 2}_{degree \ h(x)}
```

The addition come from the multiplication of polynomials $u(x)$ and $v(x)$, and the subtraction comes from the division with polynomial $t(x)$.

## Expanding the Terms
If we expand the sums from the above example, we get the following:

```math
\begin{align*}
\sum_{i=1}^4 a_iu_i(x) 
&= a_1(u_{1,2}x^2 + u_{1,1}x + u_{1,0}) + a_2(u_{2,2}x^2 + u_{2,1}x + u_{2,0}) + a_3(u_{3,2}x^2 + u_{3,1}x + u_{3,0}) + a_4(u_{4,2}x^2 + u_{4,1}x + u_{4,0})
\\
&= (a_1u_{1,2} + a_2u_{2,2} + a_3u_{3,2} + a_4u_{4,2})x^2 + (a_1u_{1,1} + a_2u_{2,1} + a_3u_{3,1} + a_4u_{4,1})x + (a_1u_{1,0} + a_2u_{2,0} + a_3u_{3,0} + a_4u_{4,0})
\\
&= u_{2a}x^2 + u_{1a}x + u_{0a}
\\

\sum_{i=1}^4 a_iv_i(x) 
&= a_1(v_{1,2}x^2 + v_{1,1}x + v_{1,0}) + a_2(v_{2,2}x^2 + v_{2,1}x + v_{2,0}) + a_3(v_{3,2}x^2 + v_{3,1}x + v_{3,0}) + a_4(v_{4,2}x^2 + v_{4,1}x + v_{4,0})
\\
&= (a_1v_{1,2} + a_2v_{2,2} + a_3v_{3,2} + a_4v_{4,2})x^2 + (a_1v_{1,1} + a_2v_{2,1} + a_3v_{3,1} + a_4v_{4,1})x + (a_1v_{1,0} + a_2v_{2,0} + a_3v_{3,0} + a_4v_{4,0})
\\
&= v_{2a}x^2 + v_{1a}x + v_{0a}
\\

\sum_{i=1}^4 a_iw_i(x) 
&= a_1(w_{1,2}x^2 + w_{1,1}x + w_{1,0}) + a_2(w_{2,2}x^2 + w_{2,1}x + w_{2,0}) + a_3(w_{3,2}x^2 + w_{3,1}x + w_{3,0}) + a_4(w_{4,2}x^2 + w_{4,1}x + w_{4,0})
\\
&= (a_1w_{1,2} + a_2w_{2,2} + a_3w_{3,2} + a_4w_{4,2})x^2 + (a_1w_{1,1} + a_2w_{2,1} + a_3w_{3,1} + a_4w_{4,1})x + (a_1w_{1,0} + a_2w_{2,0} + a_3w_{3,0} + a_4w_{4,0})\\
&= w_{2a}x^2 + w_{1a}x + w_{0a}
\\
\end{align*}
```

In general, the expression $\sum_{i=1}^m a_ip_i(x)$ produces a polynomial with at most the same power (degree) as $p(x)$. But it could be less if, for example: $(a_1w_{1,2} + a_2w_{2,2} + a_3w_{3,2} + a_4w_{4,2})x^2$ added up to $0$.

For convenience, in the final line for each case, we introduced the coefficients: $p_{ia}$, where $_i$ is the power of the coefficient (coefficient power, or the polynomial term of degree $i$), and $_a$ means we combined the polynomials with the witness $\mathbf{a}$.

In each case, since we are adding four degree $= 2$ polynomials, we will still get a degree $= 2$ polynomial.

To summarize the above cases, after reducing the above polynomials, we get the following three polynomials that represent $\mathbf{La}$, $\mathbf{Ra}$, and $\mathbf{Oa}$ respectively:

```math
\begin{align*}
\mathbf{La} &\rightarrow \sum_{i = 1}^{4}a_iu_i(x) = u_{2a}x^2 + u_{1a}x + u_{0a}
\\
\mathbf{Ra} &\rightarrow \sum_{i = 1}^{4}a_iv_i(x) = v_{2a}x^2 + v_{1a}x + v_{0a}
\\
\mathbf{Oa} &\rightarrow \sum_{i = 1}^{4}a_iw_i(x) = w_{2a}x^2 + w_{1a}x + w_{0a}
\end{align*}
```

## Combining a Trusted Setup with a QAP
We can now apply the [structured reference string (SRS) from the trusted setup](https://rareskills.io/post/trusted-setup) to evaluate the polynomials.

In the previous chaper, we established the general notation:

```math
\Omega_i = \tau^iG_1 \\
\Theta_i = \tau^iG_2
```

Given the SRS:

```math
[\Omega_2, \Omega_1, G_1], \ [\Theta_2, \Theta_1, G_2] 
\quad \text{where}\quad 
\begin{cases}\Omega_i \in \mathbb{G_1} \\ \Theta_i \in \mathbb{G_2} \end{cases}
```

Which was computed during the trusted setup as:

```math
[\Omega_2, \Omega_1, G_1] = [\tau^2 G_1, \tau G_1, G_1]
\\
[\Theta_2, \Theta_1, G_2] = [\tau^2 G_2, \tau G_2, G_2]
```

We can thus compute:

```math
\begin{align*}
[A]_1 &= \sum_{i=1}^{4}a_iu_i(\tau) = \langle[u_{2a}, u_{1a}, u_{0a}], [\Omega_2, \Omega_1, G_1]\rangle
\\
[B]_2 &= \sum_{i=1}^{4}a_iv_i(\tau) = \langle[v_{2a}, v_{1a}, v_{0a}], [\Theta_2, \Theta_1, G_1]\rangle
\\
[C]_1 &= \sum_{i=1}^{4}a_iw_i(\tau) = \langle[w_{2a}, w_{1a}, w_{0a}], [\Omega_2, \Omega_1, G_1]\rangle
\end{align*}
```

Note that $u_i(\tau)$, $v_i(\tau)$, $w_i(\tau)$ mean that the polynomials are already evaluated using the SRS generated from $\tau$ in the trusted setup, it does not mean "plug in $\tau$ and evaluate the polynomials". In other words, $u_i(\tau)$, $v_i(\tau)$, and $w_i(\tau)$ are already scalar values but hidden as an elliptic curve points. It goes without saying that elliptic curve points $[A]_1, [C]_1 \in \mathbb{G_1}$, and elliptic curve point $[B]_2 \in \mathbb{G_2}$.

Since $\tau$ should have been destroyed after the trusted setup, the value for $\tau$ should be unknown.

We have computed most of the QAP using the SRS, but we have not computed $h(x)t(x)$ yet:

```math
\underbrace{\sum_{i = 1}^{4}a_iu_i(x)}_{[A]_1} 
\underbrace{\sum_{i=1}^{4}a_iv_i(x)}_{[B]_2} = 
\underbrace{\sum_{i=1}^{4}a_iw_i(x)}_{[C]_1} + 
\underbrace{h(x)t(x)}_{???}
```

FYI, when we write $[\sum a_iu_i(\tau)]_1$, or for the matter any $[A]_1$ or $[p(\tau)]$, we mean an elliptic-curve point that serves as a commitment to that field value/evaluation at the secret $\tau$. TLDR, a commitment.

## Computing $h(x)t(x)$
By definition, we know that $t(x)$ has degree $= n$. Thus for our example, we know that the degree of $t(x) = 3$.

We also know that from the QAP formula, the degree of $h(x) = n - 2$. Which means for our example, we know that the defree of $h(x) = 1$.

If we multiply $t(x)$ and $h(x)$ together, we could get up to a degree $= 4$ polynomial, which is more than what the powers of tau ceremony (generation of the SRS) provides. Instead, the powers of tau ceremony must now be adjusted to provide a structured reference string for $h(x)t(x)$.

The person doing the trusted setup knows that the polynomial $t(x) = (x - 1)(x - 2)...(x-n)$. Thus $t(x)$ is considered public.

However, the polynomial $h(x)$ is computed by the prover, and it changes based on the values of the witness $\mathbf{a}$; and so $h(x)$ cannot be known during the trusted setup. Which means $h(x)$ is considered private.

Also note that we cannot evaluate $h(\tau)$ and $t(\tau)$ separately (using a SRS) and then put them in a bilinear pairing together. This would not result in a $\mathbb{G_1}$ element which is what we ultimately need - as $[h(\tau)t(\tau)]_1$, for Groth16.

This means we simply cannot compute $[h(\tau)]_1$ and $[t(\tau)]_2$ separately using an SRS (like in the above section); and then pair them as $[h(\tau)]_1 \bullet [t(\tau)]_2$ to verify that it is equivalent to $e(G_1, G_2)^{h(\tau)t(\tau)}$. As this results in an element in $\mathbb{G_T}$. Also, consider that $\tau$ is always unknown.

Remember that $h(\tau)t(\tau)$ needs to be added to $[C]_1$ as defined by the QAP formula. There is no structure-preserving way to go from $\mathbb{G_T} \rightarrow \mathbb{G_1}$; so the SRS must be adjusted in a way to "bake" $t(\tau)$ into the $\mathbb{G_1}$ side of the SRS, and allow the prover to use only the SRS and only the coefficients of $h(x)$ to form the commitment $[h(\tau)t(\tau)]_1$, without having the prover ever knowing $\tau$ or $t(\tau)$.

This will be clearer in a bit.

## SRS for Polynomial Products, such as $h(x)t(x)$

Observe that the following computations all result in the same value:
- The polynomial $h(x)t(x)$ evaluated at $u$, or: $(h(x)t(x))(u)$
    - Multiply $h(x)$ and $t(x)$, and then evaluate at $u$
- $h(u)$ multiplied by $t(u)$, or: $h(u)t(u)$
    - Evaluate $h$ at $u$, evaluate $t$ at $u$, and then multiply
- $h(x)$ multiplied by the evaluataion of $t(u)$, then evaluated at $u$, or: $(h(x)t(u))(u)$
    - Evaluate $t$ at $u$, then multiply the resulting scalar with $h(x)$, then evaluate at $u$

We will use the third method: $(h(x)t(u))(u)$, to compute the polynomial $h(\tau)t(\tau)$.

Suppose, without loss of generality, that:

```math
\begin{align*}
h(x) &= 3x^2 + 6x + 2 \\[4pt]
t(u) &= 4
\end{align*}
```

Then computing $h(x)t(u)$ would yield:

```math
\begin{align*}
h(x)t(u) &= (3x^2 + 6x + 2) \cdot 4 \\
&= 12x^2 + 24x + 8
\end{align*}
```

If we then plug $u$ into $12x^2 + 24x + 8$, that would give us the polynomial $h(u)t(u)$.

However, evaluating this polynomial at $\tau$ would requrie the prover to know the value of $\tau$, i.e. plugging $\tau$ into $h(u)t(u)$.

The key insight here, is that we can break the polynomial down and structure the computation of $h(u)t(u)$ as:

```math
\begin{align*}
h(u)t(u) &= 12u^2 + 24u + 8 \\[4pt]
&= \langle [3, 6, 2], [4u^2, 4u, 4] \rangle
\end{align*}
```

If the trusted setup provides $[4u^2, 4u, 4]$, and the prover provides $[3, 6, 2]$, then the prover would be able to compute $h(u)t(u)$ without knowing what $u$ is, since everything involving $u$ is already in the right vector of the inner product.

## SRS for $h(\tau)t(\tau)$

Recall that $t(x)$ has degree $= n$, which is the number of constraints (rows) we have in the R1CS. And $h(x)$ has degree $\le n - 2$ by definition of the QAP. This means we can expect the polynomial $h(x)t(x)$ to be degree $= n + (n-2) = 2n - 2$.

In zk-SNARKs like Groth16 and PLONK, the prover needs to compute $[h(\tau)t(\tau)]_1$ (a commitment in $\mathbb{G_1}$) without knowing $\tau$, by using the SRS from the trusted setup.

However, the prover only needs to compute $h(x)t(x)$ evaluated at $\tau$ without actually knowing what $\tau$ is (i.e, computing $h(\tau)t(\tau)$ as a single field element (scalar), then committed to $\mathbb{G_1}$ as $[h(\tau)t(\tau)]_1$).

To allow this, an SRS can provide precomputed $\mathbb{G_1}$ points (just like how we observed in the trusted setup - where $\Omega_i = \tau^i G_1$, and $\Theta_i = \tau^i G_2$) to allow the prover to construct $[h(\tau)t(\tau)]_1$. We use terms of the following (similar) form:

```math
\Upsilon_i = \tau^i \cdot t(\tau) \cdot G_1 \quad \text{where} \quad i = [0, 1, 2, ..., n-2]
```

It goes without saying that $t(\tau)$ is a scalar since $t(x)$ is already evaluated at $\tau$ when the SRS was created.

Note that, somewhat confusingly, a polynonial of degree $k$ will have $k + 1$ terms. Since $h(x)$ has the degree $= n-2$, then this means $h(x)$ will have $(n - 2 + 1) = n - 1$ terms. Therefore we generate $n - 1$ evaluations (terms) for $h(x)$ - a polynomial of degree $n - 2$.

```math
[\Upsilon_{n-2}, \ \Upsilon_{n-3}, \ ..., \ \Upsilon_2, \ \Upsilon_1, \ \Upsilon_0] = [\tau^{n-2}t(\tau)G_1, \ \tau^{n-3}t(\tau)G_1, \ ..., \ \tau^{2}t(\tau)G_1, \ \tau t(\tau)G_1, \ t(\tau)G_1]
```

Recall that we have to construct the SRS in successsive powers of the polynomial terms in descending order. Here, $\Upsilon_{n-2}$ represents the $(n-1)^{\text{th}}$ term, and $\Upsilon_0$ represents the last term of the polynomial (the zero-th term i.e. the constant).

To use the SRS to compute $[h(\tau)t(\tau)]_1$, the prover performs the following inner product:

```math
h(\tau)t(\tau) = \langle[h_{n-2}, h_{n-3}, ..., h_{2}, h_{1}, h_{0}], [\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{2}, \Upsilon_{1}, \Upsilon_{0}] \rangle
```

Where $h_{n-2}, h_{n-3}, ..., h_{2}, h_{1}, h_{0}$ are the coefficients of polynomial $h(x)$.

And just like during the trusted setup, $h(\tau)t(\tau)$ evaluates to a scalar that will be commited as an elliptic curve point.

```math
\begin{align*}
h(\tau)t(\tau) &= \langle[h_{n-2}, h_{n-3}, ..., h_{2}, h_{1}, h_{0}], [\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{2}, \Upsilon_{1}, \Upsilon_{0}] \rangle 
\\[4pt]
&= h_{n-2}\Upsilon_{n-2} + h_{n-3}\Upsilon_{n-3} + ..., + h_{2}\Upsilon_{2} + h_{1}\Upsilon_{1} + h_{0}\Upsilon_{0}
\\[4pt]
&= h_{n-2}\tau^{n-2}t(\tau)G_1 + h_{n-3}\tau^{n-3}t(\tau)G_1 + ... + h_{2}\tau^{2}t(\tau)G_1 + h_{1}\tau t(\tau)G_1 + h_{0}t(\tau)G_1
\\[4pt]
&= [h(\tau)t(\tau)]_1
\end{align*}
```

## Evaluating a QAP on a Trusted Setup

Now we can tie everything together. Suppose we have an R1CS with matrices of $n$ rows and $m$ columns. From this, we can apply Lagrange interpolation to convert it into a QAP.

```math
\sum_{i = 1}^{m}a_iu_i(x) \sum_{i = 1}^{m}a_iv_i(x) = \sum_{i = 1}^{m}a_iw_i(x) + h(x)t(x)
```

We establish that our R1CS has $n$ constraints, and therefore we will be interpolating over $x = [1, 2, ..., n]$. And by Lagrange interpolation, each sum term will yield a polynomial of degree $=n - 1$ (because a Lagrange interpolating polynomial will have degree $\le n - 1$ by definition, where $n$ is the number of points being interpolated).

We also know that $t(x)$ will have degree $= n$ (since there are $n$ constraints in the R1CS); and that by definition of the QAP formula, $h(x)$ will have degree $= n - 2$.

A trusted setup generates a random field element: $\tau$, and computes the following SRS:

```math
\begin{align*}
[\Omega_{n-1}, \Omega_{n-2}, ..., \Omega_{1}, G_1] &= [\tau^{n-1}G_1, \tau^{n-2}G_1, ..., \tau G_1, G_1] 
\\[4pt]
[\Theta_{n-1}, \Theta_{n-2}, ..., \Theta_{1}, G_2] &= [\tau^{n-1}G_2, \tau^{n-2}G_2, ..., \tau G_2, G_2]
\\[4pt]
[\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{1}, \Upsilon_{0}] &= [\tau^{n-2}t(\tau)G_1, \tau^{n-3}t(\tau)G_1, ..., \tau t(\tau)G_1, t(\tau)G_1]
\end{align*}
```

Note that each SRS will be used to evaluate different polynomials in the QAP. Also, each SRS needs to have enough terms to accomodate the polynomials in the QAP.

```math
\begin{align*}
\sum_{i = 1}^{m}a_iu_i(x) &\stackrel{\text{evaluated with}}{\Longleftarrow} [\Omega_{n-1}, \Omega_{n-2}, ..., \Omega_{1}, G_1]
\\[12pt]
\sum_{i = 1}^{m}a_iv_i(x) &\stackrel{\text{evaluated with}}{\Longleftarrow} [\Theta_{n-1}, \Theta_{n-2}, ..., \Theta_{1}, G_2]
\\[12pt]
\sum_{i = 1}^{m}a_iw_i(x) &\stackrel{\text{evaluated with}}{\Longleftarrow} [\Omega_{n-1}, \Omega_{n-2}, ..., \Omega_{1}, G_1]
\\[12pt]
h(x)t(x) &\stackrel{\text{evaluated with}}{\Longleftarrow} [\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{1}, \Upsilon_{0}]
\end{align*}
```

Then, the trusted setup destroys $\tau$, and publishes the structured reference strings:

```math
\Bigl( [\Omega_2, \Omega_1, G_1], \ [\Theta_2, \Theta_1, G_2], \ [\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{1}, \Upsilon_{0}] \Bigl)
```

With the SRS, the prover evaluates the components of the QAP and commits them as elliptic curve points as follows:

```math
\underbrace{\sum_{i = 1}^{m}a_iu_i(x)}_{A} \underbrace{\sum_{i = 1}^{m}a_iv_i(x)}_{B} = \underbrace{\sum_{i = 1}^{m}a_iw_i(x) + h(x)t(x)}_{C}
```

```math
\begin{align*}
[A]_1 &= \sum_{i = 1}^{m}a_iu_i(x) = \langle[u_{(n-1)a}, u_{(n-2)a}, ..., u_{1a}, u_{0a}],[\Omega_{n-1}, \Omega_{n-2}, ..., \Omega_{1}, G_1]\rangle
\\[12pt]
[B]_2 &= \sum_{i = 1}^{m}a_iv_i(x) = \langle[v_{(n-1)a}, v_{(n-2)a}, ..., v_{1a}, v_{0a}],[\Theta_{n-1}, \Theta_{n-2}, ..., \Theta_{1}, G_2] \rangle
\\[12pt]
[C]_1 &= \sum_{i = 1}^{m}a_iw_i(x) + h(x)t(x) \\ &= \langle [w_{(n-1)a}, w_{(n-2)a}, ..., w_{1a}, w_{0a}],[\Omega_{n-1}, \Omega_{n-2}, ..., \Omega_{1}, G_1] + [h_{n-2}, h_{n-3}, ..., h_{1}, h_{0}],[\Upsilon_{n-2}, \Upsilon_{n-3}, ..., \Upsilon_{1}, \Upsilon_{0}]\rangle
\end{align*}
```

The prover then publishes: $([A]_1, [B]_2, [C]_1)$, and the verifier can check that:

```math
[A]_1 \bullet [B]_2 \stackrel{?}{=} [C]_1 \bullet G_2
```

<hr>

Observe that in the structured reference strings, there are two $\Omega$ terms provided and two $\Theta$ terms provided. There is a good reason for this.

We know that the SRS provides precomputed ellptic curve points in $\mathbb{G_1}$ and $\mathbb{G_2}$, which will allow the prover to commit polynomials evaluated at the secret scalar $\tau$ (without knowing $\tau$), and the verifier to check these commitments using bilinear pairings.

Many zk-SNARKs (like Groth16) require the prover to compute quadratic combinations of polynomials, for example: $a(x) = a_2x^2 + a_1x + a_0$. With the above SRS, the prover can commit to the polynomial $a(x)$ in $\mathbb{G_1}$ evaluated at the secret scalar $\tau$ without knowing $\tau$ itself.

```math
[a(\tau)]_1 = a_2\Omega_2 + a_1\Omega_1 + a_0G_1
```

With the same SRS, a polynomial $b(x) = b_2x^2 + b_1x + b_0$ can be commited and evaluated in $\mathbb{G_2}$ with $\tau$ already obscured.

```math
[b(\tau)]_2 = b_2\Theta_2 + b_1\Theta_1 + b_0G_2
```

Even for the verifier, without having to ever learn what $\tau$ was, the verifier can use the published $\Omega$ and $\Theta$ terms within bilinear pairings to verify relationships between commited polynomials.

```math
e([a(\tau)]_1, [b(\tau)]_2) \stackrel{?}{=} e\Bigl((a_2\Omega_2 + a_1\Omega_1 + a_0G_1), \ (b_2\Theta_2 + b_1\Theta_1 + b_0G_2)\Bigr)
```

The key here is, nobody knows what $\tau$ is, and if we were only given $[\Omega_1, G_1]$ and $[\Theta_1, G_2]$ in the SRS (one of each term instead of two), by the discrete logarithm problem there is no efficient way to recover $\tau$ from $\tau G_1$ or $\tau G_2$. Without knowing $\tau$ it is impossible to compute $\tau^2$ and thus $\tau^2G_1$ or $\tau^2G_2$.

Also remember, that elliptic curve operations only allow point addition: $[a]_1 + [b]_1 = [a + b]_1$, and scalar multiplication (which is repeated addition in itself): $k \cdot [a]_1 = [k \cdot a]_1$. It does not define the multiplication of two elliptic curve points. Thus we cannot compute $[\tau^2]_1$ from $[\tau]_1$ alone.

<hr>

