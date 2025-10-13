# -*- coding: utf-8 -*-
import time
import random
import threading
import os

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.clock = 0
        self.log = []
        self.lock = threading.Lock()
       
    def local_event(self):
        with self.lock:
            self.clock += 1
            event = f"Proceso {self.process_id}: Evento local en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
       
    def send_message(self, receiver):
        with self.lock:
            self.clock += 1
            message = {"sender": self.process_id, "clock": self.clock}
            event = f"Proceso {self.process_id}: Env�o a P{receiver.process_id} en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
           
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.5))
        receiver.receive_message(message)
       
    def receive_message(self, message):
        with self.lock:
            sender_clock = message["clock"]
            self.clock = max(self.clock, sender_clock) + 1
            event = f"Proceso {self.process_id}: Recibido de P{message['sender']} en tiempo {self.clock}"
            self.log.append((self.clock, event))
            print(event)
       
    def print_log(self):
        print(f"\nRegistro de eventos del Proceso {self.process_id}:")
        for clock, event in sorted(self.log, key=lambda x: x[0]):
            print(f"   {event}")

def process_activity(process, other_processes, num_events=5):
    for _ in range(num_events):
        # Simular actividad aleatoria
        time.sleep(random.uniform(0.2, 1.0))
           
        # Decidir aleatoriamente entre evento local o env�o de mensaje
        if random.random() < 0.3 or not other_processes:  # 30% probabilidad de evento local
            process.local_event()
        else:
            # Seleccionar un proceso aleatorio para enviar mensaje
            receiver = random.choice(other_processes)
            process.send_message(receiver)
   
def main():
    # Crear procesos
    num_processes = 3
    processes = [Process(i) for i in range(num_processes)]
       
    # Crear hilos para cada proceso
    threads = []
    for i, process in enumerate(processes):
        other_procs = processes[:i] + processes[i+1:]
        thread = threading.Thread(target=process_activity, args=(process, other_procs))
        threads.append(thread)
       
    # Iniciar todos los hilos
    print("Iniciando simulaci�n de relojes l�gicos de Lamport...")
    for thread in threads:
        thread.start()
       
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
       
    # Imprimir logs
    print("\n" + "="*50)
    print("RESULTADOS DE LA SIMULACI�N")
    print("="*50)
    for process in processes:
        process.print_log()
   
if __name__ == "__main__":
    main()
