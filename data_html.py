import pandas as pd
import osmnx as ox
import folium

# Código para definir el grafo y los nodos
class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_edge(self, node, weight):
        self.edges[node] = weight

    def __str__(self):
        return f"Node {self.name}"

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_edge(self, node1, node2, weight):
        if node1 in self.nodes and node2 in self.nodes:
            self.nodes[node1].add_edge(node2, weight)
            self.nodes[node2].add_edge(node1, weight)

    def __str__(self):
        return f"Graph with {len(self.nodes)} nodes."

# Bounding box correcto para Lima Metropolitana
# (latitud_sur, latitud_norte, longitud_oeste, longitud_este)
distritos_lima = [
    "Ancón, Lima, Peru",
    "Ate, Lima, Peru",
    "Barranco, Lima, Peru",
    "Breña, Lima, Peru",
    "Carabayllo, Lima, Peru",
    "Chaclacayo, Lima, Peru",
    "Chorrillos, Lima, Peru",
    "Cieneguilla, Lima, Peru",
    "Comas, Lima, Peru",
    "El Agustino, Lima, Peru",
    "Independencia, Lima, Peru",
    "Jesús María, Lima, Peru",
    "La Molina, Lima, Peru",
    "La Victoria, Lima, Peru",
    "Lima, Lima, Peru",  # Cercado de Lima (Centro de Lima)
    "Lince, Lima, Peru",
    "Los Olivos, Lima, Peru",
    "Lurigancho, Lima, Peru",
    "Lurín, Lima, Peru",
    "Magdalena del Mar, Lima, Peru",
    "Miraflores, Lima, Peru",
    "Pachacámac, Lima, Peru",
    "Pucusana, Lima, Peru",
    "Pueblo Libre, Lima, Peru",
    "Puente Piedra, Lima, Peru",
    "Punta Hermosa, Lima, Peru",
    "Punta Negra, Lima, Peru",
    "Rímac, Lima, Peru",
    "San Bartolo, Lima, Peru",
    "San Borja, Lima, Peru",
    "San Isidro, Lima, Peru",
    "San Juan de Lurigancho, Lima, Peru",
    "San Juan de Miraflores, Lima, Peru",
    "San Luis, Lima, Peru",
    "San Martín de Porres, Lima, Peru",
    "San Miguel, Lima, Peru",
    "Santa Anita, Lima, Peru",
    "Santa María del Mar, Lima, Peru",
    "Santa Rosa, Lima, Peru",
    "Santiago de Surco, Lima, Peru",
    "Surquillo, Lima, Peru",
    "Villa El Salvador, Lima, Peru",
    "Villa María del Triunfo, Lima, Peru",

    # Distritos del Callao
    "Callao, Callao, Peru",
    "Bellavista, Callao, Peru",
    "Carmen de la Legua Reynoso, Callao, Peru",
    "La Perla, Callao, Peru",
    "La Punta, Callao, Peru",
    "Ventanilla, Callao, Peru",
    "Mi Perú, Callao, Peru"
]

# Descargar el grafo
G = ox.graph_from_place(distritos_lima, network_type='all_public')  # Solo calles transitables

# Crear una instancia del grafo según la estructura del archivo
street_graph = Graph()

# Añadir nodos y aristas del grafo de OSMnx a nuestro grafo
for node, data in G.nodes(data=True):
    street_graph.add_node(node)  # Añadir el nodo al grafo

# Añadir las aristas con la distancia como peso
for u, v, data in G.edges(data=True):
    distance = data.get('length', 1)  # Si no hay longitud, se asigna peso 1
    street_graph.add_edge(u, v, distance)

# Extraer nodos con sus coordenadas
nodes_data = []
node_mapping = {}  # Para mapear OSMnx IDs a nuestros IDs
idx = 0
for node, data in G.nodes(data=True):
    nodes_data.append({
        'node_id': idx, 
        'osm_id': node,
        'lat': data['y'], 
        'lon': data['x']
    })
    node_mapping[node] = idx
    idx += 1

# Guardar nodos en un archivo CSV
nodes_df = pd.DataFrame(nodes_data)
nodes_df.to_csv('lima_nodes.csv', index=False)

# Extraer aristas con sus distancias
edges_data = []
for u, v, data in G.edges(data=True):
    distance = data.get('length', 1)
    # Usar los IDs mapeados en lugar de los IDs de OSMnx
    edges_data.append({
        'node1': node_mapping[u], 
        'node2': node_mapping[v], 
        'distance': distance
    })

# Guardar aristas en otro archivo CSV
edges_df = pd.DataFrame(edges_data)
edges_df.to_csv('lima_edges.csv', index=False)

