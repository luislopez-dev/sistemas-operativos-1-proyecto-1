import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from GestorProcesos import GestorProcesos

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Simulador de Procesos")
        self.root.geometry("700x700")
        self.gestor = GestorProcesos()

        # Estilo general
        self.style = ttk.Style("darkly")

        # UI Principal
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        # Entradas de datos
        ttk.Label(self.frame, text="Nombre del Proceso:").grid(row=0, column=0, sticky=W, pady=5)
        self.nombre_entry = ttk.Entry(self.frame, width=30)
        self.nombre_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame, text="Memoria (MB):").grid(row=1, column=0, sticky=W, pady=5)
        self.memoria_entry = ttk.Entry(self.frame, width=30)
        self.memoria_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Duración (s):").grid(row=2, column=0, sticky=W, pady=5)
        self.duracion_entry = ttk.Entry(self.frame, width=30)
        self.duracion_entry.grid(row=2, column=1, pady=5)

        # Botón de crear proceso
        self.boton_crear = ttk.Button(self.frame, text="➕ Crear proceso", bootstyle=SUCCESS, command=self.crear_proceso)
        self.boton_crear.grid(row=3, columnspan=2, pady=15)

        # Separador visual
        ttk.Separator(self.frame, orient=HORIZONTAL).grid(row=4, columnspan=2, sticky="ew", pady=10)

        # Área de estado de memoria
        self.estado_text = ttk.Text(self.frame, height=15, width=60, wrap="none", state="disabled")
        self.estado_text.grid(row=5, columnspan=2, pady=10)

        # Iniciar actualización periódica
        self.actualizar_estado()

    def crear_proceso(self):
        try:
            nombre = self.nombre_entry.get()
            memoria = int(self.memoria_entry.get())
            duracion = int(self.duracion_entry.get())

            # Ejecutar en un hilo aparte
            threading.Thread(target=self.gestor.crear_proceso, args=(nombre, memoria, duracion), daemon=True).start()

            # Limpiar entradas
            self.nombre_entry.delete(0, "end")
            self.memoria_entry.delete(0, "end")
            self.duracion_entry.delete(0, "end")

        except ValueError:
            self.mostrar_mensaje("⚠️ Entrada inválida. Asegúrate de usar números válidos.")

    def mostrar_mensaje(self, texto):
        self.estado_text.configure(state="normal")
        self.estado_text.insert("end", f"{texto}\n")
        self.estado_text.configure(state="disabled")

    def actualizar_estado(self):
        # Mostrar RAM y procesos activos/en cola
        self.estado_text.configure(state="normal")
        self.estado_text.delete("1.0", "end")

        ram_disp = self.gestor.memoria_total - self.gestor.memoria_usada
        self.estado_text.insert("end", f"💾 RAM disponible: {ram_disp} MB\n\n")

        self.estado_text.insert("end", "⚙️ Procesos activos:\n")
        if self.gestor.procesos_activos:
            for p in self.gestor.procesos_activos:
                self.estado_text.insert("end", f"  🟢 {p.nombre} ({p.pid}) - {p.memoria}MB, {p.duracion}s\n")
        else:
            self.estado_text.insert("end", "  (Ninguno)\n")

        self.estado_text.insert("end", "\n📥 Procesos en cola:\n")
        if not self.gestor.cola_espera.empty():
            for p in list(self.gestor.cola_espera.queue):
                self.estado_text.insert("end", f"  🕓 {p.nombre} ({p.pid}) - {p.memoria}MB, {p.duracion}s\n")
        else:
            self.estado_text.insert("end", "  (Ninguno)\n")

        self.estado_text.configure(state="disabled")

        # Repetir cada segundo
        self.root.after(1000, self.actualizar_estado)

# Iniciar app
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = App(root)
    root.mainloop()
