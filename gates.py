from gate import Gate

false_circ = Gate(0, 1, lambda inputs: [False], name="constant_false")
true_circ = Gate(0, 1, lambda inputs: [True], name="constant_true")

and_gate = Gate(2, 1, lambda inputs: [inputs[0] and inputs[1]], name="and")
or_gate = Gate(2, 1, lambda inputs: [inputs[0] or inputs[1]], name="or")
not_gate = Gate(1, 1, lambda inputs: [not inputs[0]], name="not")
xor_gate = Gate(2, 1, lambda inputs: [inputs[0] ^ inputs[1]], name="xor")

nor_gate = Gate(2, 1, lambda inputs: [not inputs[0] and not inputs[1]], name="nor")
nand_gate = Gate(2, 1, lambda inputs: [not inputs[0] or not inputs[1]], name="nand")

repeater_gate = Gate(1, 1, lambda inputs: inputs, name="repeater")

all_gates = [false_circ, true_circ, and_gate, or_gate, not_gate, xor_gate, nor_gate, nand_gate, repeater_gate]

if __name__ == "__main__":
    print(nor_gate(False, False))
    print(nor_gate(False, True))
    print(nor_gate(1, 0))
    print(nor_gate(1, 1))