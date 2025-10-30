import time
import json
import threading
import requests
from flask import Flask, request, jsonify
import random
import argparse
from datetime import datetime

class Node:
    """
    Representa un nodo en un sistema distribuido con consistencia eventual,
    utilizando Vector Clocks para la detección y resolución de conflictos.
    """
    def __init__(self, node_id, port, peer_ports=None):
        self.node_id = node_id
        self.port = port
        self.peer_ports = peer_ports or []
        self.data = {}           # Almacén clave-valor (diccionario)
        self.vector_clocks = {}  # Vector clocks para cada clave (diccionario de diccionarios)
        self.lock = threading.Lock() # Bloqueo para proteger el acceso a 'data' y 'vector_clocks'
        
        # Inicializar la aplicación Flask
        self.app = Flask(f"node-{node_id}")
        self.setup_routes()
        
        # Iniciar hilo de sincronización
        self.sync_thread = threading.Thread(target=self.sync_with_peers)
        self.sync_thread.daemon = True
        self.sync_thread.start()
    
    def setup_routes(self):
        # Ruta de estado (para evitar 404 al visitar la raíz)
        @self.app.route('/', methods=['GET'])
        def home():
            return f"Nodo {self.node_id} activo en puerto {self.port}. Rutas disponibles: /get/<key>, /put, /sync. Peers: {', '.join(map(str, self.peer_ports))}"

        @self.app.route('/get/<key>', methods=['GET'])
        def get_value(key):
            with self.lock:
                if key in self.data:
                    return jsonify({
                        "key": key,
                        "value": self.data[key],
                        "vector_clock": self.vector_clocks.get(key, {})
                    })
                else:
                    return jsonify({"error": "Key not found"}), 404
        
        @self.app.route('/put', methods=['POST'])
        def put_value():
            data = request.json
            if not data or 'key' not in data or 'value' not in data:
                return jsonify({"error": "Missing key or value"}), 400
                
            key = data.get('key')
            value = data.get('value')
            client_vector_clock = data.get('vector_clock', {})
            
            with self.lock:
                # 1. Obtener el Vector Clock actual
                current_vector_clock = self.vector_clocks.get(key, {})
                
                # 2. Si hay un clock del cliente (sincronización o actualización con conocimiento previo)
                if client_vector_clock:
                    # Fusionar el clock local con el clock del cliente (tomar el máximo)
                    for node_id, count in client_vector_clock.items():
                        current_vector_clock[node_id] = max(current_vector_clock.get(node_id, 0), count)
                
                # 3. Incrementar el contador para este nodo (El evento acaba de ocurrir aquí)
                current_vector_clock[str(self.node_id)] = current_vector_clock.get(str(self.node_id), 0) + 1
                
                # 4. Actualizar datos y vector clock
                self.data[key] = value
                self.vector_clocks[key] = current_vector_clock
                
                return jsonify({
                    "status": "success",
                    "key": key,
                    "value": value,
                    "vector_clock": current_vector_clock
                })
        
        @self.app.route('/sync', methods=['POST'])
        def receive_sync():
            sync_data = request.json
            if not sync_data:
                 return jsonify({"status": "no_data"})

            with self.lock:
                for key, item in sync_data.items():
                    remote_value = item['value']
                    remote_vector_clock = item['vector_clock']
                    
                    if key not in self.data:
                        # Caso 1: Clave nueva, simplemente la añadimos
                        self.data[key] = remote_value
                        self.vector_clocks[key] = remote_vector_clock
                    else:
                        # Caso 2: Clave existente, comparamos vector clocks
                        local_vector_clock = self.vector_clocks[key]
                        
                        if self.is_concurrent(local_vector_clock, remote_vector_clock):
                            # Conflicto: Los dos valores son actualizaciones simultáneas.
                            
                            # Fusionar clocks antes de resolver, para no perder información de causalidad.
                            merged_clock = self.merge_vector_clocks(local_vector_clock, remote_vector_clock)
                            self.vector_clocks[key] = merged_clock

                            # Regla de desempate: Si los valores son diferentes, el nodo con el ID más alto 'gana'.
                            if self.data[key] != remote_value:
                                print(f"[Conflict for {key}] Local: {self.data[key]} vs Remote: {remote_value}. Merging clocks.")
                            
                                # Si el nodo local tiene un ID menor que el nodo que generó la última versión remota, usa el valor remoto.
                                if self.node_id < int(max(remote_vector_clock.keys(), key=int)):
                                     self.data[key] = remote_value
                                
                        elif self.happens_before(local_vector_clock, remote_vector_clock):
                            # El valor remoto es causalmente posterior (más reciente)
                            self.data[key] = remote_value
                            self.vector_clocks[key] = remote_vector_clock
                            # Si el valor local es más reciente, no hacemos nada (self.happens_before es False)
            
            return jsonify({"status": "sync_received"})
    
    def is_concurrent(self, vc1, vc2):
        """Determina si dos eventos son concurrentes según sus vector clocks."""
        less = False
        greater = False
        
        for node_id in set(vc1.keys()) | set(vc2.keys()):
            count1 = vc1.get(node_id, 0)
            count2 = vc2.get(node_id, 0)
            
            if count1 < count2:
                less = True
            elif count1 > count2:
                greater = True
            
        return less and greater  # Concurrentes si hay componentes donde vc1 > vc2 Y vc2 > vc1
    
    def happens_before(self, vc1, vc2):
        """Determina si vc1 sucedió causalmente antes que vc2 (vc1 -> vc2)."""
        less_equal = True
        strictly_less = False
        
        for node_id in set(vc1.keys()) | set(vc2.keys()):
            count1 = vc1.get(node_id, 0)
            count2 = vc2.get(node_id, 0)
            
            if count1 > count2:
                return False  # Si hay un componente donde vc1 es mayor, no hay relación causal (o es concurrente)
            if count1 < count2:
                strictly_less = True
        
        return strictly_less # vc1 es causalmente anterior a vc2 si es menor o igual en todas partes y estrictamente menor en al menos una.
    
    def merge_vector_clocks(self, vc1, vc2):
        """Fusiona dos vector clocks tomando el máximo para cada componente."""
        result = vc1.copy()
        
        for node_id, count in vc2.items():
            result[node_id] = max(result.get(node_id, 0), count)
        
        return result
    
    def sync_with_peers(self):
        """Sincroniza periódicamente con otros nodos."""
        while True:
            # Aumentamos el timeout a 5 segundos para reducir la probabilidad de ConnectTimeoutError 
            SYNC_TIMEOUT = 5 
            
            # Esperar 5 segundos antes de intentar sincronizar
            time.sleep(5) 
            
            with self.lock:
                # Sólo enviamos los datos que tenemos localmente
                sync_data = {
                    key: {
                        'value': self.data[key],
                        'vector_clock': self.vector_clocks.get(key, {})
                    }
                    for key in self.data
                }
            
            # Enviar datos a todos los peers
            for port in self.peer_ports:
                try:
                    # Usamos el timeout ajustado
                    response = requests.post(f"http://localhost:{port}/sync", json=sync_data, timeout=SYNC_TIMEOUT)
                    
                    if response.status_code == 200:
                         print(f"[{datetime.now().strftime('%H:%M:%S')}] Nodo {self.port}: Sincronización exitosa con el Nodo {port}")
                    else:
                         print(f"[{datetime.now().strftime('%H:%M:%S')}] Nodo {self.port}: Advertencia: Sincronización con Nodo {port} falló con estado {response.status_code}")

                except requests.exceptions.RequestException as e:
                    # Este error ahora usa el timeout de 5 segundos.
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Nodo {self.port}: Error: No se pudo conectar con el nodo en puerto {port}. El peer está caído. ({e})")
    
    def run(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

def main():
    parser = argparse.ArgumentParser(description='Nodo con consistencia eventual')
    parser.add_argument('--id', type=int, required=True, help='ID del nodo')
    parser.add_argument('--port', type=int, required=True, help='Puerto del nodo')
    parser.add_argument('--peers', type=str, help='Puertos de los nodos pares (separados por comas)')
    
    args = parser.parse_args()
    
    peer_ports = []
    if args.peers:
        peer_ports = [int(p) for p in args.peers.split(',')]
    
    node = Node(args.id, args.port, peer_ports)
    node.run()

if __name__ == "__main__":
    main()
