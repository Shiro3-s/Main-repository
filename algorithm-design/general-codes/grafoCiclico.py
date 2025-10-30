
class Node:
    def __init__(self, value):
        self.value = value
        self.connections = []

class Edge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

def print_graph(start_node, visited=None):
    if visited is None:
        visited = set()
    
    # Si el nodo ya fue visitado, retornamos para evitar ciclos infinitos
    if start_node in visited:
        return
    
    visited.add(start_node)
    print(f"Nodo: {start_node.value}")
    
    for edge in start_node.connections:
        print(f"  → {edge.destination.value}")
        print_graph(edge.destination, visited)

# Crear nodos
node_a = Node("A")
node_b = Node("B") 
node_c = Node("C")

# Crear conexiones
edge_ab = Edge(node_a, node_b)
edge_bc = Edge(node_b, node_c)
edge_ca = Edge(node_c, node_a)

# Agregar conexiones a los nodos
node_a.connections.append(edge_ab)
node_b.connections.append(edge_bc)
node_c.connections.append(edge_ca)

# Imprimir el grafo
print("Estructura del grafo cíclico:")
print_graph(node_a)
node_a.connections.append(edge_ab)
node_b.connections.append(edge_bc)
node_c.connections.append(edge_ca)

