# -*- coding: utf-8 -*-
import time
import random
import threading
import os

class Process:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.is_active = True
        self.is_leader = False
        self.current_leader = None
        self.lock = threading.Lock()
        self.election_in_progress = False
        self.responses_received = 0
        self.log = []
    
    def log_event(self, event):
        timestamp = time.time()
        self.log.append((timestamp, event))
        print(f"[{time.strftime('%H:%M:%S')}] {event}")
    
    def start_election(self):
        with self.lock:
            if self.election_in_progress:
                return
            
            self.election_in_progress = True
            self.responses_received = 0
            self.log_event(f"Proceso {self.process_id}: Inicia elecci�n")
        
        # Enviar mensaje de elecci�n a todos los procesos con ID mayor
        higher_processes = [p for p in range(self.process_id + 1, self.num_processes) if processes[p].is_active]
        
        if not higher_processes:
            # No hay procesos con ID mayor, este proceso se convierte en l�der
            self.become_leader()
        else:
            # Enviar mensaje de elecci�n a procesos con ID mayor
            for p_id in higher_processes:
                self.log_event(f"Proceso {self.process_id}: Env�a mensaje de elecci�n a P{p_id}")
                threading.Thread(target=self.send_election_message, args=(p_id,)).start()
            
            # Esperar respuestas
            threading.Thread(target=self.wait_for_responses, args=(higher_processes,)).start()
    
    def send_election_message(self, target_id):
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.3))
        
        # Verificar si el proceso destino est� activo
        if processes[target_id].is_active:
            processes[target_id].receive_election_message(self.process_id)
    
    def receive_election_message(self, sender_id):
        with self.lock:
            self.log_event(f"Proceso {self.process_id}: Recibe mensaje de elecci�n de P{sender_id}")
            
            # Responder al remitente
            threading.Thread(target=self.send_ok_message, args=(sender_id,)).start()
            
            # Iniciar una nueva elecci�n
            if not self.election_in_progress:
                threading.Thread(target=self.start_election).start()
    
    def send_ok_message(self, target_id):
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.3))
        
        # Verificar si el proceso destino est� activo
        if processes[target_id].is_active:
            processes[target_id].receive_ok_message(self.process_id)
    
    def receive_ok_message(self, sender_id):
        with self.lock:
            self.responses_received += 1
            self.log_event(f"Proceso {self.process_id}: Recibe OK de P{sender_id}")
    
    def wait_for_responses(self, higher_processes):
        # Esperar un tiempo para recibir respuestas
        time.sleep(1.0)
        
        with self.lock:
            if self.responses_received > 0:
                # Recibi� al menos una respuesta, no se convierte en l�der
                self.log_event(f"Proceso {self.process_id}: Recibi� {self.responses_received} respuestas, espera mensaje de coordinador")
                self.election_in_progress = False
            else:
                # No recibi� respuestas, se convierte en l�der
                self.become_leader()
    
    def become_leader(self):
        with self.lock:
            self.is_leader = True
            self.current_leader = self.process_id
            self.election_in_progress = False
            self.log_event(f"Proceso {self.process_id}: Se convierte en L�DER")
        
        # Anunciar victoria a todos los dem�s procesos
        for p_id in range(self.num_processes):
            if p_id != self.process_id and processes[p_id].is_active:
                threading.Thread(target=self.send_coordinator_message, args=(p_id,)).start()
    
    def send_coordinator_message(self, target_id):
        # Simular latencia de red
        time.sleep(random.uniform(0.1, 0.3))
        
        # Verificar si el proceso destino est� activo
        if processes[target_id].is_active:
            processes[target_id].receive_coordinator_message(self.process_id)
    
    def receive_coordinator_message(self, leader_id):
        with self.lock:
            self.current_leader = leader_id
            self.is_leader = False
            self.election_in_progress = False
            self.log_event(f"Proceso {self.process_id}: Reconoce a P{leader_id} como L�DER")
    
    def fail(self):
        with self.lock:
            self.is_active = False
            was_leader = self.is_leader
            self.is_leader = False
            self.log_event(f"Proceso {self.process_id}: FALLA" + (" (era L�DER)" if was_leader else ""))
        return was_leader
    
    def recover(self):
        with self.lock:
            self.is_active = True
            self.is_leader = False
            self.current_leader = None
            self.log_event(f"Proceso {self.process_id}: RECUPERADO")
        
        # Iniciar elecci�n al recuperarse
        threading.Thread(target=self.start_election).start()
    
    def print_status(self):
        status = "L�DER" if self.is_leader else f"Sigue a P{self.current_leader}" if self.current_leader is not None else "Sin l�der"
        state = "Activo" if self.is_active else "Inactivo"
        return f"Proceso {self.process_id}: {state}, {status}"

def simulate_process_failures(processes):
    # Esperar a que se establezca un l�der inicial
    time.sleep(3)
    
    # Simular fallos aleatorios
    for _ in range(3):
        time.sleep(random.uniform(1, 3))
        
        # Seleccionar un proceso aleatorio para fallar
        active_processes = [p for p in range(len(processes)) if processes[p].is_active]
        if active_processes:
            fail_id = random.choice(active_processes)
            was_leader = processes[fail_id].fail()
            
            # Si el l�der fall�, iniciar una nueva elecci�n desde otro proceso
            if was_leader:
                time.sleep(1)  # Esperar un poco para simular detecci�n de fallo
                active_processes = [p for p in range(len(processes)) if processes[p].is_active]
                if active_processes:
                    initiator = random.choice(active_processes)
                    print(f"\n[SISTEMA] Detectado fallo del l�der. P{initiator} inicia nueva elecci�n.")
                    processes[initiator].start_election()
        
        # Recuperar un proceso inactivo aleatorio
        time.sleep(random.uniform(1, 3))
        inactive_processes = [p for p in range(len(processes)) if not processes[p].is_active]
        if inactive_processes:
            recover_id = random.choice(inactive_processes)
            processes[recover_id].recover()

def print_final_status(processes):
    print("\n" + "="*50)
    print("ESTADO FINAL DEL SISTEMA")
    print("="*50)
    for process in processes:
        print(process.print_status())

# Variable global para almacenar los procesos
processes = []

def main():
    global processes
    
    # Crear procesos
    num_processes = 5
    processes = [Process(i, num_processes) for i in range(num_processes)]
    
    # Iniciar elecci�n desde el proceso 0
    print("Iniciando simulaci�n del algoritmo Bully...")
    threading.Thread(target=processes[0].start_election).start()
    
    # Simular fallos y recuperaciones
    threading.Thread(target=simulate_process_failures, args=(processes,)).start()
    
    # Ejecutar la simulaci�n por un tiempo
    time.sleep(15)
    
    # Imprimir estado final
    print_final_status(processes)

if __name__ == "__main__":
    main()
