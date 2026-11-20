"""Phase 4 - runtime measurements and chart."""
import csv
import os
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from courier.data_loader import generate_graph, generate_parcels
from courier.graph import dijkstra
from courier.knapsack import knapsack_dp
from courier.sorting import insertion_sort, merge_sort, quick_sort
from courier.tsp import nearest_neighbour_route

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")


def timeit(fn, repeat=5):
    best = float("inf")
    for _ in range(repeat):
        t = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t)
    return best * 1000  # ms


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []

    # --- sorting ---
    sort_sizes = [100, 500, 1000, 2000, 4000]
    sort_res = {"Merge sort": [], "Quick sort": [], "Insertion sort": []}
    for n in sort_sizes:
        ps = generate_parcels(n, ["Depot"] + [f"C{i}" for i in range(1, 30)])
        key = lambda p: (p.deadline, -p.priority)
        for name, fn in [("Merge sort", merge_sort), ("Quick sort", quick_sort),
                         ("Insertion sort", insertion_sort)]:
            t = timeit(lambda: fn(ps, key))
            sort_res[name].append(t)
            rows.append(["sorting", name, n, round(t, 3)])
        assert merge_sort(ps, key) == sorted(ps, key=key)

    # --- knapsack ---
    kn_sizes = [20, 50, 100, 200, 400]
    cap = 100
    kn_res = []
    for n in kn_sizes:
        ps = generate_parcels(n, ["Depot", "C1", "C2", "C3"])
        t = timeit(lambda: knapsack_dp(ps, cap), repeat=5)
        kn_res.append(t); rows.append(["knapsack_dp", f"W={cap}", n, round(t, 3)])

    # --- dijkstra ---
    dj_sizes = [50, 200, 800, 3200, 6400]
    dj_res = []
    for v in dj_sizes:
        _, g = generate_graph(v)
        t = timeit(lambda: dijkstra(g, "Depot"))
        dj_res.append(t); rows.append(["dijkstra", "single source", v, round(t, 3)])

    # --- NN TSP (k stops on a 500-node graph) ---
    _, g = generate_graph(500)
    nodes = [n for n in g if n != "Depot"]
    tsp_sizes = [5, 10, 20, 40, 80]
    tsp_res = []
    rnd = random.Random(1)
    for k in tsp_sizes:
        stops = rnd.sample(nodes, k)
        t = timeit(lambda: nearest_neighbour_route(g, "Depot", stops), repeat=5)
        tsp_res.append(t); rows.append(["nn_tsp", "500-node graph", k, round(t, 3)])

    with open(os.path.join(OUT, "runtime_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["component", "variant", "input_size", "time_ms"])
        w.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    for name, ys in sort_res.items():
        ax[0][0].plot(sort_sizes, ys, marker="o", label=name)
    ax[0][0].set(title="Sorting parcels", xlabel="parcels (n)", ylabel="time (ms)")
    ax[0][0].legend()
    ax[0][1].plot(kn_sizes, kn_res, marker="o", color="tab:green")
    ax[0][1].set(title=f"Knapsack DP (capacity {cap} kg)", xlabel="parcels (n)", ylabel="time (ms)")
    ax[1][0].plot(dj_sizes, dj_res, marker="o", color="tab:red")
    ax[1][0].set(title="Dijkstra (single source)", xlabel="graph nodes (V)", ylabel="time (ms)")
    ax[1][1].plot(tsp_sizes, tsp_res, marker="o", color="tab:purple")
    ax[1][1].set(title="Nearest-neighbour TSP (500-node graph)", xlabel="stops (k)", ylabel="time (ms)")
    for a in ax.flat:
        a.grid(alpha=.3)
    fig.suptitle("Mini-Courier Planner - runtime of major steps", fontsize=14)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "runtime_chart.png"), dpi=130)

    # console summary
    print(f"{'component':<14}{'size':>8}{'time (ms)':>12}")
    for r in rows:
        print(f"{r[0]+'/'+str(r[1]):<24}{r[2]:>6}{r[3]:>12}")


if __name__ == "__main__":
    main()
