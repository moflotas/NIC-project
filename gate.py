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


def make_gate(gate_name: str):
    gate_name = gate_name.lower()
    if gate_name == 'and':
        return Gate(2, 1, lambda inputs: [inputs[0] and inputs[1]])
    elif gate_name == 'or':
        return Gate(2, 1, lambda inputs: [inputs[0] or inputs[1]])
    elif gate_name == 'not':
        return Gate(1, 1, lambda inputs: [not inputs[0]])
    elif gate_name == 'xor':
        return Gate(2, 1, lambda inputs: [inputs[0] ^ inputs[1]])
    elif gate_name == 'nor':
        return Gate(2, 1, lambda inputs: [not inputs[0] and not inputs[1]])
    elif gate_name == 'nand':
        return Gate(2, 1, lambda inputs: [not inputs[0] or not inputs[1]])
    else:
        raise Exception(f"Gate name '{gate_name}' is undefined.")
