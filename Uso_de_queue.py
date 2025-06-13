import queue # Importamos la librería queue
import time  # Para simular retrasos

# Creamos una cola
# maxsize=3 significa que solo puede haber 3 elementos en la cola a la vez.
# Esto es útil para controlar el flujo de mensajes.
mi_cola = queue.Queue(maxsize=3)

print("--- Demostración de queue ---")

# --- Parte 1: Poniendo elementos en la cola (Productor) ---
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

# --- Parte 2: Obteniendo elementos de la cola (Consumidor) ---
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
        # si estás usando el método .join() de la cola para esperar.
        mi_cola.task_done()
        time.sleep(0.2) # Simula tiempo de procesamiento
    except queue.Empty:
        print("[Consumidor] ¡La cola está vacía! No hay más elementos para obtener.")
        break # Salimos del bucle si la cola está vacía

print("\n[Consumidor] Todos los intentos de obtener elementos han terminado.")

# Puedes usar mi_cola.join() aquí si hubieras puesto task_done() por cada get.
# mi_cola.join() # Bloquea hasta que todos los elementos put() hayan tenido su task_done()

print("--- Fin de la demostración de queue ---")
