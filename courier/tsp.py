"""Phase 3 - nearest-neighbour TSP approximation over road-network distances.

Real roads are not a complete graph, so Dijkstra is run from the depot and from
every stop to build shortest-distance tables. Nearest neighbour then builds the
tour greedily: O(k^2) after k+1 Dijkstra runs. It has no constant-factor
guarantee (only an O(log k) ratio for metric TSP) but is simple and fast.
"""
from .graph import dijkstra, path_to


def nearest_neighbour_route(graph, depot, stops):
    stops = list(dict.fromkeys(stops))            # unique, keep order
    nodes = [depot] + [s for s in stops if s != depot]
    sp = {n: dijkstra(graph, n) for n in nodes}   # node -> (dist, prev)

    order, total, current = [depot], 0, depot
    remaining = set(nodes[1:])
    while remaining:
        nxt = min(remaining, key=lambda s: (sp[current][0][s], s))
        total += sp[current][0][nxt]
        order.append(nxt)
        remaining.remove(nxt)
        current = nxt
    total += sp[current][0][depot]                # return to depot
    order.append(depot)

    # expand each leg into the actual road path
    full_path = [depot]
    for a, b in zip(order, order[1:]):
        leg = path_to(sp[a][1], b)
        full_path.extend(leg[1:])
    return order, total, full_path, sp
