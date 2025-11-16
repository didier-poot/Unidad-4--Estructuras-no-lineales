import heapq

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    priority_queue = [(0, start_node)]
    
    previous_nodes = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous_nodes

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
distances, previous_nodes = dijkstra(graph, start_node)

print(f"Distancias más cortas desde {start_node}: {distances}")

path = []
current = 'D'
while current != start_node:
    path.insert(0, current)
    current = previous_nodes[current]
path.insert(0, start_node)
print(f"Camino más corto a 'D': {' -> '.join(path)}")

