pragma circom 2.0.8;

// z = 3x^(2)y + 5xy - x - 2y + 3
template Poly() {
    signal input x;
    signal input y;

    signal v1;
    signal v2;
    
    signal output z;

    v1 <== 3 * x * x;
    v2 <== v1 * y;

    z <== v2 + (5 * x * y) - x - (2 * y) + 3;

}

component main = Poly();

/**
% circom r1cs-circom-poly.circom --r1cs --wasm --sym

template instances: 1
non-linear constraints: 3
linear constraints: 0
public inputs: 0
private inputs: 2
public outputs: 1
wires: 6
labels: 6 <--- [ 1, z, x, y, v1, v2 ]
Written successfully: ./r1cs-circom-poly.r1cs
Written successfully: ./r1cs-circom-poly.sym
Written successfully: ./r1cs-circom-poly_js/r1cs-circom-poly.wasm
Everything went okay
*/

/**
These are all the constraints in the R1CS encoded by Circom.

a = [ 1, z, x, y, v1, v2 ]

snarkjs r1cs print r1cs-circom-poly.r1cs
[INFO]  snarkJS: [ 21888242871839275222246405745257275088548364400416034343698204186575808495614main.x ] * [ main.x ] - [ 21888242871839275222246405745257275088548364400416034343698204186575808495616main.v1 ] = 0
[INFO]  snarkJS: [ 21888242871839275222246405745257275088548364400416034343698204186575808495616main.v1 ] * [ main.y ] - [ 21888242871839275222246405745257275088548364400416034343698204186575808495616main.v2 ] = 0
[INFO]  snarkJS: [ 21888242871839275222246405745257275088548364400416034343698204186575808495612main.x ] * [ main.y ] - 
[ 31 +21888242871839275222246405745257275088548364400416034343698204186575808495616main.z +21888242871839275222246405745257275088548364400416034343698204186575808495616main.x +21888242871839275222246405745257275088548364400416034343698204186575808495615main.y +main.v2 ] = 0

Effectively:
1) -3x * x - (-v1) = 0'
2) -v1 * y - (-v2) = 0
3) -5x * y - (3 + -z + -x + -2y + v2) = 0

Which are equivalent to the constraints derived in example 5.

Note that 31 is actually encoding 3, i.e. the verifier sees 31 as: (3 * scaling factor) % p
BUT WE DONT NEED TO KNOW THIS.
*/