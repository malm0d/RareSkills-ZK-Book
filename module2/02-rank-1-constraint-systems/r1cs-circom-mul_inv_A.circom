pragma circom 2.0.8;

// z = x^-1
template Mul_inv_A() {
    signal input x;
    signal output z;

    z <-- 1 / x;
    z * x === 1;

}

//circom r1cs-circom-mul_inv_A.circom --r1cs --sym
component main = Mul_inv_A();