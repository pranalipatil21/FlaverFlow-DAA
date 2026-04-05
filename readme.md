
🥗 FlavorFlow Pro: Smart Canteen Optimization System

FlavorFlow Pro is an advanced Canteen Management and Logistics system built for the T.Y. B.Tech Computer Engineering curriculum. The project demonstrates the practical application of Data Structures and Algorithms (DAA) strategies—including Divide & Conquer, Greedy, Dynamic Programming, Backtracking, and Branch & Bound—to solve real-world operational challenges in a canteen environment.

🚀 Key Features & Algorithm Mapping

The system is divided into five core modules, each mapped to a specific unit of the DAA syllabus:

1. Smart Menu Search (Unit II: Divide & Conquer)

Feature: Instant food item lookup.

Algorithm: Binary Search (
𝑂
(
log
⁡
𝑛
)
O(logn)
).

Comparative Analysis: Compared against Linear Search (
𝑂
(
𝑛
)
O(n)
) to demonstrate logarithmic efficiency.

Large-Scale Arithmetic: Implementation of the Karatsuba Algorithm (
𝑂
(
𝑛
1.58
)
O(n
1.58
)
) for bulk ingredient cost calculations, demonstrating the Master Theorem in action.

2. Multi-Stop Pickup (Unit II: Greedy Strategy)

Feature: Calculates the shortest walking path for a user picking up multiple items from different stalls.

Algorithm: Dijkstra’s Algorithm (
𝑂
(
𝐸
log
⁡
𝑉
)
O(ElogV)
).

Logic: Uses a Greedy approach to find the local shortest path to the next stall, ensuring the global path from 'Entrance' to 'Tables' is minimized.

3. Budget Meal Optimizer (Unit III: Dynamic Programming)

Feature: Recommends the highest-calorie/highest-value meal tray based on a user's strict budget.

Algorithm: 0/1 Knapsack Problem using DP (
𝑂
(
𝑛
𝑊
)
O(nW)
).

Comparative Analysis: Compared against the Greedy Fractional Knapsack to show why DP is superior for non-divisible real-world items.

4. Staff & Kitchen Management (Unit II & IV: Greedy/Backtracking)

Kitchen Scheduling: Uses Job Scheduling with Deadlines (Greedy) to prioritize high-profit orders.

Staff Shifts: Uses Graph Coloring (Backtracking) to assign shift slots to chefs, ensuring that no two chefs using the same equipment have overlapping schedules.

5. Delivery Logistics (Unit III & IV: DP / Branch & Bound)

All-Pairs Shortest Path: Uses Floyd-Warshall (
𝑂
(
𝑉
3
)
O(V
3
)
) to pre-calculate distances between all canteen stalls.

Robot Delivery: Solves the Traveling Salesperson Problem (TSP) using Branch and Bound (Least-Cost Search) to optimize the delivery cycle for NP-Hard logistics.

🛠️ Technology Stack

Language: Python 3.10+

Framework: Streamlit (For the modern White & Orange UI)

Visualization: Plotly Express (High-quality, grid-less performance graphs)

Data Handling: Pandas

Environment: Virtual Environment (venv)

📂 Folder Structure
code
Text
download
content_copy
expand_less
FlavorFlow_System/
│
├── .venv/                  # Virtual Environment
├── main.py                 # Primary UI and Integration
├── requirements.txt        # Dependencies (Streamlit, Plotly, Pandas)
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
    └── metrics.py          # Execution time measurements
⚙️ Installation & Setup

Clone the Repository:

git clone https://github.com/yourusername/FlavorFlow_System.git
cd FlavorFlow_System

Create & Activate Virtual Environment:

python -m venv .venv
.venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Run the Application:

streamlit run main.py

📊 Algorithmic Lab

The project includes a dedicated Performance Lab where users can:

Visualize the growth of functions through execution steps.

Compare "Best Case" vs "Worst Case" scenarios.

View White-Themed Graphs (with no gridlines) showing the efficiency gap between different algorithmic strategies.

Understand the P vs NP classification for problems like Search (P) vs TSP (NP-Hard).

🎨 UI/UX Design

Theme: Modern SaaS-style Orange and White.

Typography: Solid Black high-contrast text for professional readability.

Imagery: High-definition, uniform-sized food and canteen-related visuals on every page.

Responsiveness: Fully interactive sliders, multiselect boxes, and real-time path updates.

Developed for the Department of Computer Engineering (T.Y. B.Tech)