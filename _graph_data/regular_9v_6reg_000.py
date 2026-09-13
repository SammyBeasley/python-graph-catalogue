# Connected simple 6-regular graphs on 9 vertices.
# Source: Markus Meringer, Regular Graphs, University of Bayreuth.
# https://www.mathe2.uni-bayreuth.de/markus/reggraphs.html
# M. Meringer, Fast Generation of Regular Graphs and Construction of Cages,
# Journal of Graph Theory 30, 137-146 (1999).
# Python conversion: Sammy Beasley. Keys are zero-based source-list indices.
# Vertices are 0, ..., 8; source edge order is preserved.

EDGES = {
    0: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 7), (2, 8), (3, 5), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)],
    1: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 3), (2, 4), (2, 5), (2, 8), (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)],
    2: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 3), (2, 4), (2, 6), (2, 8), (3, 5), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)],
    3: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 7), (1, 8), (2, 5), (2, 6), (2, 7), (2, 8), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (4, 6), (4, 7), (4, 8), (5, 7), (5, 8), (6, 7), (6, 8)],
}
