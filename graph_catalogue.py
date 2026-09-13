"""Access the Python graph definitions using catalogue labels and stable IDs."""
from pathlib import Path
import csv
import json
import re
import networkx as nx


def _source_graph(collection, index):
    match = re.fullmatch(r'(\d+)v_(\d+)reg', collection)
    if match:
        from regular_graphs import get_graph
        return get_graph(*map(int, match.groups()), index)
    if collection.endswith('_connected'):
        from connected_graphs_4_to_7 import CONNECTED_GRAPHS
        return CONNECTED_GRAPHS[int(collection.split('v_')[0])][index].copy()
    if collection.endswith('_srg'):
        from strongly_regular_graphs import STRONGLY_REGULAR_GRAPHS
        return STRONGLY_REGULAR_GRAPHS[collection][index].copy()
    from graph_families import GRAPH_FAMILIES
    return GRAPH_FAMILIES[collection][index].copy()


def load_graphs(ids, data_dir=None):
    """Load stable graph IDs with vertices numbered in the stored node order."""
    data = Path(data_dir) if data_dir is not None else Path(__file__).parent / 'data'
    ids = list(dict.fromkeys(ids))
    wanted = set(ids)
    with (data / 'graphs.csv').open(encoding='utf-8', newline='') as handle:
        records = {row['graph_id']: row for row in csv.DictReader(handle)
                   if row['graph_id'] in wanted}
    if wanted != set(records):
        raise ValueError('Some requested graph IDs are missing from the catalogue.')
    graphs = {}
    for gid in ids:
        row = records[gid]
        graph = _source_graph(row['python_collection'], int(row['python_index']))
        graphs[gid] = nx.convert_node_labels_to_integers(graph, ordering='default')
    return graphs


def load_collection(name, data_dir=None):
    """Return (label, graph) entries with their original vertex labels and order."""
    data = Path(data_dir) if data_dir is not None else Path(__file__).parent / 'data'
    with (data / 'memberships.csv').open(encoding='utf-8', newline='') as handle:
        members = [row for row in csv.DictReader(handle) if row['collection'] == name]
    if not members:
        raise ValueError(f'Unknown or empty collection: {name}')
    graphs = load_graphs((row['graph_id'] for row in members), data)
    result = []
    for row in members:
        nodes = [tuple(node) if isinstance(node, list) else node
                 for node in json.loads(row['node_order_json'])]
        graph = nx.relabel_nodes(graphs[row['graph_id']], dict(enumerate(nodes)))
        result.append((row['label'], graph))
    return result
