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

In other words, the sum of the polynomials resulting from interpolating vectors $v$ and $w$ separately is the same as the polynomial resulting from interpolating the sum of vectors $\mathbf{v}$ and $\mathbf{w}$.

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

It also means that scalar multiplication of a vector corresponds to scalar multiplication of the interpolated polynomial, but it DOES NOT correspond to repeated polynomial addition in a finite field. Rather it is the coefficient-wise scalar multiplication of the polynomial in the finite field.

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

### Scalar Multiplication IS REALLY Vector Addition


## A R1CS in Polynomials