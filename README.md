# Mini-Courier Planner

Capstone Assignment - Design & Analysis of Algorithms (ETCCDA302), K.R. Mangalam University.

Given parcels and delivery points, the program (1) sorts parcels by deadline/priority,
(2) picks the best set for one van trip with 0/1 knapsack DP, (3) finds shortest road distances
with Dijkstra, (4) builds a delivery route with nearest-neighbour TSP, and (5) benchmarks every step.

## Project structure
```
mini_courier_planner/
├── main.py                 # end-to-end demo (Phases 2, 3, 5)
├── benchmark.py            # runtime tests + chart (Phase 4)
├── courier/
│   ├── models.py           # Parcel data design
│   ├── data_loader.py      # JSON loading + random dataset generators
│   ├── sorting.py          # merge sort (main), quick sort, insertion sort
│   ├── knapsack.py         # 0/1 knapsack DP with back-tracking
│   ├── graph.py            # Dijkstra
│   └── tsp.py              # nearest-neighbour TSP approximation
├── data/                   # sample parcels and road graph (JSON)
├── tests/test_courier.py   # unit tests
├── docs/design.md          # Phase 1 design
├── docs/report.md          # Phases 2-5 report
└── outputs/                # run traces, runtime chart/CSV, screenshots/
```

## How to run
Requires Python 3.8+. Only `benchmark.py` needs matplotlib.
```bash
pip install -r requirements.txt          # for the chart only

python main.py                           # sample data, 25 kg van
python main.py --capacity 30             # change van capacity
python main.py --large 300 --nodes 60 --capacity 100   # generated larger dataset

python benchmark.py                      # writes outputs/runtime_chart.png + runtime_results.csv
python -m unittest discover -s tests -v  # run tests
```

## Input formats
`data/parcels_small.json`: list of `{"id","dest","weight","priority","deadline"}`.
`data/graph_small.json`: `{"depot": "Depot", "edges": [["A","B",km], ...]}` (undirected).
To use your own data, edit these files (destination names must exist in the graph).

## Marks mapping
| Phase | Where |
|-------|-------|
| 1 Design | `docs/design.md` |
| 2 Sorting + DP | `courier/sorting.py`, `courier/knapsack.py`, output in `outputs/run_output_small.txt` |
| 3 Graph + route | `courier/graph.py`, `courier/tsp.py` |
| 4 Performance | `benchmark.py`, `outputs/runtime_chart.png`, `outputs/runtime_results.csv` |
| 5 Report + demo | `docs/report.md`, `outputs/screenshots/` |

Before submitting, add your name and roll number to this README.
