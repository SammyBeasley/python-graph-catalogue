# Graphs used in the QAOA and IQP project

A catalogue of the graph instances in the research source files, with the exact stored vertex order, original labels and pair memberships. This repository contains graph data and a small loader, with no simulation results or figures.

## Contents

- `data/graphs.csv`: 156,228 distinct stored graph encodings, their stable IDs, vertex/edge counts and degree information.
- `data/graphs.g6`: the same graphs in graph6 format, in the same row order.
- `data/memberships.csv`: 173,041 collection memberships with source labels and original vertex orders.
- `data/collections.csv`: 53 collections, their sizes and study status.
- `data/pairs.csv`: 10,486 stored cospectral regular pairs, plus 10 ladder and special pairs.
- `data/checksums.json`: checksums for the exported data files.

The collections include connected graphs on 4..7 vertices, the supplied regular and strongly regular graph lists, circular and Mobius ladders, the two Miyazaki-inspired graphs, and the deterministic graph families configured in the IQP family notebook.

## Load a collection

```python
from graph_catalogue import load_collection

labelled_graphs = load_collection("10v_4reg")
for label, graph in labelled_graphs:
    print(label, graph.number_of_nodes(), graph.number_of_edges())
```

Install the only loader dependency with `python -m pip install networkx`.

## Identity and indices

A graph ID is `g_` followed by the first 20 hexadecimal characters of SHA-256 of its headerless graph6 encoding. Exact repeated stored encodings occur only once in `graphs.csv`. IDs preserve vertex order; they are **not isomorphism-canonical labels**. Isomorphic relabellings can therefore have different IDs. Use collection membership when describing a particular experiment.

`position` is one-based. The regular graph lists were displayed with one-based labels in the IQP notebook; the saved QAOA cospectral indices are zero-based. Both original conventions are retained. Use `graph_id`, `source_index_1` and `source_index_2` to join pairs, rather than assuming a shared textual label has the same indexing convention in every source. `node_order_json` maps graph6 vertices back to the source vertex labels.

## What was studied

`configured_in_notebook` means a collection is explicitly included by the notebook experiment configuration. It does not establish that every long-running experiment completed. `available_in_sources` identifies the larger strongly regular lists present in the source module but outside the current notebook's main simulation range. Do not describe these as completed experiments solely because they are stored here.

The supplied connected-graph files contain 6, 21, 112 and 853 graphs for orders 4, 5, 6 and 7. The saved exact QAOA scaling results cover cospectral pairs of orders 10, 11, 12, 13, 14, 16 and 18. Completion status and numerical results belong to the separate analysis repository.

## Sources

The graph-loading notebooks credit [Markus Meringer's regular graph database](https://www.mathe2.uni-bayreuth.de/markus/reggraphs.html). Its regular-graph counts match the named regular collections here. The database requests the citation:

M. Meringer, *Fast Generation of Regular Graphs and Construction of Cages*, Journal of Graph Theory 30, 137–146 (1999).

Connected graphs come from the supplied saved connected-graph lists. Named families and special pairs retain the constructions in the supplied notebooks. Strongly regular lists come from the supplied `graphs.py`; their upstream source was not recorded there. This catalogue records those source files without inventing missing attribution.

Run `python validate.py` to verify encodings, checksums, membership references and stored pair spectra. The validation does not attempt exhaustive pairwise graph-isomorphism testing across the whole catalogue.
