# Bilinear Pairings and How They Work
https://www.rareskills.io/post/bilinear-pairing

## Prerequisites
- Elliptic curve point addition and scalar multiplication.
- Discrete log problem: Q = rP, where Q and P are EC points and r is the scalar. And it is infeasible to solve for r even if we know both EC points.
- Finite field, cyclic groups, the generator point, in the context of ECs.
- Uppercase letters denote EC points, and lowercase letters denote finite field elements (the "scalars").

## Bilinear Pairings At a High Level
Bilinear pairings allow us to take three numbers: $(a, b, c)$, where $ab = c$, and encrypt them through an encryption function: $E$, such that they become: $E(a), E(b), E(c)$. These encrypted values can then be used by a verifer to verify that $E(a) \cdot E(b) = E(c)$ without showing the verifier what the original values were. Bilinear pairings can be used to prove that a 3rd number is the product of the first two original numbers.

## How do Bilinear Pairings Work
We know conceptually that in elliptic curves, scalar multiplication is repeated point addition. When a scalar is multiplied by an EC point, another EC point is produced (group theory). That is $P = pG$ where $p$ is the scalar (the discrete log), and $G$ is the generator. And given $P$ and $G$, we cannot solve for $p$.

Given an assumption: $pq = r$, what we are trying to do is take the EC points:

```math
P = pG \\
Q = qG \\
R = rG
```

And convince a verifier that multiplying of the discrete logs of $P$ and $Q$ yields the discrete log of $R$.

And if: $pq = r$, and given: $P$, $Q$, and $R$, then we want a function:

$$
f(P, Q) = R
$$

such that it does not equate to $R$ when $pq \neq r$. And that this will hold true for all possible combinations of $p$, $q$, and $r$ in the elliptic curve group.

However, $R$ is not usually expressed as such when using bilinear pairings, rather:

$$
f(P,Q) = f(R,G)
$$

Where $G$ is the generator and can be though of as: $1$. For instance, since $pG$ means we added $G$ to itself $p$ times, then a simple $G$ just means nothing was done to $G$ (left as is). Conceptually this is the same as saying: $P \times Q = R \times 1$.

The bilinear pairing is thus a function that when we pass two EC points, we get an output that corresponds to the product of the discrete logs of the two EC points that were passed into the function.

A bilinear pairing is usually written as: $e(P, Q)$. Note that $e$ has nothing to do with the natural logarithm, and $P$ and $Q$ are EC points.

## Generalization, checking if two products are equal
If given four EC points: $P_1$, $P_2$, $Q_1$, $Q_2$, and that the discrete logs of $P_1$, and $P_2$ have the same product as the discrete logs of $Q_1$ and $Q_2$ (that is: $p_1 \cdot p_2 = q_1 \cdot q_2$). Using a bilinear pairing, we can verify this is true without knowing any of the discrete logs $p_1$, $p_2$, $q_1$, and $q_2$. Simply:

$$
e(P_1, P_2) \stackrel{?}{=} e(Q_1, Q_2)
$$

## "Bilinear"
Bilinear means that if a function takes two arguments, and one argument is held constant while the other argument varies, then the output linearly varies with the non-constant argument.

That is, if $f(x,y)$ is bilinear and $c$ is a constant, then $z = f(x,c)$ varies linearly with $x$, and $z = f(y,c)$ varies linearly with $y$.

We can therefore infer that that an elliptic curve bilinear pairing has the following property:

$$
f(aG, bG) = f(abG, G) = f(G, abG)
$$

### In more depth
Let $G$ be an additive cyclic group with curve order $n$ (which is prime), with generator $G_1$. And let $G_T$ be the multiplicative cyclic group of the same curve order.

(FYI: output of a bilinear pairing is usually an element of a multiplicative cyclic group of a finite field)

A bilinear pairing is a map:

$$
e:G \times G \rightarrow G_T
$$

such that for every elliptic curve points $P, Q \in G$, and scalars $a, b \in \mathbb{Z_n}$:

- Linearity in the first input (slot): $e(aP, Q) = e(P, Q)^a$
- Linearity in the second input (slot): $e(P, bQ) = e(P, Q)^b$

To elaborate further, in a bilinear pairing, we are moving between two kinds of groups:

- $G$ (elliptic curve points) under addition ($+$), where the "linear" action is scalar multiplication $aG = G + ... +G$ (add $G$ to itself $a$ times).
- $G_T$ (finite field subgroup) under multiplication ($\times$), where the "linear" action is exponentiation $g^a = g \times ... \times g$ (multiply $g$ by itself $a$ times).

The pairing acts like a homomorphism that translates “add $a$ times” in the curve into “multiply $a$ times” in the finite field. That is the "linear" action (repeated addition) in the domain $G$ becomes "exponentiation" (repeated multiplication) in the target $G_T$:

