# -*- coding: utf-8 -*-
import time
import random
import threading
import os
from collections import defaultdict

class Process:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.vector_clock = [0] * num_processes
        self.log = []
        self.lock = threading.Lock()
    
    def local_event(self):
        with self.lock:
            self.vector_clock[self.process_id] += 1
            clock_str = self._format_vector_clock()
            event = f"Proceso {self.process_id}: Evento local con vector {clock_str}"
            self.log.append((self.vector_clock.copy(), event))
            print(event)
    
    def send_message(self, receiver):
        with self.lock:
            self.vector_clock[self.process_id] += 1
            clock_str = self._format_vector_clock()
            event = f"Proceso {self.process_id}: Env�o a P{receiver.process_id} con vector {clock_str}"
            self.log.append((self.vector_clock.copy(), event))
            print(event)
            message = {"sender": self.process_id, "vector_clock": self.vector_clock.copy()}
        
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.5))
        receiver.receive_message(message)
    
    def receive_message(self, message):
        with self.lock:
            sender_clock = message["vector_clock"]
            # Actualizar el reloj vectorial (tomar el m�ximo para cada componente)
            for i in range(len(self.vector_clock)):
                self.vector_clock[i] = max(self.vector_clock[i], sender_clock[i])
            # Incrementar el componente propio
            self.vector_clock[self.process_id] += 1
            
            clock_str = self._format_vector_clock()
            event = f"Proceso {self.process_id}: Recibido de P{message['sender']} con vector {clock_str}"
            self.log.append((self.vector_clock.copy(), event))
            print(event)
    
    def _format_vector_clock(self):
        return "[" + ", ".join(map(str, self.vector_clock)) + "]"
    
    def print_log(self):
        print(f"\nRegistro de eventos del Proceso {self.process_id}:")
        for clock, event in self.log:
            clock_str = "[" + ", ".join(map(str, clock)) + "]"
            print(f"  {event}")
    
    def detect_concurrent_events(self, other_process):
        concurrent_events = []
        
        for clock1, event1 in self.log:
            for clock2, event2 in other_process.log:
                if self._is_concurrent(clock1, clock2):
                    concurrent_events.append((event1, event2))
        
        return concurrent_events
    
    def _is_concurrent(self, clock1, clock2):
        """Determina si dos relojes vectoriales representan eventos concurrentes."""
        less_than = False
        greater_than = False
        
        for i in range(len(clock1)):
            if clock1[i] < clock2[i]:
                less_than = True
            elif clock1[i] > clock2[i]:
                greater_than = True
        
        # Son concurrentes si hay componentes mayores en ambas direcciones
        return less_than and greater_than

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
    processes = [Process(i, num_processes) for i in range(num_processes)]
    
    # Crear hilos para cada proceso
    threads = []
    for i, process in enumerate(processes):
        other_procs = processes[:i] + processes[i+1:]
        thread = threading.Thread(target=process_activity, args=(process, other_procs))
        threads.append(thread)
    
    # Iniciar todos los hilos
    print("Iniciando simulaci�n de relojes vectoriales...")
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
    
    # Detectar eventos concurrentes
    print("\n" + "="*50)
    print("EVENTOS CONCURRENTES DETECTADOS")
    print("="*50)
    for i in range(num_processes):
        for j in range(i+1, num_processes):
            concurrent = processes[i].detect_concurrent_events(processes[j])
            if concurrent:
                print(f"\nEventos concurrentes entre P{i} y P{j}:")
                for e1, e2 in concurrent:
                    print(f"  - {e1}")
                    print(f"    {e2}")

if __name__ == "__main__":
    main()
