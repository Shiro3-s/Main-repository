class Node:
    # Clase para crear nodos del árbol
    def __init__(self, value):
        self.value = value  # Valor almacenado en el nodo
        self.left = None    # Referencia al hijo izquierdo
        self.right = None   # Referencia al hijo derecho

class BinaryTree:
    # Clase principal del árbol binario de búsqueda
    def __init__(self):
        self.root = None    # Inicializa el árbol con raíz vacía
    
    def insert(self, value):
        # Método público para insertar un valor en el árbol
        self.root = self._insert_recursive(self.root, value)
        
    def _insert_recursive(self, node, value):
        # Método recursivo privado para insertar un valor
        if node is None:
            return Node(value)  # Si el nodo es vacío, crea uno nuevo
        
        # Inserta en el subárbol izquierdo si el valor es menor
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            # Inserta en el subárbol derecho si el valor es mayor o igual
            node.right = self._insert_recursive(node.right, value)
        
        return node
    
    def search(self, value):
        # Método público para buscar un valor en el árbol
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        # Método recursivo privado para buscar un valor
        if node is None:
            return False    # Si llega a un nodo vacío, el valor no existe
        
        if node.value == value:
            return True     # Si encuentra el valor, retorna verdadero
        
        # Busca en el subárbol izquierdo si el valor es menor
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            # Busca en el subárbol derecho si el valor es mayor
            return self._search_recursive(node.right, value)
    
    def inorder_traversal(self, node):
        # Recorrido inorden del árbol (izquierda-raíz-derecha)
        if node is not None:
            self.inorder_traversal(node.left)    # Visita subárbol izquierdo
            print(node.value, end=" ")           # Visita nodo actual
            self.inorder_traversal(node.right)   # Visita subárbol derecho
    
    def print_tree(self):
        # Método para imprimir el árbol de forma visual
        lines = []
        self._print_tree_recursive(self.root, 0, lines)
        for line in lines:
            print(line)
    
    def _print_tree_recursive(self, node, level, lines):
        # Método recursivo privado para imprimir el árbol
        if node is not None:
            if len(lines) <= level:
                lines.append("")
            
            # Procesa hijo derecho
            self._print_tree_recursive(node.right, level + 1, lines)
            
            # Agrega espaciado para niveles superiores
            if level > 0:
                lines[level] += "    "
            
            # Agrega el valor del nodo actual
            lines[level] += str(node.value)
            
            # Procesa hijo izquierdo
            self._print_tree_recursive(node.left, level + 1, lines)


# Crear un nuevo árbol
tree = BinaryTree()

# Insertar valores de ejemplo
tree.insert(5)
tree.insert(3)
tree.insert(7)
tree.insert(2)
tree.insert(4)
tree.insert(6)
tree.insert(8)

# Ejemplos de búsqueda
print(tree.search(4))  # Verdadero - el valor 4 existe
print(tree.search(9))  # Falso - el valor 9 no existe

# Mostrar recorrido inorden
print("Inorder traversal:")
tree.inorder_traversal(tree.root)

# Mostrar árbol de forma visual
print("\nÁrbol visual:")
tree.print_tree()