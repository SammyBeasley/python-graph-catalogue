"""Construct NetworkX graphs with an explicit vertex order."""
import networkx as nx


def graph_from_edges(nodes, edges):
    """Return a new graph, preserving the supplied node and edge order."""
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    return graph
