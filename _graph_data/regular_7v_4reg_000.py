# Connected simple 4-regular graphs on 7 vertices.
# Source: Markus Meringer, Regular Graphs, University of Bayreuth.
# https://www.mathe2.uni-bayreuth.de/markus/reggraphs.html
# M. Meringer, Fast Generation of Regular Graphs and Construction of Cages,
# Journal of Graph Theory 30, 137-146 (1999).
# Python conversion: Sammy Beasley. Keys are zero-based source-list indices.
# Vertices are 0, ..., 6; source edge order is preserved.

EDGES = {
    0: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)],
    1: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 5), (2, 4), (2, 6), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)],
}
