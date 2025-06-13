import threading # Importamos la librería threading
import time      # Para simular un poco de trabajo

# Definimos una función que será ejecutada por un hilo
def tarea_del_hilo(nombre_hilo, duracion): # Esta funcion recibe dos argumentos tiempo y el nombre del hilo
    print(f"[{nombre_hilo}] Hilo iniciado. Trabajando por {duracion} segundos...") # Printeara el nombre del hijo y la duracion de este
    time.sleep(duracion) # Simula que el hilo está haciendo algo (esperando)
    print(f"[{nombre_hilo}] Hilo finalizado.") # Despues de que haya pasado en tiempo mostraba el nombre del hilo que finalizo

print("--- Demostración de threading ---") # Mostrara titulo de demostracion de threading

# Creamos dos hilos, cada uno ejecutando la función 'tarea_del_hilo'
# Pasamos argumentos a la función a través de 'args'
hilo1 = threading.Thread(target=tarea_del_hilo, args=("HILO-A", 3)) # Asignamos el nombre de HILO-A con una duracion de 3 segundos
hilo2 = threading.Thread(target=tarea_del_hilo, args=("HILO-B", 2)) # Asignamos el nombre de HILO-B con una duracion de 2 segundos
# Termina antes el Hilo-B porque tiene menos tiempo y como procesa en paralelo (al mismo tiempo) termina el que es mas rapido

# Iniciamos la ejecución de los hilos
# Esto hace que la función 'tarea_del_hilo' comience a ejecutarse en paralelo
hilo1.start()
hilo2.start()

print("El programa principal sigue ejecutándose mientras los hilos trabajan...") # Texto indicativo de trabajo de hilos

# Esperamos a que cada hilo termine su ejecución
# Esto asegura que el programa principal no finalice antes de que los hilos hayan completado su tarea
print("Esperando a que HILO-A termine...")
hilo1.join() # El programa principal se bloquea aquí hasta que hilo1 termine
print("HILO-A ha terminado.")

print("Esperando a que HILO-B termine...")
hilo2.join() # El programa principal se bloquea aquí hasta que hilo2 termine
print("HILO-B ha terminado.")

print("--- Todos los hilos han terminado. Programa principal finalizado. ---") # Termino de programa
