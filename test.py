from find_circuit import find_circuit
from utils import plot_modi_tree, same_modi_count


def sum3(a0, a1, a2, b0, b1, b2):
    a = a0 * 4 + a1 * 2 + a2
    b = b0 * 4 + b1 * 2 + b2
    z = a + b
    z_bits = [int(j) for j in bin(z)[2:].rjust(4, '0')]
    return z_bits


def or_and(x, y):
    return x and y, x or y


def mod4(x, y, z, w):
    return z, w


def not_and(x, y):
    return not x, (not x) and y


def not_or(x, y):
    return not x, (not x) or y


hof, pop, log = find_circuit(or_and, pop_size=1000, gens=300)
best_ind = hof[0]

plot_modi_tree(best_ind, visualize_output=True)
print(best_ind, best_ind.fitness)
