# Largrange Interpolation with Python
https://rareskills.io/post/python-lagrange-interpolation

Lagrange interpolation is a technique for computing a polynomial that passes through a set of $n$ points.

## Interpolating a Vector as a Polynomial

#### Examples:

### A Straight Line Through Two Points
If we have two points, they can be interpolated with a linear line. For instance, given $(1, 1)$ and $(2, 2)$, we can construct a linear line that intersects these two points. This line would be a straight line: $y = x$, which is a degree $1$ polynomial (linear function).

### A Single Point
If we have a single point, we can construct a horizontal line that passes through the single point. For instance, given the point $(2, 5)$, we can construct the line $y = 5$ to interpolate the single point. This line would be a degree $0$ polynomial (constant function).

### Three Points and a Parabola
For any set of $n$ distinct points, we can draw a polynomial of degree AT MOST $n-1$ that passes through all $n$ points. For example, the $3$ points: $(0, 0)$, $(1, 1)$, $(2, 4)$ can be interpolated with the degree $2$ polynomial: $y = x^{2}$.

If the $3$ points are in a straight line, such as: $(0, 0)$, $(1, 1)$, $(2, 2)$, we can interpolate them with the degree $1$ polynomial: $y = x$. This is still correct. In general, however, $3$ points won't be collinear (wont lie in the same straight line), thus we will need a degree $2$ polynomial to intersect all $3$ points.

## Langrange Interpolating Polynomial
[FYI, done out of curiosity]

The Lagrange interpolating polynomial is the polynomial $P(x)$ of degree $\le (n-1)$ that passes through $n$ points: $[ \ P(x_1) = (x_1, y_1), \ P(x_2) = (x_2, y_2), ..., P(x_n) = (x_n, y_n) \ ]$, and is given by:

```math
P(x) = 
\sum_{j = 1}^{n} y_j
\prod_{\substack{k = 1 \\ k \neq j}}^n
\frac{x - x_k}{x_j - x_k}
```

The $\prod$ symbol (pi-notation for product symbol) denotes the repeated multiplication over a specified range, i.e $\prod_{k = 1}^n a_k$ means: $a_1 \times a_2 \times ... \times a_n$.

The inner product ($\prod$) has the Kronecker delta property, which in very simple words is described as "yields 1 when the indices match, 0 otherwise".

The inner product builds the basis polynomial for a fixed $j$; and $\frac{x - x_k}{x_j - x_k}$ equals to $1$ when $x = x_j$, and equals to $0$ when $x = x_k$ for any $k \neq j$.

The outer sum ($\sum$) adds these basis polynomials, each scaled by its corresponding data value $y_j$, to reconstruct the unique $\le (n - 1)$ polynomial that passes through all $n$ points. The value $y_j$ is the value that is paired with $x_j$, i.e. the data value the interpolating polynomial must hit when $x = x_j$ because $P(x_j) = (x_j, y_j)$.

In other words, if we want to be very explicit with Langrange interpolation, it can be written explicitly as:

```math
P(x) = 
y_1 \cdot \frac{(x - x_2)(x - x_3)...(x - x_n)}{(x_1 - x_2)(x_1 - x_3)...(x_1 - x_n)} \ + \
y_2 \cdot \frac{(x - x_1)(x - x_3)...(x - x_n)}{(x_2 - x_1)(x_2 - x_3)...(x_2 - x_n)} \ + \
... \ + \
y_n \cdot \frac{(x - x_1)(x - x_2)...(x - x_{n-1})}{(x_n - x_1)(x_n - x_2)...(x_n - x_{n-1})}
```

## Python Code for Lagrange Interpolation
For our purposes, We DO NOT need to know how to compute this polynomial. There are math libraries that will do this for us. The most common algorithm is Lagrange Interpolation and the following shows how to do it in Python.

### Float Example
We can compute a polynomial $p(x)$ that intersects the points: $(1,4)$, $(2,8)$, $(3,2)$, $(4,1)$ using Lagrange interpolation.

```python
from scipy.interpolate import lagrange

x_values = [1, 2, 3, 4]
y_values = [4, 8, 2, 1]

print(lagrange(x_values, y_values))
# Output:
#     3      2
# 2.5 x - 20 x + 46.5 x - 25
#
# (i.e. 2.5x^3 - 20x^2 + 46.5x - 25)
```

### Finite Field Example
Using the same points as before, we will use a finite field $\mathbb{F}_{17}$ instead of floating point numbers.

```python
import galois
import numpy as np

GF17 = galois.GF(17)

xs = GF17(np.array([1, 2, 3, 4]))
ys = GF17(np.array([4, 8, 2, 1]))

p = galois.lagrange_poly(xs, ys)

print(p)
# 11x^3 + 14x^2 + 4x + 9

assert p(1) == GF17(4)
# p(1) = 38 = 4 (mod 17)

assert p(2) == GF17(8)
# p(2) = 161 = 8 (mod 17)

assert p(3) == GF17(2)
# p(3) = 444 = 2 (mod 17)

assert p(4) == GF17(1)
# p(4) = 953 = 1 (mod 17)
```

## Uniqueness of the Interpolating Polynomial
Going back to the example of the points $(1, 1)$, $(2, 2)$, the lowest degree polynomial that interpolates them is degree $1$ polynomial $y = x$.

In general, for a set of $n$ points, there is a unique lowest-degree polynomial of at most degree $n - 1$ that interpolates all $n$ points.

The polynomial of lowest degree that interpolates all points in the set is called the lagrange polynomial.

This means, if we use the set of points $(1, 2, ..., n)$ as the $x$ values to convert a length $n$ vector to a polynomial through Lagrange interpolation, then the resulting polynomial is unique.

That is, for the set of $n$ points $x = 1, 2, ..., n$, we can take any vector $(y_1, y_2, ..., y_n)$, plot it as $(1, y_1), (2, y_2), ..., (n, y_n)$ and Lagrange interpolation guarantees a unique single polynomial of degree $\le (n-1)$ that passes through all those points. Unique here means no other polynomial of degree $\le (n-1)$ can hit the same set of points.

In other words, given a consistent basis of $x$ values to interpolate a vector over, there is a unique polynomial that interpolates a given vector. In another way to put it, every length $n$ vector has a unique polynomial representation.

Informally, every $n$ degree vector has a unique $n - 1$ degree polynomial that "represents" it. The degree could be less if, for example, the points are collinear but the vector will be unique.

The "lowest degree" part is important. Given two points, there is an extremely large number of polynomials that cross those two points - but the lowest degree polynomial is unique.