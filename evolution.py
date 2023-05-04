from GA import mutate, correctness_fitness
from circuit import Circuit, half_adder, full_adder
from random import sample


def init_individual(c: Circuit):
    return [Circuit(no_inputs=c.no_inputs, no_outputs=c.no_outputs, no_layers=c.no_layers), None]


def init_population(circuit: Circuit, pop_size: int):
    population = []
    for _ in range(pop_size):
        population.append(init_individual(circuit))
    
    return population


def evolve(circuit_true: Circuit, pop_size: int, generations: int, edge_p: float = 0.25, replace_p: float = 0.25,
           tournsize=3,  verbose=False):
    population = init_population(circuit_true, pop_size)
    for j in range(generations):
        # Mutation
        for i in range(pop_size):
            c = population[i][0]
            population.append([mutate(c, edge_prob=edge_p, replace_prob=replace_p), None])
    
        # Selection
        new_population = []
        for i in range(pop_size):
            offsprings = sample(population=population, k=tournsize)
            
            best_offspring = (None, -1)
            for of in offsprings:
                if not of[1]:
                    of[1] = correctness_fitness(circuit_true, of[0])
                if of[1] > best_offspring[1]:
                    best_offspring = of.copy()
            
            new_population.append(best_offspring)
        
        population = sorted(new_population, key=lambda x: x[1])

        # Debug
        if verbose and j % 10 == 0:
            print(f'{j}) Best: {population[0]}\n\n')
    
    return population


pop = evolve(full_adder, pop_size=200, generations=500, verbose=True)
    