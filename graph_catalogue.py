"""Load the graph catalogue without executable pickle data."""
from pathlib import Path
import csv
import networkx as nx


def load_collection(name, data_dir=None):
    data = Path(data_dir) if data_dir is not None else Path(__file__).parent / 'data'
    with (data / 'memberships.csv').open(encoding='utf-8', newline='') as handle:
        members = [row for row in csv.DictReader(handle) if row['collection'] == name]
    if not members:
        raise ValueError(f'Unknown or empty collection: {name}')
    wanted = {row['graph_id'] for row in members}
    with (data / 'graphs.csv').open(encoding='utf-8', newline='') as handle:
        encodings = {row['graph_id']: row['graph6'] for row in csv.DictReader(handle) if row['graph_id'] in wanted}
    return [(row['label'], nx.from_graph6_bytes(encodings[row['graph_id']].encode())) for row in members]