```math
\underbrace{aP}_{\text{add }a\text{ times}}
\;\xrightarrow{\;e\;}
\underbrace{e(P,Q)^a}_{\text{multiply }a\text{ times}}
```

Since:

```math
\begin{aligned}
e(aG,bG) &= e(G,bG)^a \\[4pt]
            &= \bigl(e(G,\, G)^a\bigr)^{\,b} \\[4pt]
            &= e(G,\, G)^{ab}\, .
\end{aligned}
```

And as such:

```math
\begin{aligned}
e(abG,G) = e(G,G)^{ab} \\[8pt]
e(G,abG) = e(G,G)^{ab}
\end{aligned}
```

Thus we arrive at the elliptic curve bilinear pairing property:

$$
e(aG, bG) = e(abG, G) = e(G, abG)
$$

## What is $e(P,Q)$ Returning?
As mentioned above, the output of a bilinear pairing is an element of a multiplicative cyclic group of a finite field (or simply: an element of a finite cyclic group). This group is referred to as $G_T$.

However, it is beyond the scope that we need to know how it is mathematically derived because it is too complex: "To be honest, the output is so mathematically scary that it would be counterproductive to try to really explain it."

Technically, the output $e(P,Q)$ is constrained to a subgroup of $G_T$ with the same prime curve order as $G_1$ and $G_2$ (more on $G_2$ later).

Or to be even more technical, the output of a bilinear pairing is an element of $G_T$, a multiplicative subgroup of order $r$ within a finite field extension $\mathbb{F}^{*}_{q^k}$ where $k$ is the embedding degree.

It is best to treat $e(P,Q)$ as a black box, similar to how we treat hash functions (such as `keccak256`) like black boxes. In fact, cryptography papers also treat bilinear pairings as black boxes.

But despite bilinear pairings being treated as a black box, we still know a lot about the properties of the output, which is an element of $G_T$:

- $G_T$ is a cyclic group, which means it has a closed binary operator.
- The binary operator of $G_T$ is associative.
- $G_T$ has an identity element.
- Every element in $G_T$ has an inverse.
- Since the group is cyclic, it has a generator.
- Because the group is cyclic and finite, then finite cyclic groups (groups where all elements are powers of a single generator $g$) are homomorphic to $G_T$
- That is, we have some way to homomorphically map elements in a finite field to elements in $G_T$.

Because the group $G_T$ is cyclic, we have a notion of $G_T$, $2G_T$, $3G_T$, and so forth. The binary operator of $G_T$ is roughly what we could call "multiplication", so $8G_T = 2G_T * 4G_T$.

If we really want to know what $G_T$ "looks like", it is a 12-dimensional object. The identity element is: $(1,0,0,0,0,0,0,0,0,0,0,0)$, also known as the multiplicative identity 1 in the finite field extension where $G_T$ resides.

## Symmetric and Asymmetric Groups
The notation $e(P,Q)$ implies that we are using the same elliptic curve group and generator point everywhere when we say:

$$
e(aG,bG) = e(abG,G)
$$

In practice, however, it is easier to create bilinear pairings when the two input groups are different (but of the same order). That is, bilinear pairings often use asymmetric groups (with identical orders).

Specifically:

$$
e(a,b) \rightarrow c \hspace{0.5cm} a \in G_1, \hspace{0.125cm} b \in G_2, \hspace{0.125cm} c \in G_T
$$

None of the groups are the same: $G_1 \neq G_2 \neq G_T$.

However the elliptic curve bilinear pairing property that we care about still holds:

$$
e(aG_1, bG_2) = e(abG_1, G_2) = e(G_1, abG_2)
$$

In the above equation, $G_T$ is not explicitly shown, but that is the codomain (output) space of $e(G_1, G_2)$. That is, the bilinear pairing maps pairs of elements from groups $G_1$ and $G_2$ to elements in the target group $G_T$.

We could think of $G_1$ and $G_2$ as being different elliptic curve equations with different parameters (BUT THE SAME NUMBER OF POINTS), and that would be valid because they are different groups.

In a symmetric pairing, the same elliptic curve group, for instance $G_1$, is used for both arguments of the bilinear pairing function. This means that the elliptic curve group and the generator point used in both arguments is the same. In such cases, the pairing is denoted as:

$$
e(aG_1, bG_1) = e(abG_1, G_1) = e(G_1, abG_1)
$$

In practice, asymmetric groups are used, and the difference between the groups $G_1$ and $G_2$ will be explained shortly.

$G_1$ is the same group that was used in previous chapeters in the ZK book, and in the context of Ethereum, it is the same $G_1$ that we import from the `py_ecc.bn128` library. $G_2$ can also be imported from the same library.
```python
from py_ecc.bn128 import G1, G2
```

