# Elliptic Curve point addition is akin to "connect the dots and flip".

# Our formulas over real numbers use the normal field operations of addition and multiplication. 
# Although we use square roots to determine if a point is on the curve, and square roots are 
# not a valid field operator, we do not use square roots to compute the addition and doubling of points.

# The reader can verify this by picking two points from the plot in `02_BN128_plot_simple.py`, then plugging them into
# the code below to add points and seeing they always land on another point (or the point on infinity 
# if the points are inverses of each other). These formulas are taken from the Wikipedia page on 
# elliptic curve point multiplication.

# Example of points:
# (0, 5), (0, 6)
# (1, 2), (1, 9)
# (2, 0)
# (4, 1), (4, 10)
# (7, 4), (7, 7)
# (8, 3), (8, 8)

def double(x, y, a, p):
    lambd = (((3 * x**2) % p ) *  pow(2 * y, -1, p)) % p
    newx = (lambd**2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    return (newx, newy)

def add_points(xq, yq, xp, yp, p, a=0):
    if xq == yq == None:
        return xp, yp
    if xp == yp == None:
        return xq, yq

    assert (xq**3 + 3) % p == (yq ** 2) % p, "q not on curve"
    assert (xp**3 + 3) % p == (yp ** 2) % p, "p not on curve"

    if xq == xp and yq == yp:
        return double(xq, yq, a, p)
    elif xq == xp:
        return None, None

    lambd = ((yq - yp) * pow((xq - xp), -1, p) ) % p
    xr = (lambd**2 - xp - xq) % p
    yr = (lambd*(xp - xr) - yp) % p
    return xr, yr

print(double(7, 7, 11)) # (0, 6)
print(double(8, 3, 11)) # (7, 7)
print(add_points(7, 7, 8, 8, 11)) # (8, 3)
print(add_points(7, 7, 8, 3, 11)) # (1, 2)



