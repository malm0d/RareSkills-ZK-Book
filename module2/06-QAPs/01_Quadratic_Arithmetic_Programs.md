# Quadratic Arithmetic Programs
https://www.rareskills.io/post/quadratic-arithmetic-program

A quadratic arithmetic program (QAP) is an [arithmetic circuit](https://rareskills.io/post/arithmetic-circuit), specifically a [Rank 1 Constraint System](https://rareskills.io/post/rank-1-constraint-system) (R1CS) represented as a set of polynomials. A QAP is derived using Lagrange interpolation on a R1CS.

Unlike an R1CS where testing for equality takes $\mathcal{O}(n)$ time, a QAP can be tested for equality in $\mathcal{O}(1)$ time through the Schwartz-Zippel Lemma.

## Key Idea
In the previous chapter on the Schwartz-Zippel Lemma, we saw that we can test for equality between two vectors in $\mathcal{O}(1)$ time by converting them into Lagrange interpolating polynomials, and then running the Schwartz-Zippel Lemma test on those polynomials. (To clarify, the test is in $\mathcal{O}(1)$ time, but converting vectors to Lagrange interpolating polynomials creates overhead).

An R1CS is composed of entirely vector operations:

```math
(\mathbf{L} \cdot \mathbf{a}) \circ (\mathbf{R} \cdot \mathbf{a}) \stackrel{?}{=} (\mathbf{O} \cdot \mathbf{a})
```

Where each R1CS constraint matrix ($\mathbf{L}$, $\mathbf{R}$, $\mathbf{O}$) performs a dot product with the witness $\mathbf{a}$, which yield vectors $\mathbf{La}$, $\mathbf{Ra}$, and $\mathbf{Oa}$ . And the $\circ$ operator is the hadamard product between $\mathbf{La}$ and $\mathbf{Ra}$.

We aim to test if

```math
\mathbf{La} \circ \mathbf{Ra} \stackrel{?}{=} \mathbf{Oa}
```

holds $\mathcal{O}(1)$ time instead of $\mathcal{O}(n)$ time, where $n$ is the number of rows in the constraint matrices $\mathbf{L}$, $\mathbf{R}$, $\mathbf{O}$.

However, we need to understand some key properties of the relationship between vectors and the Lagrange interpolating polynomials that represent them.

Note that all math in this chapter is assumed to be in a FINITE FIELD. The $\mod p$ notation will be skipped for succinctness.

## The Homomorphisms Between Vector Addition and Polynomial Addition

### Vector Addition is Homomorphic to Polynomial Addition
This is really important to keep in mind.

If we take two vectors $\mathbf{v}$ and $\mathbf{w}$, interpolate them as Lagrange interpolating polynomials each, and then add the polynomials together, we would get the SAME polynomial compared to if we added vectors $v$ and $w$ together first and then interpolate that sum vector with Lagrange interpolation.

That is, using the common set of $x$ values: $[1, 2, ..., n]$, where $n$ is the length of vector $\mathbf{v}$, let $\mathcal{L}(\mathbf{v})$ be the Lagrange interpolating polynomial resulting from the interpolation of vector $\mathbf{v}$, and let $\mathcal{L}(\mathbf{w})$ be the Lagrange interpolating polynomial resulting from the interpolation of vector $\mathbf{w}$. The following is true:

```math
\mathcal{L}(\mathbf{v}) + \mathcal{L}(\mathbf{w}) = \mathcal{L}(\mathbf{v} + \mathbf{w})
```

In other words, the sum of the polynomials resulting from interpolating vectors $\mathbf{v}$ and $\mathbf{w}$ separately is the same as the polynomial resulting from interpolating the sum of vectors $\mathbf{v}$ and $\mathbf{w}$.

### Worked Example
Let the polynomial $f_1(x) = x^2$ and the polynomial $f_2(x) = x^3$.

$f_1(x)$ interpolates the points: $(1,1), (2,4), (3,9)$, or another way to see it - the vector $[1, 4, 9]$. 

And we assume that $f_2(x)$ interpolates the vector $[1, 8, 27]$.

The sum of two vectors is obtained by element-wise addition. If we took the sum of the two vectors, we would get: $[2, 12, 36]$.

If we also took the sum of the two polynomials, we'd get:

```math
f_3(x) = f_1(x) + f_2(x) = x^3 + x^2
```

And it is clear, over the common set of $x$ values, that the sum polynomial $f_3(x)$ interpolates the vector $[2, 12, 36]$:

```math
\begin{align*}
f_3(1) &= 1 + 1 = 2 \\
f_3(2) &= 8 + 4 = 12 \\
f_3(3) &= 27 + 9 = 36 \\
\end{align*}
```

### Testing the Math in Python
Unit testing a proposed mathematical identity like: $\mathcal{L}(\mathbf{v}) + \mathcal{L}(\mathbf{w}) = \mathcal{L}(\mathbf{v} + \mathbf{w})$, doesnt make it true. But it illustrates what is happening.

```python
import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GF(np.array([1, 2, 3]))

def L(v):
    return galois.lagrange_poly(x_common, v)

# Arbitray vectors
# Note we are dealing with field elements of GF(17)
v1 = GF(np.array([4, 8, 2]))
v2 = GF(np.array([1, 6, 12]))
v3 = GF(np.array([7, 4, 10]))
v4 = GF(np.array([3, 15, 9]))

assert L(v1 + v2) == L(v1) + L(v2)
assert L(v3 + v4) == L(v3) + L(v4)
assert L(v1 + v4) == L(v1) + L(v4)
assert L(v2 + v3) == L(v2) + L(v3)
```

### Scalar Multiplication
Let $\lambda$ be a scalar ($\lambda$ is specifically a field element of the finite field), and let $\mathbf{v}$ be an arbitrary vector. Then this means:

```math
\mathcal{L}(\lambda\mathbf{v}) = \lambda \mathcal{L}(\mathbf{v})
```

### Worked Example
Suppose we have the vector $ \mathbf{v} = [3, 6, 11]$, and over the common set of $x$ values, the polynomial that interpolates the vector is $f(x) = x^2 + 2$.

If we multiply the vector by $3$, i.e. $3\mathbf{v}$, we get: $[9, 18, 33]$.

And when we run Lagrange interpolation on the vector $3\mathbf{v}$:

```python
from scipy.interpolate import lagrange

x_common = [1, 2, 3]
3v = [9, 18, 33]

print(lagrange(x_values, y_values))
#    2
# 3 x + 6
# (i.e. 3x^2 + 6)
```

The Lagrange interpolating polynomial for $3\mathbf{v}$ is: $3x^2 + 6$, which is in fact: $3(x^2 + 2) = 3f(x)$

We can be even more explicit in demonstrating that $\mathcal{L}(\lambda\mathbf{v}) = \lambda \mathcal{L}(\mathbf{v})$:

```python
import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GP(np.array([1, 2, 3]))

def L(v):
    return galois.lagrange_poly(x_common, v)

# Arbitrary vector
v = GF(np.array([4, 8, 2]))

# Arbitray constant
lambda_ = GF(15)

assert L(lambda_ * v) == lambda_ * L(v)
```

The important idea here is: scalar multiplication of a vector is (repeated) vector addition.

It also means that scalar multiplication of a vector corresponds to scalar multiplication of the interpolated polynomial, but it DOES NOT necessarily correspond to repeated polynomial addition in a finite field. Rather it is the coefficient-wise scalar multiplication of the polynomial in the finite field. This scalar mulitplication is a field multiplication, not repeated addition.

To give an idea:

```python
import galois
import numpy as np

GF = galois.GF(17)
v = GF(np.array([4, 8, 2]))

fx = galois.lagrange_poly(x_common, v)
print(fx)
# 12x^2 + 2x + 7

c = GF(5)
cfx = c * fx # Scalar multiplication: c * f(x)
print(cfx)
# 9x^2 + 10x + 1
```

It may work if `c` is a small positive integer (interpreted in the finite field), but not necessarily for any `c` $\in \mathbb{F}$.

### Scalar Multiplication IS REALLY Vector Addition
When we say "multiply a vector by 3", we are really saying "add the vector to itself three times". Since we are only working in finite fields, we don't concern outselves with the interpretation of scalars such as "0.5".

We can think of vectors in a finite field under element-wise addition as a group, and we can also think of polynomials in a finite field under addition as a [group](https://rareskills.io/post/group-theory) as well.

Recall that a group must have a closed binary operator, its binary operator is associative, it has an identity element, and every element in the set has an inverse.

Vectors in a finite field under addition is a group because:

- Closure: Adding two vectors (element-wise) yields another vector.
- Associativity: Follows the associativity of addition in a finite field.
- Identity element: The zero vector $[0, 0, ..., 0]$.
- Inverse elements: The inverse of $[a_1, ..., a_n]$ is $[-a_1, ..., -a_n]$.

Polynomials in a finite field under addition is also a group because:

- Closure: Adding two polynomials yields another polynomial.
- Associativity: Follows the associativity of addition in a finite field.
- Identity element: The zero polynomial $0$.
- Inverse elements: The inverse of $f(x) = a_0 + a_1x + ... \ $, is $-f(x) = -a_0 + (-a_1)x + ... \ $.

The most important takeaway from this chapter is this:

**The group of vectors in a finite field under addition is homomorphic to the group of polynomials in a finite field under addition.**

- Lagrange interpolation ($\mathcal{L}$) functions as a linear homomorphism for vectors and polynomials. This means:
    
    - $\mathcal{L}(\mathbf{v_1} + \mathbf{v_2}) = \mathcal{L}(\mathbf{v_1}) + \mathcal{L}(\mathbf{v_2}) \quad$ is addition-preserving
    - $\mathcal{L}(\lambda\mathbf{v}) = \lambda\mathcal{L}(\mathbf{v}) \quad$ is scalar-multiplication preserving
    - (i.e. the homomorphism preserves linear operations (addition/scalar multiplication))

This is critical because equality testing with vectors takes $\mathcal{O}(n)$ time, but equality testing with **polynomials** takes $\mathcal{O}(1)$ time.

FYI: vector addition and polynomial addition are isomorphic (structurally identical, so this is one case where the homomorphism is bi-directional).

We know that testing for R1CS equality takes $\mathcal{O}(n)$ time since it requires comparing all $n$ constraints. Thus, we can leverage the homomorphism between vectors in a finite field under addition and polynomials in a finite field under addition, in order to test for R1CS equality in $\mathcal{O}(n)$ time.

This is what a Quadratic Arithmetic Program is.

## A R1CS in Polynomials
Consider that standard matrix multiplication between a rectangular matrix ($n \times m$) and a vector can be written in terms of **vector addition and scalar multiplication**.

For example, if we have a $3 \times 4$ matrix $\mathbf{A}$, and a $4$ dimensional vector $\mathbf{v}$, we write matrix multiplication as

```math
\mathbf{A} \cdot \mathbf{v} =
\begin{bmatrix}
a_{1, 1} & a_{1, 2} & a_{1, 3} & a_{1, 4} \\
a_{2, 1} & a_{2, 2} & a_{2, 3} & a_{2, 4} \\
a_{3, 1} & a_{3, 2} & a_{3, 3} & a_{3, 4}
\end{bmatrix} \cdot
\begin{bmatrix}
v_{1} \\ v_{2} \\ v_{3} \\ v_{4}
\end{bmatrix}
```

And to get the resulting matrix, we interpret each entry (row) of the resulting matrix as an inner product (generalization of dot product) between each row of matrix $\mathbf{A}$ and vector $\mathbf{v}$, i.e.

```math
\mathbf{A} \cdot \mathbf{v} =
\begin{bmatrix}
a_{1, 1} \cdot v_{1} + a_{1, 2} \cdot v_{2} + a_{1, 3} \cdot v_{3} + a_{1, 4} \cdot v_{4} \\[4pt]
a_{2, 1} \cdot v_{1} + a_{2, 2} \cdot v_{2} + a_{2, 3} \cdot v_{3} + a_{2, 4} \cdot v_{4}\\[4pt]
a_{3, 1} \cdot v_{1} + a_{3, 2} \cdot v_{2} + a_{3, 3} \cdot v_{3} + a_{3, 4} \cdot v_{4}
\end{bmatrix}
```

**HOWEVER**, we could, instead, think of splitting matrix $\mathbf{A}$ into a series of vectors as such:

```math
\mathbf{A} = 
\begin{bmatrix}
a_{1, 1} \\ a_{2, 1} \\ a_{3, 1}
\end{bmatrix}
,
\begin{bmatrix}
a_{1, 2} \\ a_{2, 2} \\ a_{3, 2}
\end{bmatrix}
,
\begin{bmatrix}
a_{1, 3} \\ a_{2, 3} \\ a_{3, 3}
\end{bmatrix}
,
\begin{bmatrix}
a_{1, 4} \\ a_{2, 4} \\ a_{3, 4}
\end{bmatrix}
```

And multiply each of these vectors by a scalar from the vector $\mathbf{v}$:

```math
\mathbf{A} \cdot \mathbf{v} =
\begin{bmatrix}
a_{1, 1} \\ a_{2, 1} \\ a_{3, 1}
\end{bmatrix}
\cdot v_1
+
\begin{bmatrix}
a_{1, 2} \\ a_{2, 2} \\ a_{3, 2}
\end{bmatrix}
\cdot v_2
+
\begin{bmatrix}
a_{1, 3} \\ a_{2, 3} \\ a_{3, 3}
\end{bmatrix}
\cdot v_3
+
\begin{bmatrix}
a_{1, 4} \\ a_{2, 4} \\ a_{3, 4}
\end{bmatrix}
\cdot v_4
```

The matrix multiplication between $\mathbf{A}$ and $\mathbf{v}$ is now expressed purely in terms of vector addition and scalar multiplication.

We established earlier that the group of vectors in a finite field under addition is homomorphic to the group of polynomials in a finite field under addition. Because of this homomorphism, we can express the computation of $\mathbf{A} \cdot \mathbf{v}$ in terms of (lagrange interpolating) polynomials that represent the vectors.

## Succinctly Testing that $\mathbf{Av_1} = \mathbf{Bv_2}$
Suppose that we have matrices $\mathbf{A}$ and $\mathbf{B}$ such that:

```math
\mathbf{A} =
\begin{bmatrix}
6 & 3 \\ 4 & 7
\end{bmatrix} \quad \text{and} \quad 
\mathbf{B} =
\begin{bmatrix}
3 & 9 \\ 12 & 6
\end{bmatrix}
```

And we have vectors $\mathbf{v_1}$ and $\mathbf{v_2}$ as:

```math
\mathbf{v_1} =
\begin{bmatrix}
2 \\ 4
\end{bmatrix} \quad \text{and} \quad 
\mathbf{v_2} =
\begin{bmatrix}
2 \\ 2 
\end{bmatrix}
```

We want to test that the following is true:

```math
\mathbf{Av_1} = \mathbf{Bv_2}
```

Technically, we could carry out regular matrix arithmetic, but the final check for equality will require $n$ comparisons, where $n$ is the number of rows in matrices $\mathbf{A}$ and $\mathbf{B}$. This would require $\mathcal{O}(n)$ time. However, we want to do the equality check in $\mathcal{O}(1)$ time.

First, we represent the matrix multiplication of $\mathbf{Av_1}$ and $\mathbf{Bv_2}$ as a group of vectors under addition:

```math
\mathbf{A} = \Biggl\{
\begin{bmatrix}
6 \\ 4 
\end{bmatrix}, 
\begin{bmatrix}
3 \\ 7 
\end{bmatrix} \Biggr\}
\quad \text{and} \quad
\mathbf{B} = \Biggl\{
\begin{bmatrix}
3 \\ 12 
\end{bmatrix}, 
\begin{bmatrix}
9 \\ 6 
\end{bmatrix} \Biggr\}
```

Next, we aim to find the homomorphic equivalent of the following vector equation in the polynomial group:

```math
\mathbf{Av_1} \stackrel{?}{=} \mathbf{Bv_2}
```

```math
\begin{bmatrix}
6 \\ 4 
\end{bmatrix} \cdot 2 \ + \
\begin{bmatrix}
3 \\ 7 
\end{bmatrix} \cdot 4 \ \stackrel{?}{=}
\begin{bmatrix}
3 \\ 12 
\end{bmatrix} \cdot 2 \ + \
\begin{bmatrix}
9 \\ 6 
\end{bmatrix} \cdot 2
```

We convert (interpolate) each of the vectors derived from matrices $\mathbf{A}$ and $\mathbf{B}$ to polynomials using **Lagrange interpolation** over the common set of $x$ values: $[1, 2]$:

```math
\underbrace{\begin{bmatrix} 6 \\ 4 \end{bmatrix}}_{p_{1}(x)} \,\cdot 2
\;+\;
\underbrace{\begin{bmatrix} 3 \\ 7 \end{bmatrix}}_{p_{2}(x)} \,\cdot 4
\;\stackrel{?}{=}\;
\underbrace{\begin{bmatrix} 3 \\ 12 \end{bmatrix}}_{q_{1}(x)} \,\cdot 2
\;=\;
\underbrace{\begin{bmatrix} 9 \\ 6 \end{bmatrix}}_{q_{2}(x)} \,\cdot 2
```

That is, we will compute the following Lagrange interpolating polynomials:
- For $\begin{bmatrix} 6 \\ 4 \end{bmatrix}$, define $p_1(x)$, such that $p_1(1) = 6$ and $p_1(2) = 4$.

- For $\begin{bmatrix} 3 \\ 7 \end{bmatrix}$, define $p_2(x)$, such that $p_2(1) = 3$ and $p_2(2) = 7$.

- For $\begin{bmatrix} 3 \\ 12 \end{bmatrix}$, define $q_1(x)$, such that $q_1(1) = 3$ and $q_1(2) = 12$. 

- For $\begin{bmatrix} 9 \\ 6 \end{bmatrix}$, define $q_2(x)$, such that $q_2(1) = 9$ and $q_2(2) = 6$. 

```python
import galois
import numpy as np

p = 17
GF = galois.GF(p)

x_common = GF(np.array([1, 2]))

def L(v):
    return galois.lagrange_poly(x_common, v)

p1 = L(GF(np.array([6, 4])))
p2 = L(GF(np.array([3, 7])))
q1 = L(GF(np.array([3, 12])))
q2 = L(GF(np.array([9, 6])))

print(p1)
# p1 = 15x + 8 (mod 17)
print(p2)
# p2 = 4x + 16 (mod 17)
print(q1)
# q1 = 9x + 11 (mod 17)
print(q2)
# q2 = 14x + 12 (mod 17)
```

Finally, we can check if the following is true using the **Schwartz-Zippel Lemma**:

```math
p_1(x) \cdot 2 + p_2(x) \cdot 4 \ \stackrel{?}{=} \ q_1(x) \cdot 2 + q_2(x) \cdot 2
```

```python
#continued from above

import random
u = random.randint(0, p)

# Random point: u
tau = GF(u)

# p1(x) * 2 + p2(x) * 4
lhs = p1(tau) * GF(2) + p2(tau) * GF(4)

# q1(x) * 2 + q2(x) * 2
rhs = q1(tau) * GF(2) + q2(tau) * GF(2)

# Assert equality -> true
assert lhs == rhs
```

**The final `assert` statement is able to test if $\mathbf{Av_1} = \mathbf{Bv_2}$ is true by doing a SINGLE comparison instead of $n$ comparisons. Thus achieving work in $\mathcal{O}(1)$ time.**

## R1CS to QAP: Succinctly Testing that $\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}$
Since we know how to test $\mathbf{Av_1} = \mathbf{Bv_2}$ succinctly, then we can also test if $\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}$ succinctly.

Say that matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ are rectangular matrices of dimensions $n \times m$, where $n$ is the number of rows and $m$ is the number of columns.

Since each matrix has $m$ columns, we can break each matrix into $m$ column vectors, and then interpolate those vectors with Lagrange interpolation on the common set of $x$: $[1, 2, ...n]$ in order to get $m$ polynomials for each matrix.

For matrix $\mathbf{L}$:

```math
\begin{align*}
\mathbf{L} &=
\begin{bmatrix}
    l_{1, 1} & l_{1, 2} & l_{1, 3} & l_{1, 4} \\
    l_{2, 1} & l_{2, 2} & l_{2, 3} & l_{2, 4} \\
    l_{3, 1} & l_{3, 2} & l_{3, 3} & l_{3, 4}
\end{bmatrix}
\\[16pt]
\mathbf{L} &=
\underbrace{ 
\begin{bmatrix}
l_{1, 1} \\ l_{2, 1} \\ l_{3, 1}
\end{bmatrix}}_{u_{1}(x)}
,
\underbrace{ 
\begin{bmatrix}
l_{1, 2} \\ l_{2, 2} \\ l_{3, 2}
\end{bmatrix}}_{u_{2}(x)}
,
\underbrace{
\begin{bmatrix}
l_{1, 3} \\ l_{2, 3} \\ l_{3, 3}
\end{bmatrix}}_{u_{3}(x)}
,
\underbrace{
\begin{bmatrix}
l_{1, 4} \\ l_{2, 4} \\ l_{3, 4}
\end{bmatrix}}_{u_{4}(x)}
\end{align*}
```

For matrix $\mathbf{R}$:

```math
\begin{align*}
\mathbf{R} &=
%--- the 3×4 matrix ---
\begin{bmatrix}
    r_{1, 1} & r_{1, 2} & r_{1, 3} & r_{1, 4} \\
    r_{2, 1} & r_{2, 2} & r_{2, 3} & r_{2, 4} \\
    r_{3, 1} & r_{3, 2} & r_{3, 3} & r_{3, 4}
\end{bmatrix}
\\[16pt]
\mathbf{R} &=
\underbrace{ 
\begin{bmatrix}
r_{1, 1} \\ r_{2, 1} \\ r_{3, 1}
\end{bmatrix}}_{v_{1}(x)}
,
\underbrace{ 
\begin{bmatrix}
r_{1, 2} \\ r_{2, 2} \\ r_{3, 2}
\end{bmatrix}}_{v_{2}(x)}
,
\underbrace{
\begin{bmatrix}
r_{1, 3} \\ r_{2, 3} \\ r_{3, 3}
\end{bmatrix}}_{v_{3}(x)}
,
\underbrace{
\begin{bmatrix}
r_{1, 4} \\ r_{2, 4} \\ r_{3, 4}
\end{bmatrix}}_{v_{4}(x)}
\end{align*}
```

For matrix $\mathbf{O}$:

```math
\begin{align*}
\mathbf{O} &=
\begin{bmatrix}
    o_{1, 1} & o_{1, 2} & o_{1, 3} & o_{1, 4} \\
    o_{2, 1} & o_{2, 2} & o_{2, 3} & o_{2, 4} \\
    o_{3, 1} & o_{3, 2} & o_{3, 3} & o_{3, 4}
\end{bmatrix}
\\[16pt]
\mathbf{O} &=
\underbrace{ 
\begin{bmatrix}
o_{1, 1} \\ o_{2, 1} \\ o_{3, 1}
\end{bmatrix}}_{w_{1}(x)}
,
\underbrace{ 
\begin{bmatrix}
o_{1, 2} \\ o_{2, 2} \\ o_{3, 2}
\end{bmatrix}}_{w_{2}(x)}
,
\underbrace{
\begin{bmatrix}
o_{1, 3} \\ o_{2, 3} \\ o_{3, 3}
\end{bmatrix}}_{w_{3}(x)}
,
\underbrace{
\begin{bmatrix}
o_{1, 4} \\ o_{2, 4} \\ o_{3, 4}
\end{bmatrix}}_{w_{4}(x)}
\end{align*}
```

Where:
- $u_1(x), u_2(x), ..., u_m(x)$ are the Lagrange interpolating polynomials that interpolate the column vectors of matrix $\mathbf{L}$. 

- $v_1(x), v_2(x), ..., v_m(x)$ are the Lagrange interpolating polynomials that interpolate the column vectors of matrix $\mathbf{R}$. 

- $w_1(x), w_2(x), ..., w_m(x)$ are the Lagrange interpolating polynomials that interpolate the column vectors of matrix $\mathbf{O}$. 

By now, we know that the group of vectors in a finite field under addition is homomorphic to the group of polynomials in a finite field under addtion. **And this by extension means multiplying a vector (column vector) in a finite field by a scalar is homomorphic to multiplying a polynomial in a finite field by a scalar.**
- We know this to be true since we have established earlier that the homomorphism is addition-preserving and scalar-multiplication preserving.

**Thus each polynomial can be multiplied by their respective element in the witness $\mathbf{a}$:**

That is:

```math
\begin{align*}
\mathbf{L} \cdot \mathbf{a} &=
\begin{bmatrix}
    l_{1, 1} & l_{1, 2} & l_{1, 3} & l_{1, 4} \\
    l_{2, 1} & l_{2, 2} & l_{2, 3} & l_{2, 4} \\
    l_{3, 1} & l_{3, 2} & l_{3, 3} & l_{3, 4}
\end{bmatrix} \cdot
\begin{bmatrix}
a_{1} \\ a_{2} \\ a_{3} \\ a_{4}
\end{bmatrix} \\[24pt]
&=
\begin{bmatrix}
    u_1(x) & u_2(x) & u_3(x) & u_4(x)
\end{bmatrix} \cdot
\begin{bmatrix}
a_{1} \\ a_{2} \\ a_{3} \\ a_{4}
\end{bmatrix} \\[24pt]
&=
a_1u_1(x) + a_2u_2(x) + a_3u_3(x) + a_4u_4(x) \\[4pt]
&=
\sum_{i = 1}^{4}a_iu_i(x)
\end{align*}
```

```math
\begin{align*}
\mathbf{R} \cdot \mathbf{a} &=
\begin{bmatrix}
    v_1(x) & v_2(x) & v_3(x) & v_4(x)
\end{bmatrix} \cdot
\begin{bmatrix}
a_{1} \\ a_{2} \\ a_{3} \\ a_{4}
\end{bmatrix} \\[24pt]
&=
a_1v_1(x) + a_2v_2(x) + a_3v_3(x) + a_4v_4(x) \\[4pt]
&=
\sum_{i = 1}^{4}a_iv_i(x)
\end{align*}
```

```math
\begin{align*}
\mathbf{O} \cdot \mathbf{a} &=
\begin{bmatrix}
    w_1(x) & w_2(x) & w_3(x) & w_4(x)
\end{bmatrix} \cdot
\begin{bmatrix}
a_{1} \\ a_{2} \\ a_{3} \\ a_{4}
\end{bmatrix} \\[24pt]
&=
a_1w_1(x) + a_2w_2(x) + a_3w_3(x) + a_4w_4(x) \\[4pt]
&=
\sum_{i = 1}^{4}a_iw_i(x)
\end{align*}
```

Something to note is that each final result is a single polynomial with degree $\le n-1$. This is because each column vector in each matrix has $n$ rows which translates to $n$ points being interpolated by Lagrange interpolation. Thus, we can also say that all polynomials interpolated from matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$ will be Lagrange interpolating polynomials, and they will each have degree $\le n-1$.

In a way of summarizing the above, each matrix-witness dot-product in the R1CS: $\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}$ can thus be transformed as:

```math
\mathbf{La} \rightarrow \sum_{i = 1}^{4}a_iu_i(x) \\[4pt]
\mathbf{Ra} \rightarrow \sum_{i = 1}^{4}a_iv_i(x) \\[4pt]
\mathbf{Oa} \rightarrow \sum_{i = 1}^{4}a_iw_1(x)
```

And since each sum term evaluates to a polynomial, we can then represent them as:

```math
\mathbf{La} \rightarrow \sum_{i = 1}^{4}a_iu_i(x) = u(x) \\[4pt]
\mathbf{Ra} \rightarrow \sum_{i = 1}^{4}a_iv_i(x) = v(x)\\[4pt]
\mathbf{Oa} \rightarrow \sum_{i = 1}^{4}a_iw_i(x) = w(x)
```

The polynomials $u(x)$, $v(x)$, and $w(x)$ will all have degree $\le n-1$.

## The Necessity to Interpolate All Columns
Because of the homomorphism:
- $\mathcal{L}(\mathbf{v_1} + \mathbf{v_2}) = \mathcal{L}(\mathbf{v_1}) + \mathcal{L}(\mathbf{v_2}) \quad$ (addition-preserving)

- $\mathcal{L}(\lambda\mathbf{v}) = \lambda\mathcal{L}(\mathbf{v}) \quad$ (scalar-multiplication preserving)

