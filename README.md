# 🚚 Mini-Courier Planner
### Design & Analysis of Algorithms (ETCCDA302)
**K.R. Mangalam University**

An algorithm-based courier delivery planning system built using Python. It combines sorting, Dynamic Programming, graph algorithms, and route optimization to make parcel selection and delivery planning more efficient.

## 👨‍🎓 Project Information

| Detail | Information |
|---|---|
| Project Title | Mini-Courier Planner |
| Student Name | Ronit |
| Roll Number | 2501350026 |
| Course | Design & Analysis of Algorithms |
| Course Code | ETCCDA302 |
| University | K.R. Mangalam University |
| Programming Language | Python 3.8+ |
| Repository | [courier-planner-assignment](https://github.com/ronits57/courier-planner-assignment) |

---

## 📌 1. Project Overview

Mini-Courier Planner is a Python-based application designed to simulate an efficient courier delivery management system.

The system takes parcel information, including weight, priority, deadline, and destination, and processes it using different algorithmic techniques.

It performs five major operations:

1. **Parcel Sorting:** Sorts parcels according to delivery deadlines and priorities.
2. **Parcel Selection:** Uses the 0/1 Knapsack Dynamic Programming algorithm to select the best combination of parcels within the van's weight capacity.
3. **Shortest Path Calculation:** Uses Dijkstra's algorithm to calculate minimum road distances.
4. **Delivery Route Planning:** Applies the Nearest-Neighbour TSP approximation to construct a delivery route.
5. **Performance Benchmarking:** Measures and compares the execution time of the implemented algorithms.

## 🎯 2. Project Objectives

- Apply theoretical concepts of Design and Analysis of Algorithms to a real-world problem.
- Implement and compare different sorting techniques.
- Optimize parcel selection using Dynamic Programming.
- Calculate shortest distances using graph algorithms.
- Generate efficient delivery routes using TSP approximation.
- Analyze time and space complexity.
- Evaluate algorithm performance using different dataset sizes.

## ⚙️ 3. Features

| Feature | Description |
|---|---|
| Parcel Management | Load parcel information from JSON files. |
| Priority Sorting | Arrange parcels by deadline and priority. |
| Capacity Optimization | Select parcels using 0/1 Knapsack DP. |
| Shortest Path | Calculate minimum distances using Dijkstra. |
| Route Planning | Generate routes using Nearest-Neighbour TSP. |
| Dataset Generation | Create random datasets for testing. |
| Performance Analysis | Benchmark algorithm execution times. |
| Graph Visualization | Generate runtime charts using Matplotlib. |
| Unit Testing | Test algorithm correctness using Python Unittest. |

## 🧠 4. Algorithms Implemented

### 1. Merge Sort
Used to sort parcels according to their deadlines and priorities.

- Time Complexity: O(n log n)
- Space Complexity: O(n)

### 2. 0/1 Knapsack – Dynamic Programming
Selects the most valuable combination of parcels without exceeding the van's weight capacity.

- Time Complexity: O(n × W)
- Space Complexity: O(n × W)

### 3. Dijkstra's Algorithm
Finds the shortest distances between the depot and delivery locations.

- Time Complexity: O((V + E) log V) using an adjacency list and priority queue.

### 4. Nearest-Neighbour TSP
Creates a delivery route by selecting the nearest unvisited destination at each step.

- Time Complexity: O(V²) with a distance-matrix implementation.
- Produces an approximate solution, not necessarily the globally shortest route.

### 5. Performance Benchmarking
Measures execution time for different input sizes and generates graphical comparisons.

---

## 📂 5. Project Structure

```text
mini_courier_planner/
│
├── main.py
├── benchmark.py
│
├── courier/
│   ├── models.py
│   ├── data_loader.py
│   ├── sorting.py
│   ├── knapsack.py
│   ├── graph.py
│   └── tsp.py
│
├── data/
│   ├── parcels_small.json
│   └── graph_small.json
│
├── tests/
│   └── test_courier.py
│
├── docs/
│   ├── design.md
│   └── report.md
│
├── outputs/
│   ├── run_output_small.txt
│   ├── runtime_chart.png
│   ├── runtime_results.csv
│   └── screenshots/
│
├── requirements.txt
└── README.md
```

## 🛠️ 6. Technologies Used

- Python 3.8+
- Data Structures and Algorithms
- Dynamic Programming
- Graph Theory
- JSON
- Matplotlib
- Python Unittest
- VS Code

## 🚀 7. Installation and Execution

**Prerequisites:** Python 3.8 or above.

### Step 1: Clone the Repository

```bash
git clone https://github.com/ronits57/courier-planner-assignment.git
```

### Step 2: Open the Project Directory

```bash
cd courier-planner-assignment
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Main Program

```bash
python main.py
```

### Step 5: Change Van Capacity

```bash
python main.py --capacity 30
```

### Step 6: Generate a Larger Dataset

```bash
python main.py --large 300 --nodes 60 --capacity 100
```

### Step 7: Run Performance Benchmarking

```bash
python benchmark.py
```

### Step 8: Execute Unit Tests

```bash
python -m unittest discover -s tests -v
```

## 📥 8. Input Data Format

The project uses JSON files for parcel information and road-network data.

**Parcel Data – `parcels_small.json`**

```json
[
  {
    "id": "P101",
    "dest": "A",
    "weight": 5,
    "priority": 1,
    "deadline": "10:00"
  }
]
```

**Road Network – `graph_small.json`**

```json
{
  "depot": "Depot",
  "edges": [
    ["Depot", "A", 5],
    ["Depot", "B", 8],
    ["A", "B", 3]
  ]
}
```

The road network is undirected. Every parcel destination must exist as a node in the graph.

## 📊 9. Performance Analysis

The benchmarking module evaluates algorithm performance using datasets of different sizes.

The analysis includes:

- Sorting algorithm execution times.
- Knapsack DP execution time.
- Dijkstra's algorithm execution time.
- TSP route-generation execution time.
- Runtime comparisons as input size increases.

**Generated Results**

| File | Purpose |
|---|---|
| `runtime_chart.png` | Graphical runtime comparison. |
| `runtime_results.csv` | Benchmark results in CSV format. |
| `run_output_small.txt` | Sample program execution output. |
| `screenshots/` | Project execution screenshots. |

## 🎓 10. Academic Marks Mapping

| Phase | Description | Implementation |
|---|---|---|
| Phase 1 | System Design | `docs/design.md` |
| Phase 2 | Sorting and Dynamic Programming | `sorting.py`, `knapsack.py` |
| Phase 3 | Graph Algorithms and Route Planning | `graph.py`, `tsp.py` |
| Phase 4 | Performance Analysis | `benchmark.py` |
| Phase 5 | Final Report and Demonstration | `docs/report.md`, `outputs/screenshots/` |

## 🔮 11. Future Scope

Some possible improvements include:

- Interactive graphical user interface.
- Real-time delivery tracking.
- Integration with real-world map services.
- Multiple delivery vans with separate capacity constraints.
- Advanced route optimization algorithms.
- Database integration for parcel management.
- Automated delivery status notifications.

## 🏁 12. Conclusion

Mini-Courier Planner demonstrates how fundamental algorithmic concepts can be combined to solve a practical logistics problem.

By integrating sorting algorithms, Dynamic Programming, shortest-path algorithms, and route optimization, the project provides a structured approach to parcel selection and delivery planning.

It also demonstrates the importance of algorithm efficiency through performance benchmarking and complexity analysis.

The project bridges the gap between theoretical algorithm concepts and their practical implementation in real-world applications.

---

### 📜 Academic Information

Developed as part of the **Design & Analysis of Algorithms (ETCCDA302)** capstone assignment at K.R. Mangalam University.

**Developed by Ronit**

**Roll Number: 2501350026**

[GitHub Repository](https://github.com/ronits57/courier-planner-assignment)

*Built with Python 🐍*
