# Phase 1 - Courier Problem Design and Planning

## 1. Problem
A courier van leaves a depot with a weight limit. Many parcels are waiting, each for some
delivery point. For one trip we must (a) decide **which parcels to load**, (b) decide
**in what order to visit** the delivery points, and (c) check that the plan is sensible
(distance and deadlines).

## 2. Data design
**Parcel** (`courier/models.py`)

| field    | meaning                              | used by            |
|----------|--------------------------------------|--------------------|
| id       | unique id, e.g. `P01`                | all                |
| dest     | delivery point = graph node name     | routing            |
| weight   | kg (integer)                         | knapsack weight    |
| priority | business value 1-10                  | knapsack value     |
| deadline | minutes after dispatch               | sorting, deadline check |

**Road graph** - undirected, weighted (km), stored as adjacency dict
`{node: {neighbour: km}}`. File format: `{"depot": "Depot", "edges": [[u, v, km], ...]}`.
Adjacency list is used because road networks are sparse (E << V^2), giving
O((V+E) log V) Dijkstra.

**Van** - one integer capacity in kg. Travel time assumed 2 min/km.

## 3. Algorithm selection and why

| Sub-problem | Algorithm | Why this one | Complexity |
|-------------|-----------|--------------|------------|
| Prioritise parcels | Merge sort (key = deadline, then -priority) | guaranteed O(n log n), stable | O(n log n) time, O(n) space |
| Choose parcels for one trip | 0/1 knapsack DP | parcels cannot be split; greedy by ratio is not optimal; DP gives the optimum | O(nW) time and space |
| Shortest road distance between points | Dijkstra with min-heap | all edge weights are non-negative | O((V+E) log V) per source |
| Order of visits | Nearest-neighbour TSP approximation | TSP is NP-hard; exact search is infeasible beyond ~15 stops | O(k^2) + k+1 Dijkstra runs |

## 4. How the pieces work together

```
 parcels.json ──► [Merge sort] ──► ordered parcels
                                        │
 van capacity ─────────────────────────►│
                                  [Knapsack DP]
                                        │ chosen parcels
                                        ▼
                        unique delivery points (stops)
                                        │
 graph.json ──► [Dijkstra from depot + every stop] ──► shortest-distance tables
                                        │
                              [Nearest-neighbour TSP]
                                        │
              stop order + expanded road path + total km + deadline check
```

1. **Sort** so that urgent parcels come first (display order, tie-breaking and later
   reuse for scheduling further trips).
2. **Knapsack** picks the subset with maximum total priority within the weight limit.
3. **Dijkstra** gives true road distances between the depot and every chosen stop
   (the road graph is not complete, so TSP cannot use direct edges).
4. **Nearest neighbour** builds the tour depot -> stops -> depot using those distances.
5. **Deadline check** reports which parcels arrive on time.

## 5. Assumptions and limits
- One van, one trip at a time; remaining parcels wait for the next trip.
- Only weight is limited (no volume).
- Graph is connected and undirected; edge weights are positive.
- Several parcels to the same point are delivered in one visit.
