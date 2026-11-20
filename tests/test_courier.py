import itertools
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from courier.data_loader import generate_graph, generate_parcels, load_graph, load_parcels
from courier.graph import dijkstra, path_to
from courier.knapsack import knapsack_dp
from courier.sorting import insertion_sort, merge_sort, quick_sort, prioritise
from courier.tsp import nearest_neighbour_route

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class TestSorting(unittest.TestCase):
    def test_all_sorts_match_python_sorted(self):
        ps = generate_parcels(300, ["Depot", "C1", "C2"], seed=7)
        key = lambda p: (p.deadline, -p.priority)
        ref = sorted(ps, key=key)
        for fn in (merge_sort, quick_sort, insertion_sort):
            self.assertEqual([key(p) for p in fn(ps, key)], [key(p) for p in ref])

    def test_merge_sort_stable(self):
        data = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]
        self.assertEqual(merge_sort(data, key=lambda x: x[0]),
                         [(0, "b"), (0, "d"), (1, "a"), (1, "c")])

    def test_empty_and_single(self):
        self.assertEqual(merge_sort([], key=lambda x: x), [])
        self.assertEqual(quick_sort([5], key=lambda x: x), [5])


class TestKnapsack(unittest.TestCase):
    def brute(self, ps, cap):
        best = 0
        for r in range(len(ps) + 1):
            for c in itertools.combinations(ps, r):
                if sum(p.weight for p in c) <= cap:
                    best = max(best, sum(p.priority for p in c))
        return best

    def test_against_brute_force(self):
        for seed in range(5):
            ps = generate_parcels(10, ["Depot", "C1"], seed=seed)
            for cap in (10, 25, 40):
                best, chosen, _ = knapsack_dp(ps, cap)
                self.assertEqual(best, self.brute(ps, cap))
                self.assertLessEqual(sum(p.weight for p in chosen), cap)
                self.assertEqual(sum(p.priority for p in chosen), best)

    def test_zero_capacity(self):
        ps = load_parcels(os.path.join(DATA, "parcels_small.json"))
        self.assertEqual(knapsack_dp(ps, 0)[0], 0)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.depot, self.g = load_graph(os.path.join(DATA, "graph_small.json"))

    def test_known_distances(self):
        dist, prev = dijkstra(self.g, "Depot")
        self.assertEqual(dist["Sector14"], 4)
        self.assertEqual(dist["MGRoad"], 7)       # via Sector14, not direct 9
        self.assertEqual(dist["CyberHub"], 9)
        self.assertEqual(path_to(prev, "MGRoad"), ["Depot", "Sector14", "MGRoad"])

    def test_route_returns_to_depot_and_visits_all(self):
        stops = ["Sector14", "CyberHub", "MGRoad", "Sohna"]
        order, total, path, _ = nearest_neighbour_route(self.g, self.depot, stops)
        self.assertEqual(order[0], "Depot")
        self.assertEqual(order[-1], "Depot")
        self.assertEqual(set(order[1:-1]), set(stops))
        self.assertEqual(path[0], "Depot")
        self.assertEqual(path[-1], "Depot")
        # path length must equal reported total
        self.assertEqual(sum(self.g[a][b] for a, b in zip(path, path[1:])), total)

    def test_generated_graph_connected(self):
        _, g = generate_graph(200)
        dist, _ = dijkstra(g, "Depot")
        self.assertTrue(all(d < float("inf") for d in dist.values()))


if __name__ == "__main__":
    unittest.main()
