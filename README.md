# Proyecto #1 del curso Sistemas Operativos 1

# Simulador de Gestión de Procesos en Memoria

Este proyecto simula cómo un sistema operativo gestiona la ejecución de procesos en una memoria RAM limitada. Los procesos que no pueden ejecutarse por falta de memoria son puestos en cola de espera, y se ejecutan cuando hay recursos disponibles. Incluye una interfaz gráfica intuitiva con soporte para **tema oscuro (dark mode)**.

---

## Descripción del Proyecto

El simulador permite:
- Crear procesos con nombre, consumo de RAM (en MB) y duración (en segundos).
- Ejecutar múltiples procesos concurrentemente si hay memoria disponible.
- Encolar procesos que no pueden ser ejecutados inmediatamente.
- Liberar memoria automáticamente cuando los procesos finalizan.
- Visualizar en tiempo real la memoria disponible, los procesos activos y en espera, todo desde una interfaz gráfica.

---

## Tecnologías Implementadas

- **Python 3.13.2**
- **Programación concurrente** (usando `threading`)
- **Interfaz gráfica con** `Tkinter`
- **Tema oscuro moderno** usando `ttkbootstrap`

---

## Lenguaje de Programación

- Python 3.13.2 

---

## Librerías / Frameworks Utilizados

| Librería        | Descripción                                         |
|-----------------|-----------------------------------------------------|
| `threading`     | Permite ejecutar procesos en paralelo (simulación) |
| `tkinter`       | Interfaz gráfica de usuario                        |
| `ttkbootstrap`  | Framework visual para modernizar `Tkinter`         |
| `uuid`          | Generación de identificadores únicos para procesos |
| `queue`         | Manejo de la cola de procesos en espera            |

## Instalación y Ejecución

```bash

1. git clone https://github.com/luislopez-dev/sistemas-operativos-1-proyecto-1

2. cd sistemas-operativos-1-proyecto-1

3. pip install ttkbootstrap

4. python main.py
