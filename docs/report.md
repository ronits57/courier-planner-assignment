# Mini-Courier Planner - Report (Phases 2-5)

K.R. Mangalam University - Design & Analysis of Algorithms (ETCCDA302) - Capstone Assignment

## Phase 2 - Package prioritisation and box filling

**Sorting.** Parcels are sorted with merge sort by `(deadline, -priority)`. Merge sort is stable and
has O(n log n) worst case, so behaviour does not degrade on already-sorted or adversarial input.
Insertion sort and quick sort were also implemented, only to compare runtimes.

**Knapsack.** `courier/knapsack.py` fills the table `dp[i][w]` and back-tracks to find the chosen
parcels. Sample run (8 parcels, 25 kg van), full table in `outputs/run_output_small.txt`:

| item | value |
|------|-------|
| Best total priority | **33** |
| Selected parcels | P01, P07, P05, P02, P08 |
| Weight loaded | 23 / 25 kg |
| Left for next trip | P03, P06, P04 |

Note that P03 has the earliest deadline but is *not* loaded: it weighs 8 kg for priority 9, and
the DP finds that P08 + P05 + P02 + P01 + P07 give more total priority in the same space. This
shows that the DP optimises priority, not the deadline order (see improvements below).
Correctness was verified against brute force on random instances (`tests/`).

## Phase 3 - Route maker and graph processing

- Graph: undirected adjacency dictionary, 8 nodes / 12 roads in the sample.
- Dijkstra from the depot (sample): Sector14 = 4 km, CyberHub = 9 km, DLFPhase = 11 km,
  GolfCourse = 11 km. Example of why shortest paths matter: Depot->MGRoad direct is 9 km but via
  Sector14 it is only 7 km (checked in the unit tests).
- Nearest-neighbour tour: `Depot -> Sector14 -> CyberHub -> DLFPhase -> GolfCourse -> Depot`
- Expanded road path: `Depot -> Sector14 -> CyberHub -> DLFPhase -> MGRoad -> GolfCourse -> MGRoad -> Sector14 -> Depot`
- **Route length: 32 km (about 64 minutes).** All 5 loaded parcels arrive before their deadlines.

NN is a heuristic: it is not guaranteed optimal. For 4 stops the tour could be checked by hand;
for larger inputs the exact answer needs exponential time, which is the reason for approximating.

## Phase 4 - Performance testing and optimisation

Datasets: the 8-parcel sample, plus generated data (seeded, reproducible) up to 4000 parcels and
6400-node graphs. Chart: `outputs/runtime_chart.png`; raw numbers: `outputs/runtime_results.csv`.
Times are the best of 5 runs on the machine used to generate this package, so absolute values will differ
on yours; the growth trend is what matters.

| Step | Input size | Time | Observation |
|------|-----------|------|-------------|
| Merge sort | 4000 parcels | ~8.5 ms | grows roughly n log n |
| Quick sort | 4000 parcels | ~6.3 ms | slightly faster than merge sort in practice |
| Insertion sort | 4000 parcels | ~365 ms | quadratic: ~43x slower than merge sort |
| Knapsack DP | 400 parcels, W=100 | ~2.2 ms | linear in n for fixed W |
| Dijkstra | 6400 nodes | ~8.4 ms | near-linear growth |
| NN-TSP | 80 stops, 500 nodes | ~38 ms | linear in k here: cost dominated by k+1 Dijkstra runs |

Correctness evidence: 8 unit tests pass (`outputs/test_output.txt`) - sorts vs Python `sorted`,
stability, knapsack vs brute force, Dijkstra known distances, tour validity.

**Why merge sort rather than the faster quick sort?** Quick sort was a little faster on random
data, but merge sort is stable (equal parcels keep arrival order) and has no O(n^2) worst case.

**Large-dataset result.** With 300 parcels, 60 nodes and a 100 kg van, the planner loaded 49 parcels
(priority 370, exactly 100 kg) and the route was 306 km, but only 36/49 parcels met their deadline.
So nearest-neighbour minimises distance, not lateness.

**Suggested improvements**
1. Deadline-aware routing: use a TSP with time windows heuristic (e.g. insert stops by earliest deadline, then 2-opt that never creates a late arrival), or make the knapsack value include a lateness penalty.
2. Improve the tour with 2-opt / Or-opt after nearest neighbour (typically 5-15% shorter).
3. Knapsack space: keep a 1-D array if only the best value is needed (O(W) space); the 2-D table is kept here to back-track.
4. Run Dijkstra once per stop only (already done) and cache results across trips; use A* if coordinates are available.
5. Multiple trips: repeat sort -> knapsack -> route on the leftover parcels until none remain.
6. Add a volume constraint (2-D knapsack) for realism.

## Phase 5 - Result explanation and demonstration

**Result explanation.** For the sample data the van is loaded with 5 parcels worth 33 priority
points (23 kg of 25). They go to 4 distinct delivery points (two parcels share Sector14), visited in
the order Sector14, CyberHub, DLFPhase, GolfCourse, a 32 km round trip. Every parcel arrives before its deadline.

**Screenshots / output traces** (`outputs/screenshots/`): `01_small_run.png`, `02_large_run.png`,
`03_unit_tests.png`. Full text traces are in `outputs/run_output_*.txt`.
These images are rendered from the real program output files.

**Originality.** All code was written for this assignment; only Python standard library is used
for the algorithms (matplotlib only for the chart). Students should be able to explain every line
in the viva (trace the DP table, trace Dijkstra's heap, explain the complexity above).

## Complexity summary

| Component | Time | Space |
|-----------|------|-------|
| Merge sort | O(n log n) | O(n) |
| Knapsack DP | O(nW) | O(nW) |
| Dijkstra (binary heap) | O((V+E) log V) | O(V) |
| NN-TSP over k stops | O(k(V+E) log V + k^2) | O(kV) |
