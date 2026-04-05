🥗 FlavorFlow Pro: Smart Canteen Optimization System

FlavorFlow Pro is an advanced Canteen Management and Logistics System built for the T.Y. B.Tech Computer Engineering curriculum.

The project demonstrates the practical application of Data Structures and Algorithms (DAA) strategies—including Divide & Conquer, Greedy, Dynamic Programming, Backtracking, and Branch & Bound—to solve real-world operational challenges in a canteen environment.

🚀 Key Features & Algorithm Mapping

The system is divided into five core modules, each mapped to a specific unit of the DAA syllabus.

1️⃣ Smart Menu Search

Unit II: Divide & Conquer

🔹 Feature

Instant food item lookup.

🔹 Algorithm

Binary Search — O(log n)

🔹 Comparative Analysis

Compared against:
Linear Search — O(n)

Demonstrates logarithmic efficiency on large datasets.

🔹 Large-Scale Arithmetic

Karatsuba Algorithm — O(n¹·⁵⁸)

Used for:
Bulk ingredient cost calculations

Demonstrates:
Master Theorem application

2️⃣ Multi-Stop Pickup

Unit II: Greedy Strategy

🔹 Feature

Calculates the shortest walking path for a user picking up multiple items from different stalls.

🔹 Algorithm

Dijkstra’s Algorithm — O(E log V)

🔹 Logic

Uses a Greedy approach to find:

Local shortest path
Global minimum path

From:
Entrance → Tables

3️⃣ Budget Meal Optimizer

Unit III: Dynamic Programming

🔹 Feature

Recommends the highest-value meal tray within a strict budget.

🔹 Algorithm

0/1 Knapsack — O(nW)

🔹 Comparative Analysis

Compared with:

Greedy Fractional Knapsack

Shows why:

Dynamic Programming is superior
for non-divisible real-world items

4️⃣ Staff & Kitchen Management

Unit II & IV: Greedy / Backtracking

🍳 Kitchen Scheduling

Uses:

Job Scheduling with Deadlines — Greedy

Purpose:

Prioritize high-profit orders
Optimize kitchen workflow
👨‍🍳 Staff Shift Assignment

Uses:

Graph Coloring — Backtracking

Ensures:

No overlapping shifts
No equipment conflicts
Efficient chef allocation
5️⃣ Delivery Logistics

Unit III & IV: DP / Branch & Bound

📍 All-Pairs Shortest Path

Algorithm:

Floyd–Warshall — O(V³)

Used to:

Pre-calculate stall distances
Speed up delivery routing
🤖 Robot Delivery Optimization

Algorithm:

Traveling Salesperson Problem (TSP)
Branch & Bound — Least Cost Search

Purpose:

Optimize robot delivery routes
Minimize total travel distance

Classification:

NP-Hard Problem

🛠️ Technology Stack
Component	Technology
Language	Python 3.10+
Framework	Streamlit
Visualization	Plotly Express
Data Handling	Pandas

Environment	Virtual Environment (venv)


📂 Folder Structure
FlavorFlow_System/
│
├── .venv/                  # Virtual Environment

├── main.py                 # Primary UI and Integration

├── requirements.txt        # Dependencies

│
├── core/                   # Algorithm Implementations

│   ├── searching.py        # Binary Search, Karatsuba

│   ├── optimization.py     # 0/1 Knapsack, Greedy Knapsack

│   ├── scheduling.py       # Job Scheduling

│   ├── pathfinding.py      # Dijkstra, Floyd-Warshall

│   └── constraints.py      # Graph Coloring, TSP B&B
│
├── data/                   # Mock Database

│   └── canteen_data.py     # Menu items, Prices, Stall Map

│
└── utils/                  # Helper Utilities

    └── metrics.py          # Execution Time Measurements
    

    
⚙️ Installation & Setup

Step 1 — Clone Repository

git clone https://github.com/yourusername/FlavorFlow_System.git

cd FlavorFlow_System

Step 2 — Create Virtual Environment

python -m venv .venv

Activate:

Windows

.venv\Scripts\activate

Linux / Mac

source .venv/bin/activate
Step 3 — Install Dependencies
pip install -r requirements.txt
Step 4 — Run Application
streamlit run main.py


📊 Algorithmic Lab

The system includes a Performance Lab that allows users to:

✅ Visualize growth of functions
✅ Compare Best Case vs Worst Case
✅ Analyze Time Complexity Trends
✅ Observe efficiency differences between algorithms
✅ Understand P vs NP Classification

Examples:

Search → P Problem
TSP → NP-Hard Problem
