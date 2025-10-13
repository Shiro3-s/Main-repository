# lamport_clocks.py
import random
import time
from threading import Thread, Lock

class Process:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.clock = 0
        self.lock = Lock()
        self.message_queue = []
        self.log = []
        self.num_processes = num_processes
    
    def local_event(self):
        with self.lock:
            self.clock += 1
            event = f"Proceso {self.process_id}: Evento local en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
    
    def send_message(self, receiver_id):
        with self.lock:
            self.clock += 1
            message = {
                "sender": self.process_id,
                "clock": self.clock,
                "content": f"Mensaje de {self.process_id} a {receiver_id}"
            }
            event = f"Proceso {self.process_id}: Envío a P{receiver_id} en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
            return message
    
    def receive_message(self, message):
        with self.lock:
            sender_clock = message["clock"]
            self.clock = max(self.clock, sender_clock) + 1
            event = f"Proceso {self.process_id}: Recibido de P{message['sender']} en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
    
    def run(self, processes):
        for _ in range(5):  # Cada proceso ejecuta 5 acciones
            time.sleep(random.uniform(0.1, 0.5))
            action = random.choice(["local", "send"])
            
            if action == "local":
                self.local_event()
            else:
                # Elegir un proceso aleatorio para enviar un mensaje
                receiver_id = random.choice([i for i in range(self.num_processes) if i != self.process_id])
                message = self.send_message(receiver_id)
                processes[receiver_id].message_queue.append(message)
        
        # Procesar mensajes recibidos
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.receive_message(message)

def main():
    num_processes = 3
    processes = [Process(i, num_processes) for i in range(num_processes)]
    
    # Crear hilos para cada proceso
    threads = []
    for i in range(num_processes):
        thread = Thread(target=processes[i].run, args=(processes,))
        threads.append(thread)
        thread.start()
    
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
    
    # Mostrar el log de eventos ordenados por tiempo lógico
    print("\nLog de eventos ordenados por tiempo lógico:")
    all_events = []
    for p in processes:
        all_events.extend(p.log)
    
    for clock, event in sorted(all_events):
        print(f"[Tiempo {clock}] {event}")

if __name__ == "__main__":
    main()