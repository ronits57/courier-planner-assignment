"""Mini-Courier Planner - end-to-end demo.

Usage:
    python main.py                          # small sample dataset, capacity 25 kg
    python main.py --capacity 30
    python main.py --large 300 --nodes 60   # generated larger dataset
"""
import argparse
import os

from courier.data_loader import (generate_graph, generate_parcels,
                                 load_graph, load_parcels)
from courier.knapsack import format_dp_table, knapsack_dp
from courier.sorting import prioritise
from courier.tsp import nearest_neighbour_route

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_PER_KM = 2          # assumed travel time: 2 minutes per km


def run(parcels, depot, graph, capacity, show_table=True):
    print("=" * 64)
    print("MINI-COURIER PLANNER")
    print("=" * 64)
    print(f"Parcels: {len(parcels)}   Graph nodes: {len(graph)}   Van capacity: {capacity} kg\n")

    # ---- Phase 2a: sorting ------------------------------------------------
    ordered = prioritise(parcels)
    print("STEP 1 - Parcels sorted by deadline (earliest first), then priority")
    print(f"{'ID':<7}{'Dest':<12}{'Wt(kg)':>7}{'Prio':>6}{'Deadline(min)':>15}")
    for p in ordered[:15]:
        print(f"{p.id:<7}{p.dest:<12}{p.weight:>7}{p.priority:>6}{p.deadline:>15}")
    if len(ordered) > 15:
        print(f"... ({len(ordered) - 15} more)")

    # ---- Phase 2b: knapsack ----------------------------------------------
    best, chosen, dp = knapsack_dp(ordered, capacity)
    print(f"\nSTEP 2 - 0/1 Knapsack DP (capacity {capacity} kg)")
    if show_table and len(ordered) <= 10 and capacity <= 30:
        print(format_dp_table(ordered, dp))
    print(f"Best total priority : {best}")
    print(f"Selected parcels    : {[p.id for p in chosen]}")
    print(f"Total weight loaded : {sum(p.weight for p in chosen)} / {capacity} kg")
    left = [p.id for p in ordered if p not in chosen]
    print(f"Left for next trip  : {left if len(left) <= 15 else str(len(left)) + ' parcels'}")

    # ---- Phase 3: routing -------------------------------------------------
    stops = [p.dest for p in chosen]
    order, total, full_path, sp = nearest_neighbour_route(graph, depot, stops)
    print("\nSTEP 3 - Dijkstra shortest distances from depot")
    dist_depot = sp[depot][0]
    for s in order[1:-1]:
        print(f"  {depot} -> {s:<11}: {dist_depot[s]} km")
    print("\nSTEP 4 - Nearest-neighbour TSP delivery route")
    print("  Stop order  : " + " -> ".join(order))
    print("  Road path   : " + " -> ".join(full_path))
    print(f"  Route length: {total} km  (~{total * MIN_PER_KM} min driving)")

    # ---- Deadline check ---------------------------------------------------
    print("\nSTEP 5 - Deadline check (arrival = distance travelled x "
          f"{MIN_PER_KM} min/km)")
    arrival, t = {}, 0
    for a, b in zip(order, order[1:-1]):
        t += sp[a][0][b]
        arrival.setdefault(b, t * MIN_PER_KM)
    late = 0
    for p in chosen:
        ok = arrival[p.dest] <= p.deadline
        late += (not ok)
        print(f"  {p.id} -> {p.dest:<11} arrive {arrival[p.dest]:>4} min, "
              f"deadline {p.deadline:>4}  {'OK' if ok else 'LATE'}")
    print(f"\nSummary: {len(chosen) - late}/{len(chosen)} parcels on time.")
    print("(NN-TSP is optimised for distance, not deadlines - see report for improvements.)")
    return chosen, order, total


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--capacity", type=int, default=25)
    ap.add_argument("--large", type=int, default=0, help="generate N random parcels")
    ap.add_argument("--nodes", type=int, default=40, help="nodes for generated graph")
    args = ap.parse_args()

    if args.large:
        depot, graph = generate_graph(args.nodes)
        parcels = generate_parcels(args.large, graph.keys())
    else:
        depot, graph = load_graph(os.path.join(HERE, "data", "graph_small.json"))
        parcels = load_parcels(os.path.join(HERE, "data", "parcels_small.json"))
    run(parcels, depot, graph, args.capacity)
