from circuit import Circuit, half_adder, full_adder
from inspect import signature
from gates import *
from random import random, choice, randint
from copy import deepcopy

import itertools


# def arguments(method):
#     return list(signature(method).parameters.keys())


def mutate(old_circuit: Circuit, edge_prob: float = 0.2, replace_prob: float = 0.2):
    circuit: Circuit = deepcopy(old_circuit)

    if random() < edge_prob:
        chosen_layer = randint(0, circuit.no_layers - 1)
        chosen_gate = randint(0, circuit.max_gates_per_layer - 1)

        if len(circuit.hidden_layers[chosen_layer][chosen_gate][1]) > 0:
            circuit.hidden_layers[chosen_layer][chosen_gate][1][randint(0, len(circuit.hidden_layers[chosen_layer][chosen_gate][1]) - 1)] = randint(
                0, (circuit.no_inputs if chosen_layer == 0 else circuit.max_gates_per_layer) - 1)

    if random() < replace_prob:
        chosen_layer = randint(0, circuit.no_layers - 1)
        chosen_gate = randint(0, circuit.max_gates_per_layer - 1)

        circuit.hidden_layers[chosen_layer][chosen_gate][0] = choice(
            circuit.gates)
        input_indecies = []

        for _ in range(circuit.hidden_layers[chosen_layer][chosen_gate][0].no_inputs):
            input_indecies.append(randint(
                0, (circuit.no_inputs if chosen_layer == 0 else circuit.max_gates_per_layer) - 1))

        circuit.hidden_layers[chosen_layer][chosen_gate][1] = input_indecies

    return circuit


def correctness_fitness(true_circuit: Circuit, test_circuit: Circuit):
    if true_circuit.no_inputs != test_circuit.no_inputs:
        raise ValueError(
            f"Expected {true_circuit.no_inputs} inputs, got {test_circuit.no_inputs}")

    if true_circuit.no_outputs != test_circuit.no_outputs:
        raise ValueError(
            f"Expected {true_circuit.no_outputs} outputs, got {test_circuit.no_outputs}")

    total_correct = 0
    for cur_inputs in [p for p in itertools.product([True, False], repeat=true_circuit.no_inputs)]:
        total_correct += sum([i == j for i, j in zip(true_circuit(*
                             cur_inputs), test_circuit(*cur_inputs))])

    return total_correct / (2 ** true_circuit.no_inputs * true_circuit.no_outputs)


if __name__ == "__main__":
    random_circ_1 = Circuit(no_inputs=2, no_outputs=2,
                            no_layers=2, max_gates_per_layer=5, output_gates=[0, 1])
    random_circ_2 = Circuit(no_inputs=2, no_outputs=2,
                            no_layers=2, max_gates_per_layer=6, output_gates=[0, 1])

    max_fitness = 0
    while max_fitness < 1:
        if correctness_fitness(random_circ_1, random_circ_2) > max_fitness:
            max_fitness = correctness_fitness(random_circ_1, random_circ_2)
            print(max_fitness)
        # random_circ_1 = mutate(random_circ_1, 1, 1)
        random_circ_2 = mutate(random_circ_2, 1, 1)
        
    print(correctness_fitness(random_circ_1, random_circ_2))