If we compute the polynomial $u(x)$ as: $\mathcal{L}(\mathbf{La})$ (i.e., we first compute the matrix-witness dot-product $\mathbf{La}$ which yields a single vector, and then interpolate that vector with Lagrange interpolation); we would still get the same result compared to if we broke matrix $\mathbf{L}$ into its respective $m$ columns, interpolate each column vector with Lagrange interpolation, multiply each Lagrange interpolating polynomial with its respective element in the witness $\mathbf{a}$, and then summing the result.

Spoken more mathematically:

```math
\sum_{i = 1}^{m}a_iu_i(x) = \mathcal{L}(\mathbf{La}) \quad | \quad u_i(x) \ \text{is the Lagrange interpolating polynomial of column vector } i \text{ in matrix } \mathbf{L}
```

So why do we not just compute a single Lagrange interpolating polynomial, instead of having to compute $m$ of them?

**There must be a distinction between who is using the QAP - the prover or the verifier.** The verifier (and the trusted setup - which will be covered later on), do not and cannot know the witness $\mathbf{a}$ and therefore cannot compute $\mathcal{L}(\mathbf{La})$. This is an optimization that only the prover can make, and other parties in the ZK protocol cannot make use of this optimization.

More specifically, 
- Prover's optimization:
    - The prover knows the witness $\mathbf{a}$ (private input).
    - They can compute the matrix-witness dot-product (or linear combination) $\mathbf{La}$, and then interpolate it to get $\mathcal{L}(\mathbf{La}) = u(x)$.
    - This is efficient because its only one Lagrange interpolation.

