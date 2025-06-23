import queue # Importamos la librería queue
import time  # Para simular retrasos

# Creamos una cola para meter elementos 
# maxsize=3 significa que solo puede haber 3 elementos en la cola a la vez.
# Esto es útil para controlar el flujo de mensajes para eso hacemos uso de esto
mi_cola = queue.Queue(maxsize=3)

print("--- Demostración de queue ---")

# Poner elementos en la cola
print("\n[Productor] Intentando poner elementos en la cola...")

for i in range(1, 6): # Intentaremos poner 5 elementos
    try:
        print(f"[Productor] Poniendo elemento {i}...")
        # put(item, block=True, timeout=None)
        # block=True (por defecto): si la cola está llena, espera.
        # timeout=1: Si la cola está llena, espera un máximo de 1 segundo.
        # Si el timeout se agota, lanza una excepción queue.Full.
        mi_cola.put(f"Mensaje_{i}", timeout=1)
        print(f"[Productor] Elemento {i} puesto. Tamaño actual de la cola: {mi_cola.qsize()}")
    except queue.Full:
        print(f"[Productor] ¡La cola está llena! No se pudo poner el elemento {i}. Esperando un momento...")
        time.sleep(0.5) # Espera un poco antes de reintentar o rendirse

print(f"\n[Productor] Todos los intentos de poner elementos han terminado. Tamaño final de la cola: {mi_cola.qsize()}")

# Obtener elementos ingresados en la cola anteriormente
print("\n[Consumidor] Intentando obtener elementos de la cola...")

while not mi_cola.empty(): # Mientras la cola no esté vacía
    try:
        # get(block=True, timeout=None)
        # block=True (por defecto): si la cola está vacía, espera.
        # timeout=1: Si la cola está vacía, espera un máximo de 1 segundo.
        # Si el timeout se agota, lanza una excepción queue.Empty.
        item = mi_cola.get(timeout=1)
        print(f"[Consumidor] Obtenido: {item}. Tamaño actual de la cola: {mi_cola.qsize()}")
        # Después de procesar un elemento, es común llamar a task_done()
        mi_cola.task_done() # Sirve para señalizar la finalización del procesamiento de una tarea.
        time.sleep(0.2) # Simula tiempo de procesamiento
    except queue.Empty:
        print("[Consumidor] ¡La cola está vacía! No hay más elementos para obtener.")
        break # Salimos del bucle si la cola está vacía

print("\n[Consumidor] Todos los intentos de obtener elementos han terminado.")

print("--- Fin de la demostración de queue ---")
