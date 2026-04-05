# core/pathfinding.py
import heapq

# --- UNIT II: GREEDY (Dijkstra) ---
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            path = path + [node]
            if node == end: return cost, path
            seen.add(node)
            for next_node, weight in graph.get(node, {}).items():
                heapq.heappush(queue, (cost + weight, next_node, path))
    return float("inf"), []

# --- INTEGRATED FEATURE: MULTI-ITEM PICKUP ROUTE ---
def get_multi_stop_route(graph, stops):
    """
    Calculates a greedy multi-stop route starting at 'Entrance',
    visiting all required stalls, and ending at 'Tables'.
    """
    full_path = ['Entrance']
    current_node = 'Entrance'
    total_time = 0
    
    # Unique list of stalls to visit
    remaining_stalls = list(set(stops))
    
    while remaining_stalls:
        best_time = float('inf')
        next_stall = None
        best_path = []
        
        # Find the nearest stall from the current position
        for stall in remaining_stalls:
            time, path = dijkstra(graph, current_node, stall)
            if time < best_time:
                best_time = time
                next_stall = stall
                best_path = path
        
        if next_stall:
            total_time += best_time
            full_path.extend(best_path[1:]) # Add path excluding the start node
            current_node = next_stall
            remaining_stalls.remove(next_stall)
        else:
            break
            
    # Finally, go to Tables
    time_to_table, path_to_table = dijkstra(graph, current_node, 'Tables')
    total_time += time_to_table
    full_path.extend(path_to_table[1:])
    
    return total_time, full_path

# --- UNIT III: DYNAMIC PROGRAMMING (Floyd-Warshall) ---
def floyd_warshall(graph, nodes):
    # Initialize distance matrix
    dist = {n1: {n2: float('inf') for n2 in nodes} for n1 in nodes}
    for n in nodes: dist[n][n] = 0
    
    # Fill in direct edges
    for u in graph:
        for v, w in graph[u].items():
            dist[u][v] = w
            
    # Triple loop DP approach
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist