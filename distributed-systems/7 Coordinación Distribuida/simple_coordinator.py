import time
import threading
import zmq
import json
from collections import defaultdict

class CoordinationService:
    def __init__(self, port=5555):
        self.port = port
        self.data = {}  # Almacén clave-valor
        self.watches = defaultdict(set)  # Observadores por clave
        self.lock = threading.Lock()
        self.active = True
        
        # Configuración de ZeroMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{self.port}")
        
        # Iniciar hilo de servicio
        self.service_thread = threading.Thread(target=self.run_service)
        self.service_thread.daemon = True
    
    def start(self):
        print(f"Servicio de coordinación iniciado en puerto {self.port}")
        self.service_thread.start()
    
    def run_service(self):
        while self.active:
            try:
                message = self.socket.recv_json()
                response = self.process_request(message)
                self.socket.send_json(response)
            except Exception as e:
                print(f"Error en el servicio: {e}")
                self.socket.send_json({"status": "error", "message": str(e)})
    
    def process_request(self, request):
        operation = request.get("operation")
        path = request.get("path")
        
        with self.lock:
            if operation == "GET":
                return self.get_data(path)
            elif operation == "SET":
                value = request.get("value")
                watch = request.get("watch", False)
                return self.set_data(path, value, watch)
            elif operation == "DELETE":
                return self.delete_data(path)
            elif operation == "WATCH":
                client_id = request.get("client_id")
                return self.add_watch(path, client_id)
            elif operation == "LIST":
                return self.list_children(path)
            else:
                return {"status": "error", "message": "Operación no soportada"}
    
    def get_data(self, path):
        if path in self.data:
            return {"status": "ok", "value": self.data[path]}
        else:
            return {"status": "error", "message": "Ruta no encontrada"}
    
    def set_data(self, path, value, watch=False):
        old_value = self.data.get(path)
        self.data[path] = value
        
        # Notificar a los observadores
        if path in self.watches and old_value != value:
            self.notify_watches(path, value)
        
        return {"status": "ok"}
    
    def delete_data(self, path):
        if path in self.data:
            del self.data[path]
            
            # Notificar a los observadores
            if path in self.watches:
                self.notify_watches(path, None)
            
            return {"status": "ok"}
        else:
            return {"status": "error", "message": "Ruta no encontrada"}
    
    def add_watch(self, path, client_id):
        self.watches[path].add(client_id)
        return {"status": "ok"}
    
    def list_children(self, path):
        # Listar todas las claves que comienzan con path/
        if not path.endswith('/'):
            path += '/'
        
        children = [k[len(path):].split('/')[0] for k in self.data.keys() 
                   if k.startswith(path) and k != path]
        
        # Eliminar duplicados
        children = list(set(children))
        
        return {"status": "ok", "children": children}
    
    def notify_watches(self, path, value):
        # En una implementación real, esto enviaría notificaciones a los clientes
        print(f"Notificando cambio en {path}: {value} a {self.watches[path]}")

class CoordinationClient:
    def __init__(self, client_id, server_port=5555):
        self.client_id = client_id
        self.server_port = server_port
        
        # Configuración de ZeroMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://localhost:{self.server_port}")
    
    def get(self, path):
        request = {
            "operation": "GET",
            "path": path
        }
        self.socket.send_json(request)
        return self.socket.recv_json()
    
    def set(self, path, value, watch=False):
        request = {
            "operation": "SET",
            "path": path,
            "value": value,
            "watch": watch
        }
        self.socket.send_json(request)
        return self.socket.recv_json()
    
    def delete(self, path):
        request = {
            "operation": "DELETE",
            "path": path
        }
        self.socket.send_json(request)
        return self.socket.recv_json()
    
    def watch(self, path):
        request = {
            "operation": "WATCH",
            "path": path,
            "client_id": self.client_id
        }
        self.socket.send_json(request)
        return self.socket.recv_json()
    
    def list_children(self, path):
        request = {
            "operation": "LIST",
            "path": path
        }
        self.socket.send_json(request)
        return self.socket.recv_json()

def main():
    # Iniciar servicio de coordinación
    service = CoordinationService()
    service.start()
    
    # Esperar a que el servicio esté listo
    time.sleep(1)
    
    # Crear algunos clientes
    clients = [CoordinationClient(f"client-{i}") for i in range(3)]
    
    # Cliente 1 crea algunos datos
    print("Cliente 1 creando datos...")
    clients[0].set("/config", {"max_connections": 100})
    clients[0].set("/status", "running")
    clients[0].set("/locks/resource1", "free")
    
    # Cliente 2 lee datos
    print("\nCliente 2 leyendo datos...")
    print(f"Config: {clients[1].get('/config')}")
    print(f"Status: {clients[1].get('/status')}")
    
    # Cliente 3 observa un recurso y lo adquiere
    print("\nCliente 3 observando y adquiriendo recurso...")
    clients[2].watch("/locks/resource1")
    print(f"Estado inicial del recurso: {clients[2].get('/locks/resource1')}")
    clients[2].set("/locks/resource1", "locked_by_client3")
    
    # Cliente 1 lista los recursos disponibles
    print("\nCliente 1 listando recursos...")
    print(f"Recursos: {clients[0].list_children('/locks')}")
    
    # Mantener el programa en ejecución un momento
    time.sleep(2)
    print("\nTerminando servicio...")
    service.active = False

if __name__ == "__main__":
    main()