## Field Extensions and the $G_2$ point in Python
Bilinear pairings are rather agnostic to the kinds of groups we opt for, but Ethereum's $G_2$ uses ellipictic curves with field extensions. If we want to be able to read Solidity code that uses ZK-SNARKS, we need to have a rough idea of what these are.

Usually EC points are thought of as two points $x$ and $y$. With field extensions, the $x$ and $y$ themselves become TWO-DIMENSIONAL objects $(x,y)$ pairs.

This is analogous to how complex numbers "extend" real numbers and turn them into something with two-dimensions (a real component and an imaginary component).

A field extension is a very abstract concept, and frankly, the relationship between a field and its extension doesn’t matter from a purely functional concept.

Just think of it this way: An elliptic curve in $G_2$ is an elliptic curve where both the $x$ and the $y$ element are two-dimensional objects. In other words, a $G_2$ point is a pair of tuples: $((x_0,x_1), \space (y_0,y_1))$.

## Why must $G_1$ and $G_2$ have the same order?
It is important for $G_1$ and $G_2$ (and by extension $G_T$) to have the same order (number of points) so that the bilinear pairing $e: G_1 \times G_2 \rightarrow G_T$ can exist.

Consider $G_1$ and $G_2$ with order $r = 5$:

- A bilinear pairing $e(G_1,G_2)$ generates $G_T$ which also has order $r = 5$

- Bilinearity holds:

$$
e(2G_1, 3G_2) = e(G_1,G_2)^6 = e(G_1,G_2)^1 \hspace{0.125cm} (since \ 6 \equiv 1 \ mod \ 5)
$$

- The exponents "wrap around correctly" because $G_T$ also has order 5.

Consider if $G_1$ has $r_1 = 5$, and $G_2$ has $r_2 = 7$:

- We know $5G_1 = O \ (identity \ in \ G_1)$, and $7G_2 = O \ (identity \ in \ G_2)$

- If bilinearity held, we'd expect:

$$
e(5G_1, 7G_2) = e(G_1, G_2)^{35}
$$ 

- But this would also mean:

$$
e(5G_1, 7G_2) = e(G_1, G_2)^{35} = e(O, O) = 1 \ \text{(by definition)}
$$

- Since $G_T$'s order must divide both $r_1$ and $r_2$ (to avoid contradictions), the only solution is $e(G_1, G_2)^{35} = 1$. This forces $e(G_1,G_2) = 1$ for all $G_1$ and $G_2$, thus making the bilinear pairing degenerate (useless for cryptography).
    - This is connected to Lagrange's Theorem: The order of any subgroup (and consequently, the order of any element) of a finite group must divide the order of the group.
        - Since $e(G_1, G_2) \in G_T$, its order must divide both $r_1 = 5$ and $r_2 = 7$.
        - The only common divisor is 1, so $e(G_1,G_2)$ must have $r = 1$.

- Also:

```math
\begin{aligned}
e(5G_1, G_2) = e(G_1, G_2)^{5} = e(O, G_2) = 1 \ \text{(by definition)} \\[8pt]
e(G_1, 7G_2) = e(G_1, G_2)^{7} = e(G_1, O) = 1 \ \text{(by definition)}
\end{aligned}
```

- From the above, $e(G_1,G_2)$ must satisfy:

$$
e(G_1, G_2)^{5} = 1 \hspace{0.5cm} and \hspace{0.5cm} e(G_1, G_2)^{7} = 1
$$

- And the only element in $G_T$ satifying this is $1$. Because $5$ and $7$ are coprime and the LCM is $35$, so we can see it as: $x^{35} = 1$ meaning $x = 1$

- Thus: 

$$
e(G_1,G_2) = 1 \hspace{0.2cm} \forall \hspace{0.2cm} G_1, G_2
$$

## The $G_2$ point in Python
```python
from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq

print(G1)
# (1, 2)

print(G2)
#((10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634), (8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531))
```
Notice that $G_2$ is a pair of tuples. The first tuple is the two-dimensional $x$ point, and the second tuple is the two-dimensional $y$ point.

$G_1$ and $G_2$ are the generator points for their respective groups; and they both have the same curve order (number of points on the curve):
```python
from py_ecc.bn128 import G1, G2, eq, curve_order, multiply, eq, curve_order

x = 10 # chosen randomly
assert eq(multiply(G2, x + curve_order), multiply(G2, x))
assert eq(multiply(G1, x + curve_order), multiply(G1, x))
```

