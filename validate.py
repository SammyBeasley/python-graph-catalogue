"""Validate the catalogue structure, graph encodings and stored pair spectra."""
from pathlib import Path
import csv
import json
import hashlib
import networkx as nx
import numpy as np

root = Path(__file__).parent
data = root / 'data'
checksums = json.loads((data / 'checksums.json').read_text())
for name, expected in checksums.items():
    assert hashlib.sha256((data / name).read_bytes()).hexdigest() == expected, name
with (data / 'graphs.csv').open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
encodings = {}
for row in rows:
    gid, g6 = row['graph_id'], row['graph6']
    assert gid not in encodings
    assert gid == 'g_' + hashlib.sha256(g6.encode()).hexdigest()[:20]
    graph = nx.from_graph6_bytes(g6.encode())
    assert len(graph) == int(row['n']) and graph.number_of_edges() == int(row['m']), gid
    assert nx.to_graph6_bytes(graph, header=False).decode().strip() == g6
    if row['regular_degree']:
        assert set(dict(graph.degree()).values()) == {int(row['regular_degree'])}, gid
    assert nx.is_connected(graph) == (row['connected'] == 'True'), gid
    encodings[gid] = g6
assert list(encodings.values()) == (data / 'graphs.g6').read_text(encoding='ascii').splitlines()
with (data / 'memberships.csv').open(encoding='utf-8', newline='') as handle:
    members = list(csv.DictReader(handle))
for row in members:
    assert row['graph_id'] in encodings
    assert len(json.loads(row['node_order_json'])) == len(nx.from_graph6_bytes(encodings[row['graph_id']].encode()))
for n, count in [(4, 6), (5, 21), (6, 112), (7, 853)]:
    assert sum(row['collection'] == f'{n}v_connected' for row in members) == count
with (data / 'pairs.csv').open(encoding='utf-8', newline='') as handle:
    pairs = list(csv.DictReader(handle))
eigenvalues = {}
regular_pairs = 0
for row in pairs:
    a, b = row['graph_id_1'], row['graph_id_2']
    assert a in encodings and b in encodings
    if row['collection'] in ['special_pairs', 'ladder_pairs']:
        continue
    regular_pairs += 1
    for gid in (a, b):
        if gid not in eigenvalues:
            graph = nx.from_graph6_bytes(encodings[gid].encode())
            eigenvalues[gid] = np.linalg.eigvalsh(nx.to_numpy_array(graph))
    np.testing.assert_allclose(eigenvalues[a], eigenvalues[b], rtol=0, atol=1e-10)
assert regular_pairs == 10486
report = {'graphs': len(rows), 'memberships': len(members), 'pairs': len(pairs),
          'cospectral_regular_pairs': regular_pairs, 'checksums': 'passed',
          'graph6_roundtrip': 'passed', 'pair_spectra': 'passed',
          'isomorphism_canonicalisation': 'not performed'}
print(json.dumps(report, indent=2))
