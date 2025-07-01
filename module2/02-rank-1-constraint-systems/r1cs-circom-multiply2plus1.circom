pragma circom 2.0.8;

// z = xy + 2
template Multiply2Plus1() {
    signal input x;
    signal input y;

    signal output z;

    z <== x * y + 2;
}

component main = Multiply2Plus1();

/**
% circom r1cs-circom-multiply2plus1.circom --r1cs --sym

template instances: 1
non-linear constraints: 1
linear constraints: 0
public inputs: 0
private inputs: 2
public outputs: 1
wires: 4
labels: 4 <--- [ 1, z, x, y ]
Written successfully: ./r1cs-circom-multiply2plus1.r1cs
Written successfully: ./r1cs-circom-multiply2plus1.sym
*/