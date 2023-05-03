from deap.gp import graph
from networkx.drawing.nx_agraph import graphviz_layout

import matplotlib.pyplot as plt
import networkx as nx


def nodes_count(individual):
    count_size = 0
    count_gate = 0
    for node in individual:
        if node.arity != 0:
            count_size += 1
            if 'modi' not in node.name:
                count_gate += 1

    return count_size, count_gate


def plot_modi_tree(individual):
    nodes, edges, labels = graph(individual)

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    pos = graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos, labels)

    plt.title(str(individual) + '\n' + str(individual.fitness))
    plt.show()