The behavior of $G_2$ is the same as other cyclic groups, especially the $G_1$ group we are familiar with. This means we can obtain other $G_2$ points with scalar multiplication (essentially repeated addition) as expected like how we observed with $G_1$ points.
```python
print(eq(add(G1, G1), multiply(G1, 2))) # True

print(eq(add(G2, G2), multiply(G2, 2))) # True
```

It should be obvious that we can only add elements from the same group (adding elements from different group violates closure thus breaking the group structure):
```python
add(G1, G2) # TypeError
```

On a side note, the `py_ecc` library overrides some arithmetic operators in python, meaning we can do the following:
```python
print(G1 + G1 + G1 == 3 * G1) # True

#The above is the same as this:
eq(add(add(G1, G1), G1), multiply(G1, 3)) # True
```

## Bilinear Pairings in Python
At the beginning of the chapter, we said that bilinear pairings can be used to check if the discrete logs of $P$ and $Q$ multiply to yield the discrete log of $R$. That is, $P = pG$, $Q = qG$, $R = rG$, and that $pq = r$.

That is, we specifically want:

$$
e(P,Q) = e(R,g_2), \quad\text{with}\quad
\begin{cases}
P = p\,g_1 \in G_1,\\
Q = q\,g_2 \in G_2,\\
R = r\,g_1 \in G_1.
\end{cases}
$$

Where: $g_1$ is a fixed generator of $G_1$, and $g_2$ is a fixed generator of $G_2$.

The LHS is equivalent to:

$$
e(P,Q) = e(pg_1, qg_1) = e(g1, g2)^{pq}
$$

And the RHS is equivalent to:

$$
e(R,g_2) = e(rg_1, g_2) = e(g1, g2)^{rq}
$$

Because $e(g_1, g_2)$ is a generator of $G_T$, the two values are equal if:

$$
pq \equiv r \ (mod \ r)
$$

which is exactly the discrete-log reltaion we are testing.

Here's how it can be achieved in Python:
```Python
from py_ecc.bn128 import G1, G2, pairing, multiply, eq

P = multiply(G1, 3)
Q = multiply(G2, 8)

R = multiply(G1, 24)

assert eq(pairing(Q, P), pairing(G2, R))
```

Note that the python library requires that the points belonging to $G_2$ be passed as the first argument to `pairing`.

## Equality of Products
At the beginning of the chapter, we also said that given EC points, a bilinear pairing can verify that the discrete logs of $P_1$, and $P_2$ have the same product as the discrete logs of $Q_1$ and $Q_2$:

$$
e(P_1, P_2) \stackrel{?}{=} e(Q_1, Q_2)
$$

This is how it can be achieved in Python:
```python
from py_ecc.bn128 import G1, G2, pairing, multiply, eq

P_1 = multiply(G1, 3)
P_2 = multiply(G2, 8)

Q_1 = multiply(G1, 6)
Q_2 = multiply(G2, 4)

assert eq(pairing(P_2, P_1), pairing(Q_2, Q_1))
```

## The Binary Operator of $G_T$
Elements in $G_T$ are combined using "multiplication" but keep in mind that this is actually a syntactic override in Python:
```python
from py_ecc.bn128 import G1, G2, pairing, multiply, eq

# 2 * 3 = 6
P_1 = multiply(G1, 2) # 2G_1
P_2 = multiply(G2, 3) # 3G_2


# 4 * 5 = 20
Q_1 = multiply(G1, 4) # 4G_1
Q_2 = multiply(G2, 5) # 5G_2

# 10 * 12 = 120 (6 * 20 = 120 also)
R_1 = multiply(G1, 10) # 10G_1
R_2 = multiply(G2, 12) # 12G_2

# e(P1, P2) * e(Q1, Q2) =?= e(R1, R2)
assert eq(pairing(P_2, P_1) * pairing(Q_2, Q_1), pairing(R_2, R_1))

# Fails!
```

### What is happening to the code?
The code above attempts to verify the following:

$$
e(2G_1, 3G_2) \ \cdot \ e(4G_1, 5G_2) \ \stackrel{?}{=} \ e(10G_1, 12G_2)
$$

Remeber the property of bilinear pairings:

$$
e(aG_1, bG_2) \ = \ e(abG_1, G_2) \ = \ e(G_1, abG_2) \ = \ e(G_1, G_2)^{ab}
$$

Thus the assertion fails because:

$$
e(2G_1, 3G_2) \cdot e(4G_1, 5G_2) = e(G_1,G_2)^{2 \cdot 3} \cdot e(G_1,G_2)^{4 \cdot 5} = e(G1, G2)^{6 + 20}
$$

And

$$
e(G1,G2)^{26} \neq e(G1,G2)^{120}
$$

### The Key Insight: $G_T$ is Multiplicative
$G_T$ is a multiplicative group, that is, all elements in $G_T$ behave like "powers" of a base.

Recall basic algebra:

