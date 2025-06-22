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
$$
P = pG \\
Q = qG \\
R = rG
$$
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

(FYI: output of a bilinear pairing is usually an element of a multiplicative group of a finite field)

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
$$
\underbrace{aP}_{\text{add }a\text{ times}}
\;\xrightarrow{\;e\;}
\underbrace{e(P,Q)^a}_{\text{multiply }a\text{ times}}
$$

Since:
$$
\begin{aligned}
e(aG,bG) &= e(G,bG)^a \\[4pt]
            &= \bigl(e(G,\, G)^a\bigr)^{\,b} \\[4pt]
            &= e(G,\, G)^{ab}\, .
\end{aligned}
$$

And as such:
$$
e(abG,G) = e(G,G)^{ab} \\[8pt]
e(G,abG) = e(G,G)^{ab}
$$

Thus we arrive at the elliptic curve bilinear pairing property:
$$
e(aG, bG) = e(abG, G) = e(G, abG)
$$
