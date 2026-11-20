"""Phase 3 - shortest paths with Dijkstra's algorithm.

Graph representation: adjacency dict {node: {neighbour: distance_km}}.
Time O((V + E) log V) with a binary heap (heapq).
"""
import heapq


def dijkstra(graph, source):
    """Return (dist, prev) for all nodes reachable from source."""
    dist = {n: float("inf") for n in graph}
    prev = {n: None for n in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                      # stale heap entry
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def path_to(prev, target):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]
