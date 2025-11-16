import sys

INF = sys.maxsize

def floyd_warshall(graph):
    
    V = len(graph)
    # Inicializa la matriz de distancias y predecesores
    dist = [list(row) for row in graph]
    pred = [[None] * V for _ in range(V)]
    for i in range(V):
        for j in range(V):
            if graph[i][j] != 0 and graph[i][j] != INF:
                pred[i][j] = i

    # Bucle principal del algoritmo
    for k in range(V): # Vértice intermedio
        for i in range(V): # Vértice de origen
            for j in range(V): # Vértice de destino
                # Si pasar por k es más corto que la ruta actual
                if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j] # Actualiza el predecesor

    # Verifica si existen ciclos negativos
    for i in range(V):
        if dist[i][i] < 0:
            raise ValueError("El grafo contiene un ciclo de peso negativo.")

    return dist, pred

def print_solution(dist, pred, V):
    """Función para imprimir la matriz de distancias y las rutas."""
    print("Matriz de distancias más cortas:")
    for i in range(V):
        for j in range(V):
            if dist[i][j] == INF:
                print("%7s" % "INF", end="")
            else:
                print("%7d" % (dist[i][j]), end="")
        print()

    print("\nPredecesores (para reconstruir rutas):")
    for row in pred:
        print(row)

graph_example = [
    [0, 5, INF, 10],
    [INF, 0, 3, INF],
    [INF, INF, 0, 1],
    [INF, INF, INF, 0]
]

num_vertices = len(graph_example)
dist_matrix, pred_matrix = floyd_warshall(graph_example)
print_solution(dist_matrix, pred_matrix, num_vertices)
