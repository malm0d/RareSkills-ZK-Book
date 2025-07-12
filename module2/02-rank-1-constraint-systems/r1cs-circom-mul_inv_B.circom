pragma circom 2.0.8;

// z = 7x^(-2)
template Mul_inv_B() {
    signal input x;
    signal output z;

    signal v1;

    v1 <== x * x;

    z <-- 7 / v1;
    7 === z * v1;

    // Or, if we wanted to be more verbose:
    //
    // signal v1_inv;
    // v1_inv <-- 1 / v1;
    // 1 === v1 * v1_inv;
    // z <== 7 * v1_inv;
}

//circom r1cs-circom-mul_inv_B.circom --r1cs --sym
component main = Mul_inv_B();