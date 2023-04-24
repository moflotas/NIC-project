from typing import Any, Iterable


class Gate:
    def __init__(self, no_inputs: int, no_outputs: int, boolean_function) -> None:
        # 'no' prefix means 'number of'
        self.no_inputs = no_inputs
        self.no_outputs = no_outputs
        self.boolean_function = boolean_function

    def _evaluate(self, inputs: Iterable[bool]) -> Iterable[bool]:
        if len(inputs) != self.no_inputs:
            raise ValueError(
                f"Expected {self.no_inputs} inputs, got {len(inputs)}")
        
        inputs = [bool(i) for i in inputs]
        if not all(isinstance(i, bool) for i in inputs):
            raise ValueError(
                f"Expected True/False inputs, got {inputs}")

        return self.boolean_function(inputs)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._evaluate(args)


# false_circ = Circuit(0, 1, lambda inputs: [False])
# true_circ = Circuit(0, 1, lambda inputs: [True])

and_gate = Gate(2, 1, lambda inputs: [inputs[0] and inputs[1]])
or_gate = Gate(2, 1, lambda inputs: [inputs[0] or inputs[1]])
not_gate = Gate(1, 1, lambda inputs: [not inputs[0]])
xor_gate = Gate(2, 1, lambda inputs: [inputs[0] ^ inputs[1]])

nor_gate = Gate(2, 1, lambda inputs: [not inputs[0] and not inputs[1]])
nand_gate = Gate(2, 1, lambda inputs: [not inputs[0] or not inputs[1]])

print(nor_gate(False, False))
print(nor_gate(False, True))
print(nor_gate(1, 0))
print(nor_gate(1, 1))