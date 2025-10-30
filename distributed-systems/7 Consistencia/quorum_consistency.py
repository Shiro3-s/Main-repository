import time
import json
import threading
import requests
from flask import Flask, request, jsonify
import random
import argparse
from datetime import datetime
import concurrent.futures

# Define Consistency Levels (usando constantes para claridad)
CONSISTENCY_LEVELS = {
    "ONE": 1,
    "QUORUM": 2, 
    "ALL": 3     
}

class QuorumNode:
    """
    Implementa un nodo de almacenamiento distribuido que utiliza el modelo de
    Consistencia de Quórum (R + W > N) con timestamps para la resolución de conflictos.
    Incluye Read Repair, niveles de consistencia y Hinted Handoff.
    """
    def __init__(self, node_id, port, peer_ports=None, read_quorum=2, write_quorum=2):
        self.node_id = node_id
        self.port = port
        self.peer_ports = peer_ports or []
        self.data = {}           # Almacén clave-valor (diccionario)
        self.timestamps = {}     # Timestamps para cada clave
        self.lock = threading.Lock()
        
        # N: Número total de nodos en el clúster (local + pares)
        self.N = 1 + len(self.peer_ports) 
        self.read_quorum = read_quorum
        self.write_quorum = write_quorum

        # Hinted Handoff storage: {port: [{key, value, timestamp}, ...]}
        self.hints = {}
        self.hints_lock = threading.Lock() 

        # --- Validación de Consistencia de Quórum ---
        if self.read_quorum + self.write_quorum <= self.N:
            print(f"ADVERTENCIA: Quórums (R={self.read_quorum}, W={self.write_quorum}) no garantizan consistencia fuerte (R+W > N={self.N}).")
        
        # Validación de mínimo quórum
        if self.read_quorum > self.N or self.write_quorum > self.N:
             raise ValueError(f"El quórum de lectura ({self.read_quorum}) o escritura ({self.write_quorum}) no puede ser mayor que el número total de nodos ({self.N}).")
        
        # Inicializar la aplicación Flask
        self.app = Flask(f"node-{node_id}")
        self.setup_routes()

        # Inicia Hinted Handoff background thread
        self.handoff_thread = threading.Thread(target=self.process_hints, daemon=True)
        self.handoff_thread.start()
    
    # --- Lógica de Hinted Handoff ---
    def process_hints(self, interval=5):
        """Intenta entregar las escrituras perdidas a los nodos que han vuelto a estar en línea."""
        print(f"[{self.node_id}] Hilo de Hinted Handoff iniciado.")
        while True:
            time.sleep(interval)
            
            with self.hints_lock:
                ports_to_check = list(self.hints.keys())
            
            for port in ports_to_check:
                if self.is_node_up(port):
                    self.deliver_hints(port)

    def is_node_up(self, port):
        """Verifica si un nodo está activo enviando una solicitud GET simple."""
        try:
            requests.get(f"http://localhost:{port}/", timeout=1)
            return True
        except requests.exceptions.RequestException:
            return False

    def deliver_hints(self, port):
        """Entrega los hints al nodo recién recuperado."""
        with self.hints_lock:
            # Se usa pop para asegurar que solo un hilo lo procese y se elimine al completarse
            hints_to_deliver = self.hints.pop(port, [])

        if not hints_to_deliver:
            return

        print(f"[{self.node_id}] Entregando {len(hints_to_deliver)} hints al nodo {port}...")
        
        success_count = 0
        for hint in hints_to_deliver:
            # Reutiliza el método interno de escritura para entregar el hint
            result = self.write_to_node(port, hint['key'], hint['value'], hint['timestamp'])
            if result and result.get("status") == "success":
                success_count += 1
                
        print(f"[{self.node_id}] Entrega de hints al nodo {port} completada. Exitosos: {success_count}/{len(hints_to_deliver)}")
    
    # --- Lógica de Consistencia ---
    def get_required_quorum_size(self, level, op_type):
        """Calcula el tamaño de quórum requerido basado en el nivel de consistencia."""
        N = self.N
        
        if op_type == 'read':
            default_quorum = self.read_quorum
        elif op_type == 'write':
            default_quorum = self.write_quorum
        else:
            raise ValueError("Invalid operation type")

        if level == "ONE":
            return 1
        elif level == "QUORUM":
            return default_quorum
        elif level == "ALL":
            return N
        else:
            # Fallback to default Quorum level if invalid level is provided
            print(f"ADVERTENCIA: Nivel de consistencia '{level}' inválido. Usando QUORUM ({default_quorum}).")
            return default_quorum

    def perform_read_repair(self, chosen_value, all_results):
        """Implementa Read Repair: Actualiza los nodos con valores desactualizados."""
        latest_timestamp = chosen_value['timestamp']
        latest_key = chosen_value['key']
        latest_value = chosen_value['value']
        
        outdated_ports = []

        for result in all_results:
            # Solo consideramos resultados válidos que no sean el nodo local (el local se repara implícitamente si fue el elegido)
            if result.get("node_id") != self.node_id and result.get("timestamp", 0) < latest_timestamp:
                outdated_ports.append(result.get("node_id"))
            
            # Nota: Si el valor elegido proviene de un par, el nodo local también puede estar desactualizado.
            # Sin embargo, el read repair solo repara pares. El cliente es responsable de usar el valor retornado.

        # Inicia reparaciones asíncronas para los nodos pares desactualizados
        if outdated_ports:
            print(f"[{self.node_id}] Iniciando reparación de lectura para nodos desactualizados: {outdated_ports}")
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for port in outdated_ports:
                    executor.submit(
                        self.write_to_node, 
                        port, 
                        latest_key, 
                        latest_value, 
                        latest_timestamp
                    )
    
    def handle_hinted_handoff(self, key, value, timestamp, write_results):
        """Almacena un 'hint' (pista) para los nodos que fallaron en la escritura."""
        failed_ports = []
        for result in write_results:
            # Si el resultado es 'error' (nodo caído) y el puerto no es el nodo local
            if result.get("status") == "error" and result.get("node_id") != self.node_id:
                failed_ports.append(result.get("node_id"))
        
        if failed_ports:
            print(f"[{self.node_id}] Nodos no disponibles para Handoff: {failed_ports}. Almacenando hints.")
            
            hint = {"key": key, "value": value, "timestamp": timestamp}
            
            with self.hints_lock:
                for port in failed_ports:
                    if port not in self.hints:
                        self.hints[port] = []
                    self.hints[port].append(hint)

    def setup_routes(self):
        
        @self.app.route('/', methods=['GET'])
        def home():
            return f"Nodo {self.node_id} activo en puerto {self.port}. Nodos totales (N): {self.N}. Quórum de Lectura (R): {self.read_quorum}. Quórum de Escritura (W): {self.write_quorum}. Rutas principales: /get/<key>, /put"
        
        # --- Rutas que implementan el Quórum (Lectura para el Cliente) ---
        @self.app.route('/get/<key>', methods=['GET'])
        def client_read(key):
            """Endpoint para lecturas de clientes con quórum (consulta R nodos), ahora soporta niveles de consistencia."""
            # Obtiene el nivel de consistencia de la query string, o usa 'QUORUM' por defecto
            level = request.args.get('consistency', 'QUORUM').upper()
            required_r = self.get_required_quorum_size(level, 'read')

            # 1. Obtener todas las respuestas
            results = self.read_from_peers(key)
            
            # Contar nodos que respondieron y tenían el valor
            successful_responses = len([r for r in results if r is not None and "error" not in r])

            if successful_responses < required_r:
                print(f"Error: Falló al alcanzar el quórum de lectura '{level}' (R={required_r}). Respuestas: {successful_responses}")
                return jsonify({"error": f"Failed to reach read consistency level {level} ({required_r} nodes needed)"}), 503
            
            # 2. Filtrar resultados válidos y encontrar el más reciente
            valid_results = [r for r in results if r and "error" not in r]
            valid_results.sort(key=lambda x: x['timestamp'], reverse=True)
            chosen = valid_results[0]
            
            # 3. Implementar Read Repair (Ejecución asíncrona)
            self.perform_read_repair(chosen, valid_results)

            return jsonify({
                "key": chosen["key"],
                "value": chosen["value"],
                "timestamp": chosen["timestamp"],
                "source_node": chosen.get("node_id", self.node_id),
                "consistency_level": level
            })
        
        # --- Rutas que implementan el Quórum (Escritura para el Cliente) ---
        @self.app.route('/put', methods=['POST'])
        def client_write():
            """Endpoint para escrituras de clientes con quórum (escribe en W nodos), ahora soporta niveles de consistencia y Hinted Handoff."""
            data = request.json
            key = data.get('key')
            value = data.get('value')
            # Obtiene el nivel de consistencia del cuerpo JSON, o usa 'QUORUM' por defecto
            level = data.get('consistency', 'QUORUM').upper()

            if not key or not value:
                return jsonify({"error": "Missing key or value in request"}), 400
                
            timestamp = time.time()
            required_w = self.get_required_quorum_size(level, 'write')
            
            # 1. Escribir en todos los nodos (local + pares)
            results = self.write_to_peers(key, value, timestamp)
            
            # Contamos las confirmaciones
            success_count = sum(1 for r in results if r.get("status") == "success")
            
            # 2. Verificar Quórum
            if success_count < required_w:
                print(f"Error: Falló al alcanzar el quórum de escritura '{level}' (W={required_w}). Confirmaciones: {success_count}")
                return jsonify({"error": f"Failed to reach write consistency level {level} ({required_w} nodes needed)"}), 503
            
            # 3. Handle Hinted Handoff for failed nodes (Ejecución asíncrona)
            self.handle_hinted_handoff(key, value, timestamp, results)
            
            return jsonify({
                "status": "success",
                "key": key,
                "value": value,
                "timestamp": timestamp,
                "confirmed_nodes": success_count,
                "consistency_level": level
            })

        # --- Rutas Internas (para comunicación entre Nodos) ---
        @self.app.route('/read_request/<key>', methods=['GET'])
        def read_request(key):
            """Endpoint interno para solicitudes de lectura de otros nodos (Devuelve valor local)."""
            with self.lock:
                if key in self.data:
                    return jsonify({
                        "key": key,
                        "value": self.data[key],
                        "timestamp": self.timestamps.get(key, 0)
                    })
                else:
                    return jsonify({"error": "Key not found"}), 404
        
        @self.app.route('/write_request', methods=['POST'])
        def write_request():
            """Endpoint interno para solicitudes de escritura de otros nodos (Actualiza valor local)."""
            data = request.json
            key = data.get('key')
            value = data.get('value')
            timestamp = data.get('timestamp', 0)
            
            if not key or not value:
                 return jsonify({"status": "error", "message": "Missing key/value"}), 400
            
            with self.lock:
                current_timestamp = self.timestamps.get(key, 0)
                
                # Solo actualizar si el timestamp es más reciente
                if timestamp > current_timestamp:
                    self.data[key] = value
                    self.timestamps[key] = timestamp
                    return jsonify({"status": "success"})
                else:
                    # Indica que el nodo no fue actualizado porque tenía una versión más nueva o igual
                    return jsonify({"status": "outdated"}) 

    
    def read_from_peers(self, key):
        """Solicita el valor de una clave a todos los nodos (local + pares)."""
        results = []
        
        # Leer del nodo local (siempre se incluye)
        with self.lock:
            if key in self.data:
                results.append({
                    "key": key,
                    "value": self.data[key],
                    "timestamp": self.timestamps.get(key, 0),
                    "node_id": self.node_id
                })
        
        # Leer de los nodos pares en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_port = {
                executor.submit(self.read_from_node, port, key): port
                for port in self.peer_ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"Error leyendo de nodo en puerto {port}: {e}")
        
        return results
    
    def read_from_node(self, port, key):
        """Lee una clave de un nodo específico."""
        try:
            # Aumentamos el timeout para mayor fiabilidad
            response = requests.get(f"http://localhost:{port}/read_request/{key}", timeout=3)
            if response.status_code == 200:
                data = response.json()
                data["node_id"] = port 
                return data
            else:
                return {"error": response.text, "node_id": port, "timestamp": 0}
        except requests.exceptions.RequestException:
            # Retorna None si el nodo no está disponible (caído)
            return None 
    
    def write_to_peers(self, key, value, timestamp):
        """Escribe un valor en todos los nodos (local + pares)."""
        results = []
        
        # 1. Escribir en el nodo local
        with self.lock:
            current_timestamp = self.timestamps.get(key, 0)
            if timestamp > current_timestamp:
                self.data[key] = value
                self.timestamps[key] = timestamp
                results.append({"status": "success", "node_id": self.node_id})
            else:
                results.append({"status": "outdated", "node_id": self.node_id})

        # 2. Escribir en los nodos pares en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_port = {
                executor.submit(self.write_to_node, port, key, value, timestamp): port
                for port in self.peer_ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result:
                        result["node_id"] = port
                        results.append(result)
                    else:
                        # Si es None, el nodo no respondió (está caído), se registra como error para Hinted Handoff
                        results.append({"status": "error", "node_id": port})
                except Exception as e:
                    print(f"Error escribiendo en nodo en puerto {port}: {e}")
                    results.append({"status": "error", "node_id": port}) # Contar como fallo

        return results
    
    def write_to_node(self, port, key, value, timestamp):
        """Escribe un valor en un nodo específico."""
        try:
            # Aumentamos el timeout para mayor fiabilidad
            response = requests.post(
                f"http://localhost:{port}/write_request",
                json={"key": key, "value": value, "timestamp": timestamp},
                timeout=3
            )
            if response.status_code == 200:
                return response.json()
            else:
                # Si la respuesta no es 200, retornamos un error.
                return {"status": "error", "message": response.text}
        except requests.exceptions.RequestException:
            return None # El nodo está caído
    
    def run(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

def main():
    parser = argparse.ArgumentParser(description='Nodo con consistencia de quórum')
    parser.add_argument('--id', type=int, required=True, help='ID del nodo')
    parser.add_argument('--port', type=int, required=True, help='Puerto del nodo')
    parser.add_argument('--peers', type=str, help='Puertos de los nodos pares (separados por comas)')
    parser.add_argument('--read-quorum', type=int, default=2, help='Tamaño del quórum de lectura (R)')
    parser.add_argument('--write-quorum', type=int, default=2, help='Tamaño del quórum de escritura (W)')
    
    args = parser.parse_args()
    
    peer_ports = []
    if args.peers:
        peer_ports = [int(p) for p in args.peers.split(',')]
    
    try:
        node = QuorumNode(args.id, args.port, peer_ports, args.read_quorum, args.write_quorum)
        node.run()
    except ValueError as e:
        print(f"Error de configuración: {e}")

if __name__ == "__main__":
    main()
