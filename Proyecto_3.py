
# El problema de Lectores y Escritores (Readers-Writers) es un clásico de la concurrencia en sistemas operativos. El objetivo principal es gestionar el acceso concurrente a un recurso compartido (como una base de datos), permitiendo:
# Múltiples lectores simultáneamente (porque no modifican el recurso),
# Pero sólo un escritor a la vez, y nunca junto con lectores.
# Además, se deben evitar dos problemas clave:
# Starvation de escritores: los escritores no deben ser bloqueados indefinidamente por lectores que no paran de llegar.
# Starvation de lectores: si siempre priorizamos escritores, los lectores podrían no tener oportunidad de leer.

# Importar librerias
import threading
import queue
import random
import time

base_datos = [] # Simulacion de base de datos

# Semáforos y variables de sincronización
mutex_lectores = threading.Lock() # Protege la variable lectores, esta lleva la cuenta de cuantos lectores esta leyendo
mutex_escritura = threading.Lock() # Protege la variable escritores, esta lleva la cuenta de cuantos escritores estan escribiendo
lectores_activos = 0 # Empieza con 0 lectores

canal_peticiones = queue.Queue(maxsize=10) # Establece cuando peticiones de lectura o escritura puede permitir el canal


class Lector(threading.Thread): # Establece que cada lector sera un hilo diferente
    def __init__(self, id_lector): # Establece los parametros de inicialización de la clase __init__ y recibe un ID
        super().__init__() # Inicializa correctamente la clase
        self.id = id_lector # Guarda el ID de lector
        self._detener = threading.Event() # Evento para detener el hilo

    def detener(self): # Sirve para detener pq el le indica al hilo que se debe detener
        self._detener.set() # Detiene el hilo

    def run(self): # Es lo primero que corre al llamar al hilo con .start
        global lectores_activos # Declara de manera globar que modificaremos esta variable
        while not self._detener.is_set(): # Mientra que no se pida deter el hilo este continua ejecutando
            try: # Intenta
                tipo, mensaje = canal_peticiones.get(timeout=2) # Intenta obtener algun tipo de dato del canal un tiempo de espera de 2 segundos
                if tipo != "leer": # Si tipo es diferente a leer
                    canal_peticiones.put((tipo, mensaje))  # No lee el mensaje
                    continue # Continua

                # Control de entrada de lectores
                with mutex_lectores: # Mientras este trabajando con lectores
                    global lectores_activos # Lectores estara activo de manera global
                    lectores_activos += 1 # Detectara un lector mas cada vez
                    if lectores_activos == 1: # Mientras haya un lector no se podra escribir
                        mutex_escritura.acquire()

                print(f"[LECTOR {self.id}] Leyendo base de datos: {base_datos}")
                time.sleep(random.uniform(0.1, 0.5)) # Tiempo de intento

                # Salida de lector
                with mutex_lectores:
                    lectores_activos -= 1
                    if lectores_activos == 0: # Si lectores es igual a 0 se pudra escribir
                        mutex_escritura.release()

                canal_peticiones.task_done() # Se finalizan las tareas

            except queue.Empty: # Si esta vacio arroja esto
                print(f"[LECTOR {self.id}] Esperando peticiones...") # Si no hay hilos ejecutandose tira esto


class Escritor(threading.Thread): # Establece que cada Escritor sera un hilo diferente
    def __init__(self, id_escritor):
        super().__init__()
        self.id = id_escritor
        self._detener = threading.Event()

    def detener(self):
        self._detener.set()

    def run(self):
        while not self._detener.is_set():
            try:
                tipo, mensaje = canal_peticiones.get(timeout=2)
                if tipo != "escribir": # Si es tipo que devuelve el canal de peticiones es diferente a tipo devuelve
                    canal_peticiones.put((tipo, mensaje))  # No es mio, lo devuelvo
                    continue # continua

                mutex_escritura.acquire() # Aqui bloquea a los lectores y escritores
                base_datos.append(mensaje) # Aqui se agregan los mensajes a la base de dato
                print(f"[ESCRITOR {self.id}] Escribió en la base de datos: {mensaje}") # Se printea los mensajes
                time.sleep(random.uniform(0.1, 0.5)) # Tiempo
                mutex_escritura.release() # Se cambia a modo escritura

                canal_peticiones.task_done() # Termina las colas 

            except queue.Empty:
                print(f"[ESCRITOR {self.id}] Esperando peticiones...")


class GeneradorPeticiones(threading.Thread):
    def __init__(self):
        super().__init__()
        self._detener = threading.Event()
        self.contador = 1

    def detener(self):
        self._detener.set()

    def run(self):
        while not self._detener.is_set():
            if random.random() < 0.5:
                canal_peticiones.put(("leer", None))
            else:
                mensaje = f"Orden {self.contador}"
                canal_peticiones.put(("escribir", mensaje))
                self.contador += 1
            time.sleep(random.uniform(0.1, 0.7))


# Programa principal donde se ejecutan todas las clases de arriba
if __name__ == "__main__":
    lectores = [Lector(i) for i in range(3)]
    escritores = [Escritor(i) for i in range(2)]
    generador = GeneradorPeticiones()

    for l in lectores:
        l.start()
    for e in escritores:
        e.start()
    generador.start()

    try:
        time.sleep(15)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")

    print("\nDeteniendo hilos...")
    generador.detener()
    for l in lectores:
        l.detener()
    for e in escritores:
        e.detener()

    generador.join()
    for l in lectores:
        l.join()
    for e in escritores:
        e.join()

    print("Programa finalizado.")
