# crdt_counter.py
import time
import json
import threading
import requests
from flask import Flask, request, jsonify
import argparse

class GCounter:
    """
    G-Counter (Grow-only Counter) CRDT.
    Permite incrementos concurrentes sin conflictos.
    """
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.values = [0] * num_nodes
    
    def increment(self, amount=1):
        """Incrementa el contador para este nodo."""
        self.values[self.node_id] += amount
    
    def merge(self, other_counter):
        """Fusiona con otro contador tomando el máximo para cada posición."""
        for i in range(len(self.values)):
            self.values[i] = max(self.values[i], other_counter.values[i])
    
    def value(self):
        """Obtiene el valor total del contador."""
        return sum(self.values)
    
    def to_dict(self):
        """Convierte el contador a un diccionario para serialización."""
        return {"values": self.values}
    
    @classmethod
    def from_dict(cls, data, node_id):
        """Crea un contador a partir de un diccionario deserializado."""
        counter = cls(node_id, len(data["values"]))
        counter.values = data["values"]
        return counter

class CRDTNode:
    def __init__(self, node_id, port, num_nodes, peer_ports=None):
        self.node_id = node_id
        self.port = port
        self.num_nodes = num_nodes
        self.peer_ports = peer_ports or []
        self.counter = GCounter(node_id, num_nodes)
        self.lock = threading.Lock()
        
        # Inicializar la aplicación Flask
        self.app = Flask(f"node-{node_id}")
        self.setup_routes()
        
        # Iniciar hilo de sincronización
        self.sync_thread = threading.Thread(target=self.sync_with_peers)
        self.sync_thread.daemon = True
        self.sync_thread.start()
    
    def setup_routes(self):
        @self.app.route('/increment', methods=['POST'])
        def increment():
            data = request.json
            amount = data.get('amount', 1)
            
            with self.lock:
                self.counter.increment(amount)
            
            return jsonify({
                "status": "success",
                "new_value": self.counter.value()
            })
        
        @self.app.route('/value', methods=['GET'])
        def get_value():
            with self.lock:
                return jsonify({
                    "value": self.counter.value(),
                    "components": self.counter.values
                })
        
        @self.app.route('/sync', methods=['POST'])
        def receive_sync():
            data = request.json
            
            with self.lock:
                remote_counter = GCounter.from_dict(data, self.node_id)
                self.counter.merge(remote_counter)
            
            return jsonify({"status": "sync_received"})
    
    def sync_with_peers(self):
        """Sincroniza periódicamente con otros nodos."""
        while True:
            time.sleep(5)  # Sincronizar cada 5 segundos
            
            with self.lock:
                counter_data = self.counter.to_dict()
            
            # Enviar datos a todos los peers
            for port in self.peer_ports:
                try:
                    requests.post(f"http://localhost:{port}/sync", json=counter_data, timeout=1)
                except requests.exceptions.RequestException as e:
                    print(f"Error sincronizando con nodo en puerto {port}: {e}")
    
    def run(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

def main():
    parser = argparse.ArgumentParser(description='Nodo CRDT (G-Counter)')
    parser.add_argument('--id', type=int, required=True, help='ID del nodo')
    parser.add_argument('--port', type=int, required=True, help='Puerto del nodo')
    parser.add_argument('--num-nodes', type=int, required=True, help='Número total de nodos')
    parser.add_argument('--peers', type=str, help='Puertos de los nodos pares (separados por comas)')
    
    args = parser.parse_args()
    
    peer_ports = []
    if args.peers:
        peer_ports = [int(p) for p in args.peers.split(',')]
    
    node = CRDTNode(args.id, args.port, args.num_nodes, peer_ports)
    node.run()

if __name__ == "__main__":
    main()