- Verifier's Constraint:
    - The verifier does not know the witness $\mathbf{a}$ since it's private to the prover.
    - They only know the public structure of the QAP: the precomputed Lagrange interpolations of each column of matrices $\mathbf{L}$, $\mathbf{R}$, and $\mathbf{O}$.
    - To verify the prover's claim, the verifier needs to work with these precomputed Lagrange interpolating polynomials, not the witness-dependent computation $\mathcal{L}(\mathbf{La})$

- Trusted Setup:
    - The QAP polynomials: $u(x)$, $v(x)$, $w(x)$, are created during the trusted setup phase, where the structure of the R1CS is "baked into" the polynomials.
    - All parties in the ZK protocol must agree on these polynomials before any proofs are generated or verified.
    - The verifier cannot later compute $\mathcal{L}(\mathbf{La})$ because $\mathbf{a}$ is always private.

## Polynomial Degree Imbalance
At this point, we CANNOT express the final result of: $\mathbf{La} \circ \mathbf{Ra} = \mathbf{Oa}$, as:

```math
u(x)v(x) = w(x)
```

because the polynomial degrees on both sides of the equality are not equal (do not match).

Multiplying two polynomials together results in a product polynomial of which its degree is the sum of the degrees of the two polynomials being multiplied together.

Polynomials $u(x)$, $v(x)$, and $w(x)$ are each of degree $n-1$. Thus when we multiply $u(x)$ and $v(x)$, the product polynomial $u(x)v(x)$ will have degree: $(n-1) + (n-1) = 2n - 2$.

