
# -*- coding: utf-8 -*-
import time
import random
import threading
import os
from collections import defaultdict

class Process:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.clock = 0
        self.state = "RELEASED"  # RELEASED, WANTED, HELD
        self.request_timestamp = 0
        self.reply_pending = set()
        self.deferred_replies = set()
        self.lock = threading.Lock()
        self.resource_access_count = 0
        self.log = []
    
    def log_event(self, event):
        timestamp = time.time()
        self.log.append((timestamp, event))
        print(f"[{time.strftime('%H:%M:%S')}] {event}")
    
    def local_event(self):
        with self.lock:
            self.clock += 1
    
    def request_resource(self):
        with self.lock:
            self.state = "WANTED"
            self.clock += 1
            self.request_timestamp = self.clock
            self.reply_pending = set(range(self.num_processes)) - {self.process_id}
            self.log_event(f"Proceso {self.process_id}: Solicita recurso con timestamp {self.request_timestamp}")
        
        # Enviar solicitudes a todos los dem�s procesos
        for p_id in range(self.num_processes):
            if p_id != self.process_id:
                threading.Thread(target=self.send_request, args=(p_id,)).start()
        
        # Esperar respuestas
        self.wait_for_replies()
    
    def send_request(self, target_id):
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.3))
        
        # Enviar solicitud
        processes[target_id].receive_request(self.process_id, self.request_timestamp)
    
    def receive_request(self, sender_id, timestamp):
        with self.lock:
            # Actualizar reloj l�gico
            self.clock = max(self.clock, timestamp) + 1
            
            if self.state == "HELD" or (self.state == "WANTED" and 
                                        (self.request_timestamp < timestamp or 
                                        (self.request_timestamp == timestamp and self.process_id < sender_id))):
                # Diferir la respuesta
                self.deferred_replies.add(sender_id)
                self.log_event(f"Proceso {self.process_id}: Difiere respuesta a P{sender_id}")
            else:
                # Enviar respuesta inmediatamente
                threading.Thread(target=self.send_reply, args=(sender_id,)).start()
    
    def send_reply(self, target_id):
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.3))
        
        # Enviar respuesta
        processes[target_id].receive_reply(self.process_id)
    
    def receive_reply(self, sender_id):
        with self.lock:
            if sender_id in self.reply_pending:
                self.reply_pending.remove(sender_id)
                self.log_event(f"Proceso {self.process_id}: Recibe respuesta de P{sender_id}, pendientes: {len(self.reply_pending)}")
    
    def wait_for_replies(self):
        while True:
            with self.lock:
                if not self.reply_pending:
                    self.state = "HELD"
                    self.log_event(f"Proceso {self.process_id}: ACCEDE al recurso")
                    break
            time.sleep(0.1)
        
        # Simular uso del recurso
        time.sleep(random.uniform(0.5, 1.5))
        
        # Liberar el recurso
        self.release_resource()
    
    def release_resource(self):
        with self.lock:
            self.state = "RELEASED"
            self.resource_access_count += 1
            self.log_event(f"Proceso {self.process_id}: LIBERA el recurso (accesos totales: {self.resource_access_count})")
            
            # Enviar respuestas diferidas
            deferred = list(self.deferred_replies)
            self.deferred_replies.clear()
        
        # Enviar todas las respuestas diferidas
        for p_id in deferred:
            threading.Thread(target=self.send_reply, args=(p_id,)).start()
    
    def run(self, num_requests=3):
        for _ in range(num_requests):
            # Esperar un tiempo aleatorio antes de solicitar el recurso
            time.sleep(random.uniform(1, 3))
            
            # Solicitar acceso al recurso
            self.request_resource()

# Variable global para almacenar los procesos
processes = []

def print_statistics(processes):
    print("\n" + "="*50)
    print("ESTAD�STICAS DE ACCESO AL RECURSO")
    print("="*50)
    for process in processes:
        print(f"Proceso {process.process_id}: {process.resource_access_count} accesos")

def main():
    global processes
    
    # Crear procesos
    num_processes = 5
    processes = [Process(i, num_processes) for i in range(num_processes)]
    
    # Crear hilos para cada proceso
    threads = []
    for process in processes:
        thread = threading.Thread(target=process.run)
        threads.append(thread)
    
    # Iniciar todos los hilos
    print("Iniciando simulaci�n del algoritmo de exclusi�n mutua de Ricart-Agrawala...")
    for thread in threads:
        thread.start()
    
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
    
    # Imprimir estad�sticas
    print_statistics(processes)

if __name__ == "__main__":
    main()
