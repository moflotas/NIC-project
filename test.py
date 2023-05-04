from find_circuit import find_circuit
from utils import plot_modi_tree, same_modi_count
from circuit import Circuit


def sum3(a0, a1, a2, b0, b1, b2):
    a = a0 * 4 + a1 * 2 + a2
    b = b0 * 4 + b1 * 2 + b2
    z = a + b
    z_bits = [int(j) for j in bin(z)[2:].rjust(4, '0')]
    return z_bits


def sum2(a0, a1, b0, b1):
    a = a0 * 2 + a1
    b = b0 * 2 + b1
    z = a + b
    z_bits = [int(j) for j in bin(z)[2:].rjust(3, '0')]
    return z_bits


def sum1(a0, b0):
    z = a0 + b0
    z_bits = [int(j) for j in bin(z)[2:].rjust(2, '0')]
    return z_bits


def or_and(x, y):
    return x and y, x or y


def mod4(x, y, z, w):
    return z, w


def not_and(x, y):
    return not x, (not x) and y


def not_or(x, y):
    return not x, (not x) or y


def xor3(x, y, z):
    return x and y, x or y, (x and not y) or (y and not x)


def eq2(x, y, z):
    return x == y == z,


def full_adder(x, y, z):
    return [int(j) for j in bin(x + y + z)[2:].rjust(2, '0')]


def ex1(a, b, c, d):
    return ((b and c) or (d ^ b)) ^ (a or (not (d or c))),


hof, pop, log = find_circuit(ex1, pop_size=5000, gens=100)
best_ind = hof[0]
str(best_ind)
plot_modi_tree(best_ind, visualize_output=True)
print(best_ind, best_ind.fitness)