Since $w(x)$ (the target polynomial) has degree $n - 1$, then:

```math
u(x)v(x) \neq w(x)
```

As polynomials, $u(x)v(x)$ and $w(x)$ are not equal even though the underlying vector interpolated by $u(x)v(x)$ is equal to the underlying vector interpolated by $w(x)$.

That is, the vector that polynomial $u(x)v(x)$ interpolates at $x = 1, 2, ...,n$:

```math
[(1, u(1)v(1)), \ (2, u(2)v(2)), \ ..., \ (n, u(n)v(n))]
```

is identical to the vector that polynomial $w(x)$ interpolates at $x = 1, 2, ...,n$:

```math
[(1, w(1)), \ (2, w(2)), \ ..., \ (n, w(n))]
```

because the original vectors obeyed: $u_iv_i = w_i$.

Although the underlying vectors on both sides of the equality are equal, the polynomials that interpolate them are not equal.

Another way to put it, the polynomials $u(x)v(x)$ and $w(x)$ may evaulate to the same values at specific points $x = [1, 2, ...n]$, but they are not the same polynomial because their degrees differ (which is to say $u(x)v(x)$ and $w(x)$ are distinct polynomials).

**This is because the homorphisms we established earlier only make claims about vector addition (and vector scalar multiplcation), not Hadamard product.**

