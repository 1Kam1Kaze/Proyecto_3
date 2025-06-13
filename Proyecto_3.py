# ¿Qué significa esto para tu tarea en Python?

# Necesitarás implementar un sistema donde diferentes partes de tu programa (hilos o procesos)
# se comuniquen usando el concepto de "mensajes" en lugar de acceder directamente a la misma memoria.

# Python tiene módulos que te permiten implementar esto:

# Módulo threading (para hilos): Puedes crear múltiples hilos dentro de un mismo proceso.

# Módulo multiprocessing (para procesos): Puedes crear procesos separados. Para la comunicación
# entre procesos, multiprocessing ofrece herramientas como Queue (colas), Pipe (tuberías) que implementan el paso de mensajes.

# Colas (Queue): Las colas son perfectas para este tipo de comunicación.

# Funcionan como los "canales" o "buzones" que mencionan los slides.

# Un hilo/proceso puede put() (enviar) un mensaje en la cola.

# Otro hilo/proceso puede get() (recibir) un mensaje de la cola.

# Las colas de Python manejan automáticamente la sincronización bloqueo cuando la cola está vacía o llena,
# dependiendo de la configuración),
# lo que simplifica mucho tu trabajo.

# Tu tarea probablemente implicará:

# Definir dos o más "tareas" (hilos o procesos): Por ejemplo, un hilo Ventas y un hilo Procesamiento como en el ejemplo.

# Establecer un mecanismo de comunicación basado en mensajes: La forma más sencilla y directa en Python es usar una Queue (cola).

# Implementar la lógica de envío (send): Una tarea pondrá mensajes (objetos de Python que representen las órdenes) en la cola.

# Implementar la lógica de recepción (receive): La otra tarea obtendrá mensajes de la cola y los procesará.

# Manejar la sincronización: Afortunadamente, las Queue de Python se encargan de esto por ti (el get() se bloqueará si no hay mensajes, 
# y el put() puede bloquearse si la cola está llena, si le das un tamaño máximo).
