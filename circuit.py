from gates import all_gates, false_circ, true_circ, and_gate, or_gate, not_gate, xor_gate, nor_gate, nand_gate, repeater_gate
from gate import Gate
from random import randint, choice
from typing import Any, Iterable
import itertools


class Circuit:
    def __init__(self, no_inputs: int, no_outputs: int, no_layers: int, max_gates_per_layer: int = None, gates: list[Gate] = all_gates, hidden_layers: list[list[Gate]] = None, output_gates: list[int] = None) -> None:
        
        
        self.no_inputs = no_inputs
        self.no_outputs = no_outputs
        self.no_layers = no_layers
        self.gates = gates

        # defaulting to 2x of no_inputs
        if not max_gates_per_layer:
            self.max_gates_per_layer = 2 * self.no_inputs
        
        if hidden_layers:
            self.hidden_layers = hidden_layers
        else:
            self.hidden_layers = [[[choice(self.gates)] for _ in range(
                self.max_gates_per_layer)] for _ in range(no_layers)]

            for layer in self.hidden_layers:
                for gate in layer:
                    gate.append([randint(0, self.no_inputs - 1)
                                for _ in range(gate[0].no_inputs)])

        if output_gates:
            self.output_layer_indices = output_gates
        else:
            self.output_layer_indices = [
                randint(0, self.max_gates_per_layer - 1) for _ in range(no_outputs)]

    def _evaluate(self, inputs: Iterable[bool]) -> Iterable[bool]:
        if len(inputs) != self.no_inputs:
            raise ValueError(
                f"Expected {self.no_inputs} inputs, got {len(inputs)}")

        inputs = [bool(i) for i in inputs]
        if not all(isinstance(i, bool) for i in inputs):
            raise ValueError(
                f"Expected True/False inputs, got {inputs}")

        layer_results = [inputs]

        for layer in self.hidden_layers:
            layer_results.append([])
            for gate, input_indices in layer:
                layer_results[-1].append(*gate(*[layer_results[-2][i]
                                         for i in input_indices]))

        return [layer_results[-1][i] for i in self.output_layer_indices]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._evaluate(args)
    
    def __repr__(self) -> str:
        return '\n'.join(str(i) for i in self.hidden_layers) + '\n' + str(self.output_layer_indices)


half_adder = Circuit(no_inputs=2, no_outputs=2, no_layers=1,
                     hidden_layers=[[[and_gate, [0, 1]], [xor_gate, [0, 1]]]], output_gates=[0, 1])

full_adder_hidden_layers = [
    [[xor_gate, [0, 1]], [repeater_gate, [2]], [and_gate, [0, 1]]],
    [[xor_gate, [0, 1]], [and_gate, [0, 1]], [repeater_gate, [2]]],
    [[repeater_gate, [0]], [or_gate, [1, 2]], [repeater_gate, [2]]]
]
full_adder = Circuit(no_inputs=3, no_outputs=2, no_layers=3,
                     hidden_layers=full_adder_hidden_layers, output_gates=[1, 0])



if __name__ == '__main__':
    x = [True, False]
    for inp in [p for p in itertools.product(x, repeat=2)]:
        print(inp, half_adder._evaluate(inp))

    print()

    for inp in [p for p in itertools.product(x, repeat=3)]:
        print(inp, full_adder._evaluate(inp))
