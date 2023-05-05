from deap.gp import graph
from networkx.drawing.nx_agraph import graphviz_layout

import matplotlib.pyplot as plt
import networkx as nx

from collections import Counter


BIG_INT = int(1e6)


def dead_end_(x, y):
    return BIG_INT


def same_modi_count(individual):
    count = Counter()
    for node in individual:
        if 'modi' in node.name:
            count[node.name] += 1

    return max(count.values()) if count else 0


def nodes_count(individual):
    count_size = 0
    count_gate = 0
    for node in individual:
        if node.arity != 0:
            count_size += 1
            if 'modi' not in node.name and 'end' not in node.name:
                count_gate += 1

    or_count = str(individual).count('+')

    return count_size, count_gate + or_count


def plot_modi_tree(individual, visualize_output=False):
    nodes, edges, labels = graph(individual)

    if visualize_output:
        modis = [i for i in labels if 'modi' in labels[i]]
        modi_edges = [edge for edge in edges if edge[1] in modis]
        edges = [edge for edge in edges if edge[1] not in modis]
        for i in range(len(edges)):
            edge = edges[i]
            if edge[0] in modis:
                for m_edge in modi_edges:
                    if edge[0] == m_edge[1]:
                        edges.append((m_edge[0], edge[1]))

        # new nodes
        outs = [nodes[-1] + 1 + i for i in range(individual.num_outputs)]
        for i in range(individual.num_outputs):
            labels[outs[i]] = 'out' + str(i)
        nodes += outs
        modi_map = {}
        for modi in modis:
            modi_index = int(labels[modi].replace('modi', ''))
            modi_map[modi] = modi_index
        # new edges
        for i in range(len(edges)):
            f, t = edges[i]
            if f in modi_map:
                f = outs[modi_map[f]]
            if t in modi_map:
                t = outs[modi_map[t]]
            edges[i] = (f, t)
        # delete modis
        nodes = [n for n in nodes if n not in modis]
        labels = {n: labels[n] for n in labels if n not in modis}

        # delete ends
        ends = [i for i in labels if 'end' in labels[i]]
        nodes = [n for n in nodes if n not in ends]
        edges = [e for e in edges if e[0] not in ends and e[1] not in ends]
        labels = {n: labels[n] for n in labels if n not in ends}

        # delete alone nodes
        flatten_edges = [item for sublist in edges for item in sublist]
        nodes = [n for n in nodes if n in flatten_edges]
        labels = {n: labels[n] for n in labels if n in flatten_edges}

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g = nx.reverse_view(g)
    pos = graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos, node_size=700)
    nx.draw_networkx_edges(g, pos, arrowsize=24)
    nx.draw_networkx_labels(g, pos, labels)

    plt.title(str(individual) + '\n' + str(individual.fitness))
    plt.show()
