import threading  # Para manejo de hilos (simulación de ejecución concurrente de procesos)
import time       # Para simular duración de procesos con sleep
import uuid       # Para generar identificadores únicos (PID)
from queue import Queue  # Para la cola de procesos en espera
from Proceso import Proceso

class GestorProcesos:
    def __init__(self, memoria_total=1024):
        self.memoria_total = memoria_total   # RAM total disponible (1 GB = 1024 MB)
        self.memoria_usada = 0               # Memoria actualmente utilizada
        self.procesos_activos = []           # Lista de procesos que se están ejecutando
        self.cola_espera = Queue()           # Cola FIFO de procesos que no pudieron ejecutarse
        self.lock = threading.Lock()         # Para sincronización entre hilos

    # Crear un nuevo proceso y lo intenta ejecutar
    def crear_proceso(self, nombre, memoria, duracion):
        pid = str(uuid.uuid4())[:8]  # Genera un PID único y corto (8 caracteres)
        proceso = Proceso(pid, nombre, memoria, duracion)
        self._intentar_ejecutar(proceso)  # Intenta ejecutarlo inmediatamente

    # Verificar si hay suficiente memoria para ejecutar el proceso
    def _intentar_ejecutar(self, proceso):
        with self.lock:  # Bloque crítico para evitar condiciones de carrera
            if self.memoria_usada + proceso.memoria <= self.memoria_total:
                # Si hay suficiente memoria, se inicia el proceso
                self.memoria_usada += proceso.memoria
                self.procesos_activos.append(proceso)
                hilo = threading.Thread(target=self._ejecutar_proceso, args=(proceso,))
                hilo.start()
            else:
                # Si no hay memoria, se encola
                self.cola_espera.put(proceso)

    # Simular la ejecución del proceso y su finalización
    def _ejecutar_proceso(self, proceso):
        print(f"Ejecutando {proceso.nombre} ({proceso.pid})...")
        time.sleep(proceso.duracion)  # Simula el tiempo de ejecución real
        with self.lock:
            self.memoria_usada -= proceso.memoria               # Libera la memoria usada
            self.procesos_activos.remove(proceso)               # Elimina de la lista de activos
            print(f"Finalizado {proceso.nombre} ({proceso.pid})")
        self._verificar_cola()  # ejecutar procesos que estaban en espera

    # Revisar la cola de procesos en espera para ver si alguno puede ejecutarse ahora
    def _verificar_cola(self):
        with self.lock:
            procesos_restantes = []  # Procesos que siguen sin poder ejecutarse
            while not self.cola_espera.empty():
                proceso = self.cola_espera.get()
                if self.memoria_usada + proceso.memoria <= self.memoria_total:
                    # Si ahora hay memoria suficiente, se ejecuta
                    self.memoria_usada += proceso.memoria
                    self.procesos_activos.append(proceso)
                    threading.Thread(target=self._ejecutar_proceso, args=(proceso,)).start()
                else:
                    # Si sigue sin haber suficiente memoria, se reencola
                    procesos_restantes.append(proceso)
            for p in procesos_restantes:
                self.cola_espera.put(p)

    # Mostrar en consola el estado actual del sistema (RAM y procesos)
    def estado_memoria(self):
        print(f"Memoria disponible: {self.memoria_total - self.memoria_usada} MB")
        print("Procesos activos:")
        for p in self.procesos_activos:
            print(f"  {p.nombre} ({p.pid}) - {p.memoria}MB")
        print("Procesos en cola:")
        for p in list(self.cola_espera.queue):
            print(f"  {p.nombre} ({p.pid}) - {p.memoria}MB")
