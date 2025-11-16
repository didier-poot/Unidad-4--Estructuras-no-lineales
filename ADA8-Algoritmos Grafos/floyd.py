import sys

INF = sys.maxsize

def floyd_warshall(graph):
    V = len(graph)
    dist = list(map(lambda i: list(i), graph))
    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

if __name__ == "__main__":
    graph = [
        [0, 5, INF, 10],
        [INF, 0, 3, INF],
        [INF, INF, 0, 1],
        [INF, INF, INF, 0]
    ]

    distances = floyd_warshall(graph)

    print("Las distancias más cortas entre todos los pares de nodos son:")
    for row in distances:
        print(row)

