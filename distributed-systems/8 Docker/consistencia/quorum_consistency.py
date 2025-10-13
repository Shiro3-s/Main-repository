import time
import random
import threading
import os
from collections import defaultdict

class StorageNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}  # key -> (value, version)
        self.is_active = True
        self.lock = threading.Lock()
        self.log = []
    
    def log_event(self, event):
        timestamp = time.time()
        self.log.append((timestamp, event))
        print(f"[{time.strftime('%H:%M:%S')}] Nodo {self.node_id}: {event}")
    
    def read(self, key):
        if not self.is_active:
            return None, -1
        
        with self.lock:
            if key in self.data:
                value, version = self.data[key]
                self.log_event(f"Lee {key}={value} (versión {version})")
                return value, version
            else:
                self.log_event(f"Lee {key}=None (no existe)")
                return None, 0
    
    def write(self, key, value, version):
        if not self.is_active:
            return False
        
        with self.lock:
            current_version = 0
            if key in self.data:
                _, current_version = self.data[key]
            
            if version > current_version:
                self.data[key] = (value, version)
                self.log_event(f"Escribe {key}={value} (versión {version})")
                return True
            else:
                self.log_event(f"Rechaza escritura {key}={value} (versión {version}, actual {current_version})")
                return False
    
    def fail(self):
        with self.lock:
            self.is_active = False
            self.log_event("FALLA")
    
    def recover(self):
        with self.lock:
            self.is_active = True
            self.log_event("RECUPERADO")

class QuorumSystem:
    def __init__(self, num_nodes, read_quorum, write_quorum):
        self.nodes = [StorageNode(i) for i in range(num_nodes)]
        self.read_quorum = read_quorum
        self.write_quorum = write_quorum
        self.num_nodes = num_nodes
        self.log = []
        
        # Verificar que los quórums cumplen la condición R + W > N
        if read_quorum + write_quorum <= num_nodes:
            print(f"ADVERTENCIA: La condición R + W > N no se cumple ({read_quorum} + {write_quorum} <= {num_nodes})")
            print("Esto puede llevar a inconsistencias en los datos.")
    
    def log_event(self, event):
        timestamp = time.time()
        self.log.append((timestamp, event))
        print(f"[{time.strftime('%H:%M:%S')}] Sistema: {event}")
    
    def read_value(self, key):
        active_nodes = [node for node in self.nodes if node.is_active]
        
        if len(active_nodes) < self.read_quorum:
            self.log_event(f"Lectura de {key} FALLIDA: No hay suficientes nodos activos ({len(active_nodes)} < {self.read_quorum})")
            return None
        
        # Seleccionar nodos aleatorios para el quórum de lectura
        read_nodes = random.sample(active_nodes, self.read_quorum)
        
        # Leer de todos los nodos en el quórum
        results = []
        for node in read_nodes:
            value, version = node.read(key)
            results.append((value, version, node))
        
        # Encontrar el valor con la versión más alta
        if not results:
            return None
        
        max_version = max(version for _, version, _ in results)
        if max_version <= 0:
            self.log_event(f"Lectura de {key}: No existe en ningún nodo del quórum")
            return None
        
        # Obtener el valor con la versión más alta
        latest_value = next(value for value, version, _ in results if version == max_version)
        
        # Reparar nodos con versiones antiguas
        for value, version, node in results:
            if version < max_version:
                threading.Thread(target=self._repair_node, args=(node, key, latest_value, max_version)).start()
        
        self.log_event(f"Lectura de {key}={latest_value} (versión {max_version}) exitosa")
        return latest_value
    
    def _repair_node(self, node, key, value, version):
        """Reparar un nodo con una versión antigua del valor."""
        node.write(key, value, version)
    
    def write_value(self, key, value):
        active_nodes = [node for node in self.nodes if node.is_active]
        
        if len(active_nodes) < self.write_quorum:
            self.log_event(f"Escritura de {key}={value} FALLIDA: No hay suficientes nodos activos ({len(active_nodes)} < {self.write_quorum})")
            return False
        
        # Determinar la versión actual más alta
        max_version = 0
        for node in active_nodes:
            _, version = node.read(key)
            max_version = max(max_version, version)
        
        # Nueva versión
        new_version = max_version + 1
        
        # Seleccionar nodos aleatorios para el quórum de escritura
        write_nodes = random.sample(active_nodes, self.write_quorum)
        
        # Escribir en todos los nodos del quórum
        success_count = 0
        for node in write_nodes:
            if node.write(key, value, new_version):
                success_count += 1
        
        # La escritura es exitosa si se escribe en todos los nodos del quórum
        success = success_count == self.write_quorum
        
        if success:
            self.log_event(f"Escritura de {key}={value} (versión {new_version}) exitosa en {success_count} nodos")
        else:
            self.log_event(f"Escritura de {key}={value} PARCIAL: Solo {success_count}/{self.write_quorum} nodos")
        
        return success
    
    def simulate_node_failures(self, num_failures=2, duration=3):
        """Simula fallos aleatorios en los nodos."""
        # Seleccionar nodos aleatorios para fallar
        nodes_to_fail = random.sample(self.nodes, min(num_failures, len(self.nodes)))
        
        for node in nodes_to_fail:
            node.fail()
        
        self.log_event(f"{len(nodes_to_fail)} nodos han fallado")
        
        # Programar la recuperación después de la duración especificada
        threading.Timer(duration, self._recover_nodes, args=(nodes_to_fail,)).start()
    
    def _recover_nodes(self, nodes):
        """Recupera los nodos que han fallado."""
        for node in nodes:
            node.recover()
        
        self.log_event(f"{len(nodes)} nodos se han recuperado")