Meaning, we cannot naively assert that $u(x)v(x) = w(x)$ as polynomials, even though their evaluations (underlying vectors they interpolate) match. This mismatch occurs because:
- The homomorphism $\mathcal{L}$ preserves linear operations (addition/scalar multiplication), but not multiplicative operations like the Hadamard product.
- The Hadamard product of vectors $\mathbf{u} \circ \mathbf{v}$ translates to pointwise multiplication in evaluations, but this does not carry over to polynomial multiplication from interpolation.

### Example of the Underlying Equality/Inequality
Let $u(x)$ be the Lagrange interpolating polynomial that interpolates the vector $[2, 4, 8]$:

```math
u(x) = x^2 - x + 2 \\[8pt]
u(1) = 2, \ u(2) = 4, \ u(3) = 8
```

And let $v(x)$ be the Lagrange interpolating polynomial that interpolates the vector $[4, 2, 8]$:

```math
v(x) = 4x^2 - 14x + 14 \\[8pt]
v(1) = 4, \ v(2) = 2, \ v(3) = 8
```

Note that the above polynomials are not represented in their finite field equivalent. Calculating them in $\mod 17$ would yield $u(x) = x^2 + 16x + 2$ and $v(x) = 4x^2 + 3x + 14$.

If we take the Hadamard product of vectors $[2, 4, 8] \circ [4, 2, 8]$, the result will be: $[8, 8, 64]$. And if we multiply polynomials $u(x)$ and $v(x)$ together, we get the product polynomial $w(x) = 4x^4 - 18x^3 + 36x^2 - 42x + 28$. The Lagrange interpolating polynomial that interpolates the Hadamard product vector $[8, 8, 64]$ is: $h(x) = 28x^2 - 84x + 64$ (or $11x^2 + x + 13$ in $\mod 17$).