$$
b^{x} \cdot b^{y} = b^{x+y}
$$

This is exactly what happens in any multiplicative group, including $G_T$.

As $G_T$ is a multiplicative group, its operation is multiplication, but its structure is exponential due to pairings:

$$
e(aG_1, bG_2) = e(G_1, G_2)^{ab}
$$

We can think of $b$ as $e(G_1, G_2)$ as a fixed base, and so $e(2G_1, 3G_2)$ would be akin to $b^{6}$.

Bilinear pairings convert elliptic curve additions (in $G_1$ and $G_2$) into "multiplications" in $G_T$, but the exponents come from scalar multiplications (another way to put it: pairings convert elliptic curve addition into exponentiation i.e. scalar multiplicativity multiplies exponents):

$$
e(aG_1, bG_2) = e(G_1, G_2)^{ab} \quad (\text{like} \ b^{ab})
$$

Thus to make the code work, we just change $R_1$ and $R_2$ to multiply to $26$.
```python
from py_ecc.bn128 import G1, G2, pairing, multiply, eq

# 2 * 3 = 6
P_1 = multiply(G1, 2)
P_2 = multiply(G2, 3)

# 4 * 5 = 20
Q_1 = multiply(G1, 4)
Q_2 = multiply(G2, 5)

# 13 * 2 = 26
R_1 = multiply(G1, 13)
R_2 = multiply(G2, 2)

# b ^ {2 * 3} * b ^ {4 * 5} = b ^ {13 * 2}
# b ^ 6 * b ^ 20 = b ^ 26

assert eq(pairing(P_2, P_1) * pairing(Q_2, Q_1), pairing(R_2, R_1))
```

Effectively computing:

$$
b^{2 \cdot 3} \ast b^{4 \cdot 5} = b^{13 \cdot 2}
$$

$$
b^{6} \ast b^{20} = b^{26}
$$

## Bilinear Pairings in Ethereum

