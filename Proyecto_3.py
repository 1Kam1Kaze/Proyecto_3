# Componentes Clave a Implementar:
#
# El Canal de Mensajes (Cola):
#
# Una instancia de queue.Queue que servirá como el "buzón" o "canal" por donde las órdenes (mensajes) serán pasadas de un hilo a otro.
# Podrías definirle un maxsize para simular un buffer limitado y ver cómo afecta la sincronización (bloqueo) de los hilos.
# El Hilo Productor (HiloVentas):
#
# Una clase que herede de threading.Thread.
# Su método run() contendrá la lógica para:
# Generar "órdenes" (pueden ser diccionarios con id, producto, cantidad). Aquí usarás random para variar los datos de la orden.
# Enviar estas órdenes al canal de mensajes usando cola.put().
# Simular el tiempo que toma generar una nueva orden usando time.sleep().
# Manejar posibles bloqueos o excepciones si el canal está lleno (usando timeout en put() y un bloque try-except queue.Full).
# El Hilo Consumidor (HiloProcesamiento):
#
# Otra clase que herede de threading.Thread.
# Su método run() contendrá la lógica para:
# Recibir órdenes del canal de mensajes usando cola.get().
# Simular el tiempo que toma procesar una orden usando time.sleep().
# Manejar posibles bloqueos o excepciones si el canal está vacío (usando timeout en get() y un bloque try-except queue.Empty).
# Indicar que una orden ha sido procesada llamando a cola.task_done().
# El Programa Principal (Main):
#
# Aquí es donde se instancian el canal de mensajes y los hilos productor y consumidor.
# Se inician los hilos (hilo.start()).
# Se controlará el ciclo de vida de la aplicación, permitiendo que los hilos se ejecuten por un tiempo.
# Se asegurará una detención controlada de los hilos (hilo.stop() y hilo.join()).

# Se importan las librerias que utilizaremos
import threading
import queue
import random
import time

canal_mensajes = queue.Queue(maxsize=5) # Canal de mensajes cuantos mensajes se pueden leer al mismo tiempo si son mmas de 5 se bloquea

class HiloVentas(threading.Thread): # Se crea una clase personalizada con el cual va a realizar ordenes cuando empiece el .start mas abajo
    def __init__(self, canal): # Inicializa el hilo, guarda la cola y crea un interruptor para detenerlo despues
        super().__init__() # Llama a lo de arriba, la clase Thread, para que se inicialice como un hilo
        self.canal = canal # Guarda en canal como un atributo del objeto. Así puede usarlo en run() // aqui tu vas metiendo cosas al canal con run()
        self._detener = threading.Event() # Crea un interruptor interno que se puede prender para indicar que el hilo debe detenerse //  donde esta el detenerse

    def detener(self): # Sirve para avisarle al hilo que debe detenerse
        self._detener.set()

    def run(self): # Aqui se genera una orden se mete a la cola se espera un rato y se repite
        id_orden = 1 # El primer ID
        productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Impresora'] # Productos q se pueden seleccionar
        while not self._detener.is_set(): # Mientras que no se detenga
            orden = { # Esto de aqui se encarga de realizar ordenes aleatorias con la libreria de random
                'ID': id_orden, # ID del producto
                'Producto': random.choice(productos), # Seleccion un producto random
                'Cantidad': random.randint(1, 5) # Candidad aleatoria entre 1 y 5
            }
            try: # Intenta meter las ordenes de arriba
                self.canal.put(orden, timeout=2) # Lo mete a la cola o lo intenta al menos y tiene un tiempo maximo de espera de 2 segundos si no tira el cola llena FULL de abajo
                print(f"[PRODUCTOR] Orden generada: [ID = {orden['ID']}, Producto = {orden['Producto']}, Cantidad = {orden['Cantidad']}]") # Printea el numero de orden
                id_orden += 1 # Suma la cantidad de ordenes segun esta se le vaya dando osea Orden 1, Orden 2...
            except queue.Full: # En caso de que la cola este llena ocurre este except
                print("[PRODUCTOR] Canal lleno. No se pudo enviar la orden.") # Printea esto en caso de FULL
            time.sleep(random.uniform(0.1, 1))  # Simula tiempo de creación para que no vaya soltando las cosas altiro

class HiloProcesamiento(threading.Thread): # Encargado de procesar las ordenes dadas anteriormente en la clase HiloVentas
    def __init__(self, canal):
        super().__init__()
        self.canal = canal
        self._detener = threading.Event()

    def detener(self):
        self._detener.set()

    def run(self):
        while not self._detener.is_set(): # Mientas no este detenido ejecuta
            try:
                orden = self.canal.get(timeout=2)
                print(f"[CONSUMIDOR] Procesando orden: [ID = {orden['ID']}, Producto = {orden['Producto']}, Cantidad = {orden['Cantidad']}]")
                time.sleep(random.uniform(0.1, 1))  # Simula tiempo de procesamiento
                self.canal.task_done() # Termina las tareas que se le vayan dando
                print(f"[CONSUMIDOR] Orden procesada: {orden['ID']}\n")
            except queue.Empty: # Cuando este vacio se termina
                print("[CONSUMIDOR] Canal vacío. Esperando órdenes...")

# Programa principal
if __name__ == "__main__": # Ejecuta
    productor = HiloVentas(canal_mensajes) # Ejecuta la clase HiloVentas segun el queue de al pricipio y la guarda en productor
    consumidor = HiloProcesamiento(canal_mensajes) # Ejecuta la clase HiloProcesamiento segun el queue de al pricipio y la guarda en consumidor

    # Inicializa las dos variables anteriores
    productor.start()
    consumidor.start()

    # Ejecuta esto durante 15 segundos a menos que uno mismo lo detenga Ctrl + c detener ejecución
    try:
        time.sleep(15)  # Ejecutar durante 15 segundos
    except KeyboardInterrupt:
        print("Interrupción del usuario")

    print("\nDeteniendo hilos...") # Se detiene
    productor.detener()
    consumidor.detener()

    # Espera a que terminen de correr.
    productor.join()
    consumidor.join()

    print("Programa finalizado.")
