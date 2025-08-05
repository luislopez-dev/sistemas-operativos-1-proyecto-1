class Proceso:
    def __init__(self, pid, nombre, memoria, duracion):
        self.pid = pid              # ID único del proceso
        self.nombre = nombre        # Nombre del proceso
        self.memoria = memoria      # Memoria requerida en MB
        self.duracion = duracion    # Tiempo de ejecución en segundos
