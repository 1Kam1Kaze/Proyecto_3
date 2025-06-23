import time # Importamos la librería time
import random # También importamos random para un ejemplo de pausa aleatoria

print("--- Demostración de time.sleep() ---")

print("Inicio de la simulación...")
segundos_a_esperar = 3
print(f"Esperando {segundos_a_esperar} segundos...")

# time.sleep(segundos)
# Pausa la ejecución del hilo actual por el número de segundos especificado.
# En este caso, el programa se detendrá aquí por 3 segundos.
time.sleep(segundos_a_esperar)

print("¡Despertando! Han pasado 3 segundos.")

print("\nSimulando una pequeña pausa aleatoria...")
# Generamos un número flotante aleatorio entre 0.5 y 2.0
pausa_aleatoria = random.uniform(0.5, 2.0)
print(f"Pausando por {pausa_aleatoria:.2f} segundos...") # .2f para mostrar 2 decimales
time.sleep(pausa_aleatoria) # Pausa por el tiempo aleatorio
print("Pausa aleatoria terminada.")

print("--- Fin de la demostración de time ---")
