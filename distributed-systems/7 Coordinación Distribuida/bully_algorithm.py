# bully_algorithm.py
import time
import random
import threading
import zmq
from datetime import datetime

class Process:
    def __init__(self, process_id, total_processes, base_port=5550):
        self.id = process_id
        self.total_processes = total_processes
        self.base_port = base_port
        self.leader_id = None
        self.active = True
        self.election_in_progress = False
        
        # Configuración de ZeroMQ
        self.context = zmq.Context()
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(f"tcp://*:{self.base_port + self.id}")
        
        self.senders = {}
        for i in range(total_processes):
            if i != self.id:
                sender = self.context.socket(zmq.PUSH)
                sender.connect(f"tcp://localhost:{self.base_port + i}")
                self.senders[i] = sender
        
        # Iniciar hilos
        self.receiver_thread = threading.Thread(target=self.receive_messages)
        self.heartbeat_thread = threading.Thread(target=self.send_heartbeats)
        self.election_thread = None
    
    def start(self):
        print(f"Proceso {self.id} iniciado")
        self.receiver_thread.start()
        self.heartbeat_thread.start()
        
        # Si soy el proceso con ID más alto, inicio como líder
        if self.id == self.total_processes - 1:
            self.become_leader()
        else:
            # Esperar un momento para que todos los procesos se inicien
            time.sleep(2)
            self.start_election()
    
    def receive_messages(self):
        while self.active:
            try:
                message = self.receiver.recv_json(flags=zmq.NOBLOCK)
                self.process_message(message)
            except zmq.ZMQError:
                pass
            time.sleep(0.1)
    
    def process_message(self, message):
        msg_type = message.get("type")
        sender_id = message.get("sender_id")
        
        if msg_type == "ELECTION":
            print(f"Proceso {self.id} recibió mensaje de elección de {sender_id}")
            # Responder al remitente que hay un proceso con ID mayor
            self.send_message(sender_id, {"type": "RESPONSE", "sender_id": self.id})
            # Iniciar mi propia elección
            if not self.election_in_progress:
                self.start_election()
        
        elif msg_type == "RESPONSE":
            print(f"Proceso {self.id} recibió respuesta de {sender_id}")
            self.election_in_progress = False
        
        elif msg_type == "COORDINATOR":
            print(f"Proceso {self.id} recibió anuncio de coordinador: {sender_id}")
            self.leader_id = sender_id
            self.election_in_progress = False
        
        elif msg_type == "HEARTBEAT":
            # Solo procesar heartbeats si vienen del líder actual
            if sender_id == self.leader_id:
                print(f"Proceso {self.id} recibió heartbeat del líder {sender_id}")
    
    def send_message(self, target_id, message):
        if target_id in self.senders:
            self.senders[target_id].send_json(message)
    
    def broadcast_message(self, message):
        for target_id in self.senders:
            self.send_message(target_id, message)
    
    def start_election(self):
        print(f"Proceso {self.id} inicia elección")
        self.election_in_progress = True
        self.leader_id = None
        
        # Enviar mensaje de elección a todos los procesos con ID mayor
        higher_processes_exist = False
        for i in range(self.id + 1, self.total_processes):
            if i in self.senders:
                higher_processes_exist = True
                self.send_message(i, {"type": "ELECTION", "sender_id": self.id})
        
        # Si no hay procesos con ID mayor, me convierto en líder
        if not higher_processes_exist:
            self.become_leader()
        else:
            # Esperar respuestas por un tiempo
            def wait_for_responses():
                time.sleep(2)  # Esperar 2 segundos por respuestas
                if self.election_in_progress:
                    # Si aún estamos en elección, no recibimos respuestas de procesos mayores
                    self.become_leader()
            
            self.election_thread = threading.Thread(target=wait_for_responses)
            self.election_thread.start()
    
    def become_leader(self):
        print(f"Proceso {self.id} se convierte en líder")
        self.leader_id = self.id
        self.election_in_progress = False
        
        # Anunciar a todos los procesos
        self.broadcast_message({"type": "COORDINATOR", "sender_id": self.id})
    
    def send_heartbeats(self):
        while self.active:
            if self.leader_id == self.id:  # Si soy el líder
                print(f"Líder {self.id} enviando heartbeat")
                self.broadcast_message({"type": "HEARTBEAT", "sender_id": self.id})
            time.sleep(1)
    
    def simulate_failure(self):
        print(f"Proceso {self.id} simulando fallo")
        self.active = False
        time.sleep(5)  # Simular fallo por 5 segundos
        self.active = True
        print(f"Proceso {self.id} recuperado")
        # Reiniciar hilos
        if not self.receiver_thread.is_alive():
            self.receiver_thread = threading.Thread(target=self.receive_messages)
            self.receiver_thread.start()
        if not self.heartbeat_thread.is_alive():
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeats)
            self.heartbeat_thread.start()

def main():
    total_processes = 4
    processes = []
    
    # Crear procesos
    for i in range(total_processes):
        processes.append(Process(i, total_processes))
    
    # Iniciar procesos
    for p in processes:
        p.start()
    
    # Esperar un tiempo para que se establezca el líder
    time.sleep(5)
    
    # Simular fallo del líder después de un tiempo
    time.sleep(10)
    leader_index = total_processes - 1  # El proceso con ID más alto
    print(f"\nSimulando fallo del líder (Proceso {leader_index})...")
    processes[leader_index].simulate_failure()
    
    # Mantener el programa en ejecución
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminando procesos...")
        for p in processes:
            p.active = False

if __name__ == "__main__":
    main()