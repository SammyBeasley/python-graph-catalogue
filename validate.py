"""Validate the Python graph definitions, metadata and saved cospectral pairs."""
from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json

import networkx as nx
import numpy as np

from graph_catalogue import _source_graph
from connected_graphs_4_to_7 import CONNECTED_GRAPHS
from cospectral_pairs import PAIR_INDICES, get_pairs
from regular_graphs import GRAPH_COUNTS, get_graph
from strongly_regular_graphs import STRONGLY_REGULAR_GRAPHS

root = Path(__file__).resolve().parent

def read_csv(name):
    with (root / 'data' / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def graph_id(graph):
    # Retain the existing stable identifiers across the storage-format change.
    normalized = nx.convert_node_labels_to_integers(graph, ordering='default')
    return 'g_' + hashlib.sha256(nx.to_graph6_bytes(normalized, header=False).strip()).hexdigest()[:20]


def main():
    manifest = json.loads((root / 'data/checksums.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
    records = {row['graph_id']: row for row in read_csv('graphs.csv')}
    members = read_csv('memberships.csv')
    by_collection = defaultdict(list)
    for row in members:
        assert row['graph_id'] in records
        by_collection[row['collection']].append(row)
    for number, (gid, row) in enumerate(records.items(), 1):
        graph = _source_graph(row['python_collection'], int(row['python_index']))
        assert graph_id(graph) == gid, gid
        assert len(graph) == int(row['n'])
        assert graph.number_of_edges() == int(row['m'])
        assert nx.is_connected(graph) == (row['connected'] == 'True')
        if row['regular_degree']:
            assert set(dict(graph.degree()).values()) == {int(row['regular_degree'])}
        if number % 25000 == 0:
            print(f'Checked {number:,} graph definitions.', flush=True)
    for n_degree, count in GRAPH_COUNTS.items():
        n, degree = n_degree
        collection = f'{n}v_{degree}reg'
        assert len(by_collection[collection]) == count
        # Every source position must refer to the corresponding Python graph.
        for index, row in enumerate(by_collection[collection]):
            assert int(row['position']) == index + 1
            # The ID check above covers each distinct graph; metadata retains
            # the source location even where another collection shares an ID.
            stored = records[row['graph_id']]
            assert (stored['python_collection'], int(stored['python_index'])) == (collection, index)
    for n, count in [(4, 6), (5, 21), (6, 112), (7, 853)]:
        graphs = CONNECTED_GRAPHS[n]
        assert len(graphs) == count
        atlas = [g for g in nx.graph_atlas_g() if len(g) == n and nx.is_connected(g)]
        assert len(atlas) == count
        buckets = defaultdict(list)
        for graph in atlas:
            buckets[tuple(sorted(dict(graph.degree()).values()))].append(graph)
        for index, graph in enumerate(graphs):
            assert graph_id(graph) == by_collection[f'{n}v_connected'][index]['graph_id']
            bucket = buckets[tuple(sorted(dict(graph.degree()).values()))]
            match = next((i for i, candidate in enumerate(bucket) if nx.is_isomorphic(graph, candidate)), None)
            assert match is not None, (n, index)
            bucket.pop(match)
        assert not any(buckets.values())
    parameters = {'16v_srg': (16, 6, 2, 2), '25v_srg': (25, 12, 5, 6),
                  '26v_srg': (26, 10, 3, 4), '28v_srg': (28, 12, 6, 4),
                  '29v_srg': (29, 14, 6, 7)}
    for collection, graphs in STRONGLY_REGULAR_GRAPHS.items():
        n, degree, adjacent, nonadjacent = parameters[collection]
        for graph in graphs:
            a = nx.to_numpy_array(graph, dtype=int)
            assert a.shape == (n, n) and np.all(a.sum(axis=1) == degree)
            expected = (degree - nonadjacent) * np.eye(n, dtype=int) + (adjacent - nonadjacent) * a + nonadjacent * np.ones((n, n), dtype=int)
            np.testing.assert_array_equal(a @ a, expected)
    pair_rows = defaultdict(list)
    for row in read_csv('pairs.csv'):
        pair_rows[row['collection']].append(row)
    checked_pairs = 0
    for collection, indices in PAIR_INDICES.items():
        rows = pair_rows[collection]
        assert len(rows) == len(indices)
        eigvals = {}
        for (a, b), row in zip(indices, rows):
            assert (a, b) == (int(row['source_index_1']), int(row['source_index_2']))
            for index, suffix in [(a, '1'), (b, '2')]:
                if index not in eigvals:
                    graph = _source_graph(collection, index)
                    assert graph_id(graph) == row['graph_id_' + suffix]
                    eigvals[index] = np.linalg.eigvalsh(nx.to_numpy_array(graph))
            np.testing.assert_allclose(eigvals[a], eigvals[b], atol=1e-10, rtol=0)
            checked_pairs += 1
    # Independent copies protect later experiments from accidental shared edits.
    a, b = get_pairs('10v_4reg')[0]
    a.clear()
    assert len(get_pairs('10v_4reg')[0][0]) == 10
    first = get_graph(10, 4, 0)
    first.clear()
    assert len(get_graph(10, 4, 0)) == 10
    assert checked_pairs == 10487
    print(json.dumps({'graphs': len(records), 'memberships': len(members),
                      'cospectral_pairs': checked_pairs,
                      'connected_graphs_match_atlas': True,
                      'strongly_regular_parameters': 'passed',
                      'checksums_and_stable_ids': 'passed'}, indent=2))


if __name__ == '__main__':
    main()
