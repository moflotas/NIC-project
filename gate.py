from typing import Any, Iterable

class Gate:
    def __init__(self, no_inputs: int, no_outputs: int, boolean_function, name: str) -> None:
        # 'no' prefix means 'number of'
        self.no_inputs = no_inputs
        self.no_outputs = no_outputs
        self.boolean_function = boolean_function
        self.name = name

    def _evaluate(self, inputs: Iterable[bool]) -> Iterable[bool]:
        if len(inputs) != self.no_inputs:
            raise ValueError(
                f"Expected {self.no_inputs} inputs, got {len(inputs)}")
        
        inputs = [bool(i) for i in inputs]
        if not all(isinstance(i, bool) for i in inputs):
            raise ValueError(
                f"Expected True/False inputs, got {inputs}")

        return self.boolean_function(inputs)

    def __repr__(self) -> str:
        return f"Gate(no_inputs={self.no_inputs}, no_outputs={self.no_outputs}, name={self.name})"
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._evaluate(args)
