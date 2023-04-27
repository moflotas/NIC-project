import numpy
import operator
import random
from deap import gp, creator, base, tools, algorithms

num_outputs = 2
pset = gp.PrimitiveSet("MAIN", 2)
pset.addPrimitive(numpy.add, 2, name="vadd")
pset.addPrimitive(numpy.subtract, 2, name="vsub")

for i in range(num_outputs):
    modi_i = gp.Modi(i)
    pset.addPrimitive(modi_i, 1, name=str(modi_i))

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.MultiOutputTree, num_outputs=2, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual, points):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    er1, er2 = 0, 0
    for x, y in points:
        true1, true2 = x + y, abs(x - y)
        pred1, pred2 = func(x, y)
        er1 += (true1 - pred1) ** 2
        er2 += (true2 - pred2) ** 2
    return er1 + er2,


toolbox.register("evaluate", evalSymbReg, points=[(random.randint(0, 20), random.randint(0, 20)) for _ in range(10)])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

tree = toolbox.individual()
print(f"tree: {tree}")
print(f"eval: {toolbox.evaluate(tree)}")

stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)

pop = toolbox.population(n=300)
hof = tools.HallOfFame(1)
pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 400, halloffame=hof, verbose=True, stats=mstats)

print(pop[0], toolbox.evaluate(pop[0]))
