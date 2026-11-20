"""Load / generate parcels and road graphs."""
import json
import random
from .models import Parcel


def load_parcels(path):
    with open(path) as f:
        raw = json.load(f)
    return [Parcel(**p) for p in raw]


def load_graph(path):
    """Graph file format: {"depot": "Depot", "edges": [[u, v, km], ...]} (undirected)."""
    with open(path) as f:
        raw = json.load(f)
    graph = {}
    for u, v, w in raw["edges"]:
        graph.setdefault(u, {})[v] = w
        graph.setdefault(v, {})[u] = w
    return raw["depot"], graph


def generate_graph(n_nodes, extra_edges_factor=2, seed=42):
    """Random connected undirected weighted graph. 'Depot' is the start node."""
    rnd = random.Random(seed)
    names = ["Depot"] + [f"C{i}" for i in range(1, n_nodes)]
    graph = {n: {} for n in names}
    # random spanning tree guarantees connectivity
    for i in range(1, n_nodes):
        j = rnd.randrange(0, i)
        w = rnd.randint(1, 20)
        graph[names[i]][names[j]] = w
        graph[names[j]][names[i]] = w
    for _ in range(n_nodes * extra_edges_factor):
        a, b = rnd.sample(names, 2)
        w = rnd.randint(1, 20)
        if b not in graph[a] or w < graph[a][b]:
            graph[a][b] = w
            graph[b][a] = w
    return "Depot", graph


def generate_parcels(n, graph_nodes, seed=42):
    rnd = random.Random(seed)
    customers = [x for x in graph_nodes if x != "Depot"]
    return [
        Parcel(
            id=f"P{i:04d}",
            dest=rnd.choice(customers),
            weight=rnd.randint(1, 15),
            priority=rnd.randint(1, 10),
            deadline=rnd.randint(30, 600),
        )
        for i in range(1, n + 1)
    ]