The following is a plot of polynomials $h(x)$ (red) and $w(x)$ (blue):
![qap-point-cross](/module2/06-QAPs/qap-3-point-cross.png)

Notice that both the product polynomial $w(x)$ and the Lagrange interpolating polynomial of the Hadamard product vector $h(x)$ do not look the same and yet they interpolate the exact same points. The key here is that the product polynomial $w(x)$ interpolates the Hadamard product $[8, 8, 64]$ of the two vectors from $u(x)$ and $v(x)$. Despite interpolating the exact same points, i.e. having the same underlying vectors, the two polynomials are clearly different and not equal.

The important thing at this point is to figure out how to "make" $w(x)$ equal to $u(x)v(x)$ as polynomials since they both interpolate the same vector over the common set of $x$ values $[1, 2, ..., n]$.

## Interpolating the Zero Vector $\mathbf{0} = [0, 0, ..., 0]$
**If $\mathbf{v_1} \circ \mathbf{v_2} = \mathbf{v_3}$, then $\mathbf{v_1} \circ \mathbf{v_2} = \mathbf{v_3} + \mathbf{0}$ (where $\mathbf{0}$ is the zero vector $[0, 0, ..., 0]$).**

When we interpolate $\mathbf{0}$ (i.e. interpolate the points $[(1, 0), (2, 0), ..., (n, 0)]$), the minimal-degree polynomial that interpolates these points is the zero polynomial $f(x) = 0$.

