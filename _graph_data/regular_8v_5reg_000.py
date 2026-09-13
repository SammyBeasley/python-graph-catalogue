# Connected simple 5-regular graphs on 8 vertices.
# Source: Markus Meringer, Regular Graphs, University of Bayreuth.
# https://www.mathe2.uni-bayreuth.de/markus/reggraphs.html
# M. Meringer, Fast Generation of Regular Graphs and Construction of Cages,
# Journal of Graph Theory 30, 137-146 (1999).
# Python conversion: Sammy Beasley. Keys are zero-based source-list indices.
# Vertices are 0, ..., 7; source edge order is preserved.

EDGES = {
    0: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 6), (2, 7), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)],
    1: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 6), (2, 3), (2, 5), (2, 7), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)],
    2: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 6), (2, 5), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5), (4, 6), (4, 7), (5, 7), (6, 7)],
}
