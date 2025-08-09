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

For a matrix $\mathbf{L}$, let $\mathbf{L}_{(*, j)}$ denote all rows (*) and the $j$-th column of the matrix.

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

Therefore, $h(x)$ will be at most degree $= n-2$ because from the QAP formula:

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