Instead of interpolating $\mathbf{0}$ with Lagrange interpolation and getting $f(x) = 0$ (remember that Lagrange interpolation finds the polynomial of the lowest degree $\le n-1$ that interpolates all points in a set of $n$ points), we can utilize a **higher-degree polynomial** that also interpolates $\mathbf{0}$ to balance out the mismatch in polynomial degrees.

**That is, we find a polynomial $b(x)$ that interpolates the points $[(1, 0), (2, 0), ..., (n, 0)]$.**

Another way to put it, find a polynomial $b(x)$ that evaluates to zero over the common set of $x$ values: $[1, 2, ..., n]$. Such as:

```math
b(x) = (x - 1)(x - 2)...(x - n)
```

For example, the black polynomial ($b(x) = 4x^4 - 18x^3 + 8x^2 + 42x + 28$) in the image below interpolates the points: $[(1, 0), (2, 0), (3, 0)]$.

![zero-poly](/module2/06-QAPs/qap-zero-polynomial.png)

It can be said that $b(x) = 4x^4 - 18x^3 + 8x^2 + 42x + 28$ is a valid interpolation of the zero vector $[0, 0, 0]$.

(On a side note, be aware that $\mathbf{0}$ can cary in its representations depending on the context. Higher-degree polynomials can be valid interpolations of $\mathbf{0}$ but they are not minimal. The space of possible interpolants for $\mathbf{0}$ (i.e. all polynomials that evaluate to zero over the common set of $x$ values) is infinite-dimensional - since we can construct infinitely many higher-degree polynomials that fit.)

Thus, we can rewrite our original equation: $u(x)v(x) = w(x)$ to the following balanced equation:

```math
u(x)v(x) = w(x) + b(x)
```

Note that in the image above, $b(x)$ was computed based on the balanced equation as:

```math
b(x) = u(x)v(x) - w(x)
```

However, we can't let the prover choose any random $b(x)$, otherwise a malicious prover could choose a $b(x)$ that balances $u(x)v(x)$ and $w(x)$, but ultimately does not interpolate the same underlying vector (e.g. $[8, 8, 64]$). In other words, a malicious prover could pick a $b(x)$ that balances the equation but both sides do not end up with the same underlying vector.