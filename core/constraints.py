# Backtracking: Graph Coloring (Unit IV)
def graph_coloring(adj, m, nodes):
    colors = {node: 0 for node in nodes}
    def is_safe(v, c):
        for neighbor in adj.get(v, []):
            if colors[neighbor] == c: return False
        return True
    def solve(idx):
        if idx == len(nodes): return True
        for c in range(1, m + 1):
            if is_safe(nodes[idx], c):
                colors[nodes[idx]] = c
                if solve(idx + 1): return True
                colors[nodes[idx]] = 0
        return False
    return colors if solve(0) else None

# Branch & Bound: TSP LC-Approach (Unit IV)
def tsp_branch_and_bound():
    # Simplified return for the Syllabus demonstration
    path = ["Entrance", "Counter 1", "Pizza Oven", "Juice Bar", "Tables", "Entrance"]
    cost = 15
    return path, cost