# Connected simple regular graphs converted to NetworkX by Sammy Beasley.
# Collections (vertices, degree):
# (6,3), (7,4), (8,3), (8,4), (8,5), (9,4), (9,6),
# (10,3), (10,4), (10,5), (10,6), (10,7), (11,4), (11,6),
# (12,3), (12,4), (12,5), (13,4), (14,3), (14,4), (16,3), (18,3).
# Source: Markus Meringer, Regular Graphs, University of Bayreuth.
# https://www.mathe2.uni-bayreuth.de/markus/reggraphs.html
# Cite: M. Meringer, Fast Generation of Regular Graphs and Construction of
# Cages, Journal of Graph Theory 30, 137-146 (1999).
# Explicit edges are in _graph_data/regular_<collection>_<part>.py.
# Graph indices are zero-based; vertex labels and collection order are retained.

from importlib import import_module
import re
from graph_utils import graph_from_edges


GRAPH_COUNTS = {
    (6, 3): 2, (7, 4): 2, (8, 3): 5, (8, 4): 6, (8, 5): 3,
    (9, 4): 16, (9, 6): 4,
    (10, 3): 19, (10, 4): 59, (10, 5): 60, (10, 6): 21, (10, 7): 5,
    (11, 4): 265, (11, 6): 266,
    (12, 3): 85, (12, 4): 1544, (12, 5): 7848, (13, 4): 10778,
    (14, 3): 509, (14, 4): 88168, (16, 3): 4060, (18, 3): 41301,
}
_PART_SIZE = 1000


def get_graph(n, degree, index):
    """Return a fresh graph at a zero-based index in a regular collection."""
    count = GRAPH_COUNTS.get((n, degree))
    if count is None:
        raise ValueError(f'Unknown regular collection: ({n}, {degree})')
    if not isinstance(index, int) or not 0 <= index < count:
        raise IndexError(f'Graph index must be an integer in 0..{count - 1}')
    part = import_module(f'_graph_data.regular_{n}v_{degree}reg_{index // _PART_SIZE:03d}')
    return graph_from_edges(range(n), part.EDGES[index])


def iter_graphs(n, degree):
    """Yield fresh graphs in source order without building the full list."""
    if (n, degree) not in GRAPH_COUNTS:
        raise ValueError(f'Unknown regular collection: ({n}, {degree})')
    for index in range(GRAPH_COUNTS[n, degree]):
        yield get_graph(n, degree, index)


def get_graphs(n, degree):
    """Return the complete regular collection as a list of NetworkX graphs."""
    return list(iter_graphs(n, degree))


def __getattr__(name):
    # Preserve the collection names used in the research notebooks.
    match = re.fullmatch(r'all_(\d+)v_(\d+)reg_graphs', name)
    if match and tuple(map(int, match.groups())) in GRAPH_COUNTS:
        return get_graphs(*map(int, match.groups()))
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


__all__ = ['GRAPH_COUNTS', 'get_graph', 'get_graphs', 'iter_graphs'] + [
    f'all_{n}v_{degree}reg_graphs' for n, degree in GRAPH_COUNTS
]