def simulate_client_operations(quorum_system):
    """Simula operaciones de cliente en el sistema de quórum."""
    # Realizar algunas escrituras iniciales
    quorum_system.write_value("contador", 0)
    quorum_system.write_value("nombre", "Sistema Distribuido")
    
    # Simular fallos de nodos después de un tiempo
    threading.Timer(2, quorum_system.simulate_node_failures).start()
    
    # Realizar operaciones de lectura y escritura
    for i in range(10):
        time.sleep(random.uniform(0.5, 1.5))
        
        # Decidir aleatoriamente entre lectura y escritura
        if random.random() < 0.7:  # 70% probabilidad de lectura
            key = random.choice(["contador", "nombre"])
            value = quorum_system.read_value(key)
        else:
            if random.random() < 0.5:
                # Incrementar contador
                current = quorum_system.read_value("contador")
                if current is not None:
                    quorum_system.write_value("contador", current + 1)
            else:
                # Actualizar nombre
                suffix = random.randint(1, 100)
                quorum_system.write_value("nombre", f"Sistema Distribuido {suffix}")

def print_final_state(quorum_system):
    """Imprime el estado final de todos los nodos."""
    print("\n" + "="*50)
    print("ESTADO FINAL DEL SISTEMA")
    print("="*50)
    
    for node in quorum_system.nodes:
        print(f"Nodo {node.node_id} ({'Activo' if node.is_active else 'Inactivo'}):")
        for key, (value, version) in node.data.items():
            print(f"  {key} = {value} (versión {version})")

def main():
    # Crear sistema de quórum con 5 nodos, quórum de lectura 3, quórum de escritura 3
    # Esto cumple R + W > N (3 + 3 > 5)
    quorum_system = QuorumSystem(5, 3, 3)
    
    print("Iniciando simulación de sistema de quórum...")
    
    # Simular operaciones de cliente
    simulate_client_operations(quorum_system)
    
    # Esperar a que terminen todas las operaciones
    time.sleep(10)
    
    # Imprimir estado final
    print_final_state(quorum_system)

if __name__ == "__main__":
    main()
