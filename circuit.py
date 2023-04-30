from inspect import signature
from collections.abc import Sized, Iterable


def arguments(method):
    return list(signature(method).parameters.keys())


def int_output(method):
    def _wrapper(*args, **kwargs):
        output = method(*args, **kwargs)
        if isinstance(output, Iterable):
            return [int(i) for i in output]
        else:
            return int(output)

    return _wrapper


class Circuit:
    def __init__(self, function):
        self.function = int_output(function)
        self.arg_names = arguments(function)
        self.num_inputs = len(self.arg_names)
        self.num_outputs = None
        self.inputs = []
        self.outputs = []
        for i in range(2 ** self.num_inputs):
            input_list = [int(j) for j in bin(i)[2:].rjust(self.num_inputs, '0')]
            output_list = self.function(*input_list)
            assert isinstance(output_list, Sized), 'Function output is not iterable'
            if self.num_outputs:
                assert len(output_list) == self.num_outputs, 'Function returns output of different sizes'
            else:
                self.num_outputs = len(output_list)

            self.inputs.append(input_list)
            self.outputs.append(output_list)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def fitness(self, function):
        valid = 0
        function = int_output(function)
        for i, inp in enumerate(self.inputs):
            valid += int(function(*inp) == self.outputs[i])

        return valid / len(self.inputs)
