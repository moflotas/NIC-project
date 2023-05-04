import operator
import numpy as np
import multiprocessing


from circuit import Circuit, int_output, arguments
from collections import Callable
from deap import gp, creator, base, tools, algorithms
from utils import nodes_count, dead_end_


def find_circuit(function: Callable, pop_size=300, gens=200, operators=None, verbose=True):
    circ = Circuit(function)

    pset = gp.PrimitiveSet("MAIN", circ.num_inputs)
    if not operators:
        operators = [operator.and_, operator.not_, operator.or_, operator.xor]
    # operators = [i for i in operators if i != operator.xor]
    for op in operators:
        arity = len(arguments(op))
        pset.addPrimitive(op, arity)

    args_map = {}
    for i in range(circ.num_inputs):
        args_map[f'ARG{i}'] = circ.arg_names[i]
    pset.renameArguments(**args_map)

    for i in range(circ.num_outputs):
        modi_i = gp.Modi(i)
        pset.addPrimitive(modi_i, 1, name=str(modi_i))

    pset.addPrimitive(dead_end_, 2, name='end')

    creator.create("FitnessMin", base.Fitness, weights=(1.0, -1.0))
    creator.create("Individual", gp.MultiOutputTree, num_outputs=circ.num_outputs, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=4)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    def eval_circuit(individual, circuit):
        # Transform the tree expression in a callable function
        func = int_output(toolbox.compile(expr=individual))
        valid_fitness = circuit.fitness(func)

        size_fitness, gate_fitness = nodes_count(individual)
        size_fitness = size_fitness if valid_fitness == 1 else np.inf
        gate_fitness = gate_fitness if valid_fitness == 1 else np.inf

        return valid_fitness, gate_fitness

    toolbox.register("evaluate", eval_circuit, circuit=circ)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePointLeafBiased, termpb=0.25)
    toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate("mate", gp.staticLimit(key=len, max_value=250))
    toolbox.decorate("mutate", gp.staticLimit(key=len, max_value=250))

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats_gates = tools.Statistics(lambda ind: nodes_count(ind)[1])
    mstats = tools.MultiStatistics(fitness=stats_fit, gates=stats_gates)
    mstats.register("avg", np.mean)
    mstats.register("max", np.max)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, gens, halloffame=hof, verbose=verbose, stats=mstats)

    return hof, pop, log