### EIP 197 Specification
The `py_ecc` library is maintained by the Ethereum Foundation and it is what powers the precompile at address `0x8` in the [PyEVM implementation](https://github.com/ethereum/py-evm).

The Ethereum precompile defined in [EIP-197](https://eips.ethereum.org/EIPS/eip-197) works on elliptic curve points in $G_1$ and $G_2$, and implicitly works on points in $G_T$.

The precompile takes in a list of $G_1$ and $G_2$ points laid out as follows:

$$
A_1, B_1, A_2, B_2,..., A_n, B_n : A_i \in G_1, B_i \in G_2 
$$

There were originally created as:
```
A₁ = a₁G1
B₁ = b₁G2
A₂ = a₂G1
B₂ = b₂G2
...
Aₙ = aₙG1
Bₙ = bₙG2
```

The precompile returns `1` if the following is true:
```
a₁b₁ + a₂b₂ + ... + aₙbₙ = 0
```

and `0` if otherwise.

This seems to imply that the precompile is taking the discrete log of each of the points, which is considered infeasible in general. Furthermore, it does not behave like the pairing examples we have seen. Earlier examples return an element in $G_T$, but this precompile returns a `bool`.

### Justification for EIP 197 Design Decision
The first problem is that elements in $G_T$ are very large; specifically each element is a 12-dimentional object. This alone would take up a lot of space in memeory which leads to larger gas costs.

Also, because of how ZK verification algorithms work (out of scope here), we generally do not check the value of the output of a bilinear pairing, but only that the output of the bilinear pairing is equal to other bilinear pairings. Using a simple example:

$$
e(A, B) \ \stackrel{?}{=} \ e(C, D) \ \cdot \ e(E,F)
$$

Specifically, the final step in [Groth16](https://www.rareskills.io/post/groth16) (the ZK algorithm used by tornado cash) looks like the following:

$$
e(A₁, B₂) = e(α₁, β₂) + e(L₁, γ₂) + e(C₁, δ₂) \quad\text{where}\quad
\begin{cases}
A₁, α₁, L₁, C₁ \in G_1 \\
B₂, β₂, γ₂, D₂ \in G_2
\end{cases}
$$

The meanings of the above variables is not critical at this point, but for your info:

- $A_1$ : Proof element in $G_1$
- $B_2$ : Proof element in $G_2$
- α₁, β₂, γ₂, δ₂ : Public parameters (trusted setup)
- $L_1$, $C_1$ : Terms derived from the proof and public inputs

The fact that the above can be written as the sum of "products" (elliptic curve bilinear pairing) is what matters. Specifically, we can write (rearrange) it as:

$$
0 = e(-A_1, B_2) + e(α₁, β₂) + e(L₁, γ₂) + e(C₁, δ₂)
$$

And this matches the precompile specification perfectly.

<hr>

### Arriving at the equation (FYI)
In the equation:

$$
e(A₁, B₂) = e(α₁, β₂) + e(L₁, γ₂) + e(C₁, δ₂)
$$

The above is written additively in $G_T$, which uses $0$ as the identity (additive identiy). But if we write it multiplicatively in $G_T$, which uses $1$ as the identity (multiplicative identity), we have:

$$
e(A₁, B₂) = e(α₁, β₂) \cdot e(L₁, γ₂) \cdot e(C₁, δ₂)
$$

Using the additive notation for $G_T$, we move $e(A_1, B_1)$ to the RHS by subtracting it on both sides:

$$
0 = -e(A_1, B_2) + e(α₁, β₂) + e(L₁, γ₂) + e(C₁, δ₂)
$$

Because the pairing is bilinear and alternating in the first slot:

$$
-e(A_1, B_2) = e(-A_1, B_2)
$$

Note that either inputs can be negated, and we will still get the multiplicative inverse of the bilinear pairing, but it is simpler to negate a $G_1$ point than a $G_2$ point. Additionally, a minus sign in the domain becomes “take the multiplicative inverse” in the target (i.e. negation in $G_1$ translates to inversion in $G_T$). So technically:

$$
-e(A_1, B_2) = e(-A_1, B_2) = e(A_1, B_2)^{-1}
$$

This gives the equation:

$$
0 = e(-A_1, B_2) + e(α₁, β₂) + e(L₁, γ₂) + e(C₁, δ₂)
$$

Which, when we convert back to the multiplicative notation used in EIP-197, is "technically" the same as:

$$
1 = e(A_1, B_2)^{-1} \cdot e(α₁, β₂) \cdot e(L₁, γ₂) \cdot e(C₁, δ₂)
$$

<hr>

It is not just Groth16, most ZK algorithms have verification formula that looks like the above, which is why the precompile was designed to work with sums of pairings, rather than return the value of a single pairing.

If we look at the verification code of [Tornado Cash](https://www.rareskills.io/post/how-does-tornado-cash-work), we can see it is doing the same:

$$
0 = e(-A, B) + e(α \cdot G_1, β \cdot G_2) + e(L, γ \cdot G_2) + e(C, δ \cdot G_2)
$$

```solidity
    return Pairing.pairing(
        Pairing.negate(_proof.A),
        _proof.B,
        vk.alfa1,
        vk.beta2,
        vk_x,
        vk.gamma2,
        _proof.C,
        vk.delta2
    );
```

Inside the `pairing` function is where the call to `address(8)` is done to complete the bilinear pairing calculation and to determine if the proof is valid or not.

Sometimes, the group $G_T$ is referred to as $G_{12}$ in the context of EIP-197.

### Sum of Discrete Logarithms
The key insight here is the linear relationships in the exponents of the pairings:

$$
ab + cd = 0
$$

Then it must also be true, in the $G_{12}$ group that:

$$
A_1B_2 + C_1D_2 = 0_{12} \quad\text{where}\quad A_1,C_1 \in G_1, \ B_2,D_2 \in G_2
$$

For example, valid proofs satisfy algebraic constraints such as the above for secret scalars $a$, $b$, $c$, $d$.

This translates to:

$$
e(A_1, B_2) \cdot e(C_1, D_2) = 1 \quad\text{(in multiplicative notation)}
$$

Where $A_1 = aG_1$, $B_2 = bG_2$, $C_1 = cG_1$, and $D_2 = dG_2$.

Instead of solving for $a$, $b$, $c$, and $d$, the precompile checks if the product of the pairings equals $1$ (the multiplicative identity in $G_T$), which indirectly verifies that $ab + cd = 0$.

That is, the precompile computes:

$$
e(A_1, B_2) \cdot e(C_1, D_2) \stackrel{?}{=} 1
$$

Which, expressed additively (in exponents):

$$
e(G_1, G_2)^{ab} \cdot e(G_1, G_2)^{cd} = e(G_1, G_2)^{ab+cd} = 1
$$

The precompile isn’t actually computing the discrete logarithm, it’s simply checking if the sum of pairings is zero.

And the sum of pairings is zero if and only if the sum of the products of the discrete logarithms is zero. I.e. this hold if and only if $ab + cd = 0$.

## End to End Example of Bilinear Pairings with Python and Solidity
In many verification circuits like Groth16, PLONK, we actually want to check an equality such as:

$$
ab = cd
$$

This will be encoded by negating one of the $G_1$ points before it goes into the pairing precompile:

$$
(-A_1, B_2, C_1, D_2) = (-aG_1, bG_2, cG_1, dG_2)
$$

As shown earlier, negating a point flips the sign of its scalar. The precompile now checks:

$$
e(-A_1, B_2) \cdot e(C_1, D_2) = e(G_1, G_2)^{-ab+cd} \stackrel{?}{=} 1_{G_T}
$$

Which is true if and only if:

$$
-ab + cd \equiv 0 \quad(\text{mod} \ r) \quad \leftrightarrow \quad ab \equiv cd \quad(\text{mod} \ r)
$$

Consider the discrete logarithms: `a`, `b`, `c`, and `d`.

```
a = 4
b = 3
c = 6
d = 2

-ab + cd = 0
```

Putting it into formula, we can get:

$$
A_1B_2 + C_1D_1 = e(-aG_1,bG_2) + e(cG_1,dG_2) = 0
$$

In Python, this will equate to:
```python
from py_ecc.bn128 import neg, multiply, G1, G2
a = 4
b = 3
c = 6
d = 2

# negate G1 * a to make the equation sum up to 0
print(neg(multiply(G1, a)))
#(3010198690406615200373504922352659861758983907867017329644089018310584441462, 17861058253836152797273815394432013122766662423622084931972383889279925210507)

print(multiply(G2, b))
# ((2725019753478801796453339367788033689375851816420509565303521482350756874229, 7273165102799931111715871471550377909735733521218303035754523677688038059653), (2512659008974376214222774206987427162027254181373325676825515531566330959255, 957874124722006818841961785324909313781880061366718538693995380805373202866))

print(multiply(G1, c))
# (4503322228978077916651710446042370109107355802721800704639343137502100212473, 6132642251294427119375180147349983541569387941788025780665104001559216576968)

print(multiply(G2, d))
# ((18029695676650738226693292988307914797657423701064905010927197838374790804409, 14583779054894525174450323658765874724019480979794335525732096752006891875705), (2140229616977736810657479771656733941598412651537078903776637920509952744750, 11474861747383700316476719153975578001603231366361248090558603872215261634898))
```

The output in structured format:
```solidity
aG1_x = 3010198690406615200373504922352659861758983907867017329644089018310584441462,
aG1_y = 17861058253836152797273815394432013122766662423622084931972383889279925210507,

bG2_x1 = 2725019753478801796453339367788033689375851816420509565303521482350756874229,
bG2_x2 = 7273165102799931111715871471550377909735733521218303035754523677688038059653,
bG2_y1 = 2512659008974376214222774206987427162027254181373325676825515531566330959255,
bG2_y2 = 957874124722006818841961785324909313781880061366718538693995380805373202866,

cG1_x = 4503322228978077916651710446042370109107355802721800704639343137502100212473,
cG1_y = 6132642251294427119375180147349983541569387941788025780665104001559216576968,

dG2_x1 = 18029695676650738226693292988307914797657423701064905010927197838374790804409,
dG2_x2 = 14583779054894525174450323658765874724019480979794335525732096752006891875705,
dG2_y1 = 2140229616977736810657479771656733941598412651537078903776637920509952744750,
dG2_y2 = 11474861747383700316476719153975578001603231366361248090558603872215261634898
```

The individual discrete logarithm values are now encrypted into points in the $G_1$ and $G_2$ groups. And someone else, or another program, can verify that we have computed $e(A_1, B_2) \cdot e(C_1, D_2) = 0$ correctly without even knowing the individual values of `a`, `b`, `c`, or `d`.

The following is a Solidity smart contract that uses the ecPairing precompile (`0x08`) to confirm that we computed the euqations with valid values.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

contract Pairings {
    /**
     * returns true if == 0 (-ab + cd = 0)
     * returns false if != 0 (-ab + cd =/= 0)
     * reverts with "Wrong pairing" if invalid pairing
    */
    function run(uint256[12] memory input) public view returns (bool) {
        //staticcall(gas, addr, argsOffset, argsSize, retOffset, retSize)
        //argsOffset: `input` -> the pointer of the input array (uint256[12])
        //argsSize: `0x0180` -> 384 bytes
        //retOffset: `input` -> reuse the already-allocated memory from `input`
        assembly {
            let success := staticcall(gas(), 0x08, input, 0x0180, input, 0x20)
            if success {
                return(input, 0x20)
            }
        }
        revert("Wrong pairing");
    }   
}

```

And we use the following Foundry test to deploy and call the `Pairings` contract, to confirm the ecPairing calculation.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import "forge-std/Test.sol";
import "../src/Pairings.sol";

contract PairingsTest is Test {
    Pairings pairings;

    function setUp() public {
        pairings = new Pairings();
    }

    function testPairings() public view {
        uint256 aG1_x = 3010198690406615200373504922352659861758983907867017329644089018310584441462;
        uint256 aG1_y = 17861058253836152797273815394432013122766662423622084931972383889279925210507;

        uint256 bG2_x1 = 2725019753478801796453339367788033689375851816420509565303521482350756874229;
        uint256 bG2_x2 = 7273165102799931111715871471550377909735733521218303035754523677688038059653;
        uint256 bG2_y1 = 2512659008974376214222774206987427162027254181373325676825515531566330959255;
        uint256 bG2_y2 = 957874124722006818841961785324909313781880061366718538693995380805373202866;

        uint256 cG1_x = 4503322228978077916651710446042370109107355802721800704639343137502100212473;
        uint256 cG1_y = 6132642251294427119375180147349983541569387941788025780665104001559216576968;

        uint256 dG2_x1 = 18029695676650738226693292988307914797657423701064905010927197838374790804409;
        uint256 dG2_x2 = 14583779054894525174450323658765874724019480979794335525732096752006891875705;
        uint256 dG2_y1 = 2140229616977736810657479771656733941598412651537078903776637920509952744750;
        uint256 dG2_y2 = 11474861747383700316476719153975578001603231366361248090558603872215261634898;

        uint256[12] memory points = [
            aG1_x,
            aG1_y,
            bG2_x2,
            bG2_x1,
            bG2_y2,
            bG2_y1,
            cG1_x,
            cG1_y,
            dG2_x2,
            dG2_x1,
            dG2_y2,
            dG2_y1
        ];

        bool x = pairings.run(points);
        console2.log("result:", x);
    }
}
```

Note that the way $G_2$ points are arranged is not the same way Python lays out the $G_2$ points.

This passes and prints out `true` to the console.

Notice that the points: `aG1_x`, `aG1_y`, `bG2_x2`, `bG2_x1`, `bG2_y2`, `bG2_y1`, and etc, have been labeled by their variable name (`a`, `b`, `c`, `d`), which group they belong (`G1`, `G2`), and if they represent an `x` or a `y` of the elliptic curve point (for `G1`: `_x`, `_y`, and for `G2`: `_x1`, `_x2`, `_y1`, `_y2`).

Also note that the exPairing precompile does not expect or require an array, and that using in-line assembly as above is optional. One can also do the same as such:
```solidity
//In Pairings.sol
//Change parameter to `bytes calldata`
function run(bytes calldata input) public view returns (bool) {
    // optional, the precompile checks this too and reverts (with no error) if false, this helps narrow down possible errors
    if (input.length % 192 != 0) revert("Points must be a multiple of 6");
    (bool success, bytes memory data) = address(0x08).staticcall(input);
    if (success) return abi.decode(data, (bool));
    revert("Wrong pairing");
}

//In PairingsTest.sol
function testPairings() public view {
    uint256 aG1_x = 3010198690406615200373504922352659861758983907867017329644089018310584441462;
    uint256 aG1_y = 17861058253836152797273815394432013122766662423622084931972383889279925210507;

    uint256 bG2_x1 = 2725019753478801796453339367788033689375851816420509565303521482350756874229;
    uint256 bG2_x2 = 7273165102799931111715871471550377909735733521218303035754523677688038059653;
    uint256 bG2_y1 = 2512659008974376214222774206987427162027254181373325676825515531566330959255;
    uint256 bG2_y2 = 957874124722006818841961785324909313781880061366718538693995380805373202866;

    uint256 cG1_x = 4503322228978077916651710446042370109107355802721800704639343137502100212473;
    uint256 cG1_y = 6132642251294427119375180147349983541569387941788025780665104001559216576968;

    uint256 dG2_x1 = 18029695676650738226693292988307914797657423701064905010927197838374790804409;
    uint256 dG2_x2 = 14583779054894525174450323658765874724019480979794335525732096752006891875705;
    uint256 dG2_y1 = 2140229616977736810657479771656733941598412651537078903776637920509952744750;
    uint256 dG2_y2 = 11474861747383700316476719153975578001603231366361248090558603872215261634898;

    // Use abi.encode
    bytes memory points = abi.encode(
        aG1_x,
        aG1_y,
        bG2_x2,
        bG2_x1,
        bG2_y2,
        bG2_y1,
        cG1_x,
        cG1_y,
        dG2_x2,
        dG2_x1,
        dG2_y2,
        dG2_y1
    );

    bool x = pairings.run(points);
    console2.log("result:", x);
}
```

This will pass and return true just like the initial implementation because it sends the exact same calldata to the precompile.

The only difference is that in the first implementation, the test file sends an array of points to the pairing contract which uses inline-assembly to slice off the first 32 bytes (array length) and sends the rest to the precompile. (It is not actually slicing per se, it is because `input` already points at the first 32-byte word of the fixed-length array in memory: `uint256[12]`)

And in the second implementation, the test file sends the abi encoded points to the pairing contract which forwards it as it is to the precompile.