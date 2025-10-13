import time
import random
import threading
import zmq
from datetime import datetime

# --- CONFIGURACIÓN ---
REQUEST_TIMEOUT = 10 # Segundos antes de que una solicitud se considere fallida o bloqueada.

class Process:
    """
    Implementación del Algoritmo de Exclusión Mutua de Ricart-Agrawala.
    Utiliza Relojes de Lamport para la ordenación de eventos y ZeroMQ para la comunicación.
    """
    def __init__(self, process_id, total_processes, base_port=5550):
        self.id = process_id
        self.total_processes = total_processes
        self.base_port = base_port
        self.clock = 0 
        self.active = True
        
        # Estado para exclusión mutua
        self.requesting_resource = False
        self.request_timestamp = 0
        # El número de respuestas requeridas es N-1
        self.required_replies = total_processes - 1
        self.replies_received = set()
        self.deferred_replies = []
        
        # Configuración de ZeroMQ
        self.context = zmq.Context()
        # SOCKET: PULL (Receptor)
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(f"tcp://*:{self.base_port + self.id}")
        
        # SOCKETS: PUSH (Emisores a pares)
        self.senders = {}
        for i in range(total_processes):
            if i != self.id:
                sender = self.context.socket(zmq.PUSH)
                # Conectar a la dirección del PULL receptor del otro proceso
                sender.connect(f"tcp://localhost:{self.base_port + i}")
                self.senders[i] = sender
        
        # Iniciar hilo receptor
        self.receiver_thread = threading.Thread(target=self.receive_messages)
        self.receiver_thread.daemon = True
    
    def start(self):
        """Inicia el proceso y el hilo de recepción de mensajes."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Proceso {self.id} iniciado. Puerto: {self.base_port + self.id}")
        self.receiver_thread.start()
    
    def receive_messages(self):
        """Bucle para recibir y procesar mensajes de otros procesos."""
        while self.active:
            try:
                # Intentar recibir un mensaje sin bloquear (NOBLOCK)
                message = self.receiver.recv_json(flags=zmq.NOBLOCK)
                self.process_message(message)
            except zmq.ZMQError:
                # Si no hay mensajes disponibles, continuar
                pass
            except Exception as e:
                print(f"[{self.id}] Error inesperado en el receptor: {e}")
            time.sleep(0.01) # Pequeño delay para no saturar el CPU
    
    def process_message(self, message):
        """Procesa mensajes REQUEST y REPLY de acuerdo al algoritmo."""
        msg_type = message.get("type")
        sender_id = message.get("sender_id")
        msg_timestamp = message.get("timestamp", 0)
        
        # 1. Actualizar reloj lógico (Regla de Lamport)
        self.clock = max(self.clock, msg_timestamp) + 1
        
        print(f"[{self.id}] Clock: {self.clock}. Recibido {msg_type} de {sender_id} (TS: {msg_timestamp})")
        
        if msg_type == "REQUEST":
            other_timestamp = message.get("request_timestamp")
            
            # Condición de prioridad Ricart-Agrawala:
            # Enviar REPLY inmediatamente si:
            # 1. No estoy solicitando el recurso.
            # 2. O mi solicitud tiene un timestamp mayor (menos prioritario).
            # 3. O los timestamps son iguales, pero mi ID es mayor (regla de desempate).
            
            if (not self.requesting_resource or 
                self.request_timestamp > other_timestamp or
                (self.request_timestamp == other_timestamp and self.id > sender_id)):
                
                # Enviar REPLY inmediatamente
                print(f"[{self.id}] Enviando REPLY inmediato a {sender_id}. Mi TS: {self.request_timestamp}")
                reply_msg = {
                    "type": "REPLY", 
                    "sender_id": self.id,
                    "timestamp": self.clock
                }
                self.send_message(sender_id, reply_msg)
            else:
                # Diferir la respuesta
                print(f"[{self.id}] Difiriendo REPLY para {sender_id}. Mi TS: {self.request_timestamp} (Prioritario)")
                self.deferred_replies.append(sender_id)
        
        elif msg_type == "REPLY":
            self.replies_received.add(sender_id)
            
            # Verificar si ya podemos acceder al recurso (hemos recibido N-1 respuestas)
            if (self.requesting_resource and 
                len(self.replies_received) == self.required_replies):
                
                print(f"[{self.id}] Recibidas todas las respuestas ({self.required_replies}). ¡Acceso a SC concedido!")
                self.requesting_resource = False
    
    def send_message(self, target_id, message):
        """Envía un mensaje a un proceso específico, actualizando el reloj local."""
        self.clock += 1
        message["timestamp"] = self.clock
        
        if target_id in self.senders:
            try:
                self.senders[target_id].send_json(message)
            except Exception as e:
                print(f"[{self.id}] Error al enviar mensaje a {target_id}: {e}")
    
    def broadcast_message(self, message):
        """Envía un mensaje de REQUEST a todos los procesos pares."""
        for target_id in self.senders:
            self.send_message(target_id, message)
    
    def request_resource(self):
        """Pasa al estado de solicitud y emite el mensaje REQUEST."""
        # 1. Actualizar estado y timestamp
        self.requesting_resource = True
        self.request_timestamp = self.clock + 1 # El timestamp del mensaje será clock + 1
        self.replies_received.clear()
        
        # 2. Enviar solicitud a todos los procesos
        request_msg = {
            "type": "REQUEST",
            "sender_id": self.id,
            "request_timestamp": self.request_timestamp,
        }
        print(f"[{self.id}] TS: {self.request_timestamp}. Broadcast REQUEST a N-1 procesos.")
        self.broadcast_message(request_msg)
    
    def release_resource(self):
        """Libera la Sección Crítica y envía las respuestas diferidas."""
        # 1. Actualizar estado
        self.requesting_resource = False
        self.request_timestamp = 0
        
        # 2. Enviar respuestas diferidas
        # Creamos una copia para evitar problemas de concurrencia
        deferred_copy = list(self.deferred_replies)
        self.deferred_replies.clear()
        
        for deferred_id in deferred_copy:
            reply_msg = {
                "type": "REPLY",
                "sender_id": self.id,
            }
            print(f"[{self.id}] Enviando REPLY diferido a {deferred_id}.")
            self.send_message(deferred_id, reply_msg)
    
    def use_resource(self):
        """Bucle principal para solicitar y usar el recurso."""
        print(f"\n--- Proceso {self.id} inicia intento de acceso a SC ---")
        self.request_resource()
        
        # Esperar hasta obtener el recurso (o que expire el timeout)
        start_time = time.time()
        while self.requesting_resource:
            # 2. Implementación de Timeout/Detección de Interbloqueo por tiempo
            if time.time() - start_time > REQUEST_TIMEOUT:
                # Si el tiempo se agota, asumimos fallo de red o nodo caído
                print(f"[{self.id}] ⚠️ ERROR: Solicitud agotó el tiempo de espera ({REQUEST_TIMEOUT}s). Liberando estado y abortando SC.")
                self.requesting_resource = False
                self.release_resource() # Limpiar estado y enviar respuestas diferidas (si las hay)
                return
            time.sleep(0.01) # Espera activa ligera
        
        # --- SECCIÓN CRÍTICA ---
        print(f"[{self.id}] ***************** ACCEDIENDO A SECCIÓN CRÍTICA *****************")
        print(f"[{self.id}] Clock final de entrada: {self.clock}")
        time.sleep(random.uniform(1, 2)) # Simular uso del recurso
        # --- FIN SECCIÓN CRÍTICA ---
        
        print(f"[{self.id}] ***************** LIBERANDO SECCIÓN CRÍTICA *****************")
        self.release_resource()

def main():
    total_processes = 3
    processes = []
    
    # Crear procesos
    for i in range(total_processes):
        processes.append(Process(i, total_processes))
    
    # Iniciar procesos
    for p in processes:
        p.start()
    
    # Esperar un momento para que todos los sockets se inicialicen
    time.sleep(3) 
    
    # Simular solicitudes de recurso
    print("\n================== INICIO SIMULACIÓN ==================")
    threads = []
    for p in processes:
        t = threading.Thread(target=p.use_resource)
        threads.append(t)
        t.start()
        # Escalonar las solicitudes para crear conflictos (condición de carrera)
        time.sleep(random.uniform(0.1, 0.5)) 
        
    for t in threads:
        t.join()
    
    # Simular otra ronda de acceso para ver la re-solicitud
    time.sleep(1)
    print("\n================== SEGUNDA RONDA ==================")
    
    threads = []
    for p in processes:
        t = threading.Thread(target=p.use_resource)
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.1, 0.5)) 
        
    for t in threads:
        t.join()
    
    print("\nTerminando simulación...")
    time.sleep(2)
    for p in processes:
        p.active = False
        
if __name__ == "__main__":
    main()
