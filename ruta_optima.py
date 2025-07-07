import pandas as pd
import folium
import heapq
import random

# Cargar datos de nodos y arcos desde archivos CSV
nodes_df = pd.read_csv('lima_nodes.csv')
edges_df = pd.read_csv('lima_edges.csv')

# Limpiar nombres de columna
nodes_df.columns = nodes_df.columns.str.strip()
edges_df.columns = edges_df.columns.str.strip()

# Construir grafo como diccionario de adyacencia
graph = {int(row['node_id']): [] for _, row in nodes_df.iterrows()}
for _, row in edges_df.iterrows():
    u = int(row['node1'])
    v = int(row['node2'])
    w = float(row['distance'])
    if u in graph:
        graph[u].append((v, w))

# Definir nodo de origen (UPC)
start_node = 258920  # Ajusta según el node_id de la UPC en lima_nodes.csv
if start_node not in graph:
    raise ValueError(f"start_node {start_node} no está definido en el grafo de nodos CSV")

# Algoritmo de Dijkstra
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev

# Reconstruir camino desde start hasta end
def reconstruct_path(prev, start, end):
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = prev[curr]
    return path[::-1]

# TSP utilizando el algoritmo de Held-Karp
def tsp_held_karp(graph, nodes):
    n = len(nodes)
    if n == 0:
        return []

    dist_matrix = [[[float('inf'), []] for _ in range(n)] for _ in range(n)]
    for i, u in enumerate(nodes):
        dist_matrix[i][i][0] = 0
        dist, prev = dijkstra(graph, u)
        for j, v in enumerate(nodes):
            if u != v and dist[v] < float('inf'):
                dist_matrix[i][j] = [dist[v], reconstruct_path(prev, u, v)]

    
    matrix_dist = [dist_matrix[i][j][0] for i in range(n) for j in range(n)]
    print("Matriz de distancias:", matrix_dist)
    # Aplicar el algoritmo de Held-Karp
    ALL = 1 << n
    dp = [[float('inf')] * n for _ in range(ALL)]
    previos = [[-1] * n for _ in range(ALL)]
    
    # Estado inicial: solo el nodo 0 visitado
    dp[1][0] = 0
    
    for mask in range(1, ALL):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
                
            for v in range(n):
                if v == u or (mask & (1 << v)) or dist_matrix[u][v][0] == float('inf'):
                    continue
                
                nextmask = mask | (1 << v)
                newDist = dp[mask][u] + dist_matrix[u][v][0]

                if newDist < dp[nextmask][v]:
                    dp[nextmask][v] = newDist
                    previos[nextmask][v] = (u, dist_matrix[u][v][1])


    # Cerramos el camino volviendo al nodo de inicio
    lastNode = -1
    min_cost = float('inf')

    for u in range(1, n):
        cost = dp[ALL - 1][u] + dist_matrix[u][0][0]
        if cost < min_cost:
            min_cost = cost
            lastNode = u
            previos[ALL - 1][0] = (u, dist_matrix[u][0][1])

    pathNodes = []
    pathEdges = []
    # Reconstruir el camino
    
    mask = ALL - 1
    curr = lastNode

    pathEdges.append(dist_matrix[curr][0][1]) # Añadimos el camino del ultimo nodo al inicio

    while previos[mask][curr] != -1:
        pathNodes.append(nodes[curr])
        prev, edges = previos[mask][curr]
        pathEdges.append(edges)
        mask = mask ^ (1 << curr)
        curr = prev
    pathEdges.reverse()

    return pathEdges[::-1]

# Seleccionar nodos para incluir en el TSP
available = [nid for nid in graph if nid != start_node]
other_nodes = random.sample(available, 3)
list_nodes = [start_node] + other_nodes

# Crear mapa interactivo con Folium
map_center = [nodes_df['y'].mean(), nodes_df['x'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Dibujar marcadores de inicio y nodos seleccionados
for nid in list_nodes:
    df = nodes_df[nodes_df['node_id'] == nid]
    if df.empty:
        continue
    y, x = df.iloc[0][['y', 'x']]
    folium.CircleMarker(
        location=[y, x],
        radius=6,
        color='red' if nid == start_node else 'blue',
        fill=True,
        fill_color='red' if nid == start_node else 'blue',
        fill_opacity=0.7
    ).add_to(m)

# Calcular tour TSP exacto y trazar ruta
tourEdges = tsp_held_karp(graph, list_nodes)

if not tourEdges:
    raise RuntimeError("No se encontró un tour completo con los nodos seleccionados")

# Trazar cada segmento
for tourEdge in tourEdges:
    for u, v in zip(tourEdge[:-1], tourEdge[1:]):
        df1 = nodes_df[nodes_df['node_id'] == u]
        df2 = nodes_df[nodes_df['node_id'] == v]
        if df1.empty or df2.empty:
            continue
        y1, x1 = df1.iloc[0][['y', 'x']]
        y2, x2 = df2.iloc[0][['y', 'x']]
        folium.PolyLine(
            locations=[(y1, x1), (y2, x2)],
            color='green',
            weight=3,
            opacity=0.8
        ).add_to(m)

# Guardar mapa final con ruta exacta
dest_file = 'lima_streets_map_tsp_exact.html'
m.save(dest_file)