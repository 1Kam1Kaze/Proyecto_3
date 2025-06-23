import random # Importamos la librería random

print("--- Demostración de random ---")

# Generar un entero aleatorio entre 1 y 10 (inclusive)
num_entero = random.randint(1, 10)
print(f"Número entero aleatorio entre 1 y 10: {num_entero}")

# Generar un número flotante aleatorio entre 0.0 (inclusive) y 1.0 (exclusivo)
num_flotante_0_1 = random.random()
print(f"Número flotante aleatorio entre 0.0 y 1.0: {num_flotante_0_1:.4f}")

# Generar un número flotante aleatorio en un rango específico
num_flotante_rango = random.uniform(5.0, 10.0)
print(f"Número flotante aleatorio entre 5.0 y 10.0: {num_flotante_rango:.4f}")

# Seleccionar un elemento aleatorio de una lista
productos = ["Laptop", "Mouse", "Teclado", "Monitor", "Webcam"]
producto_aleatorio = random.choice(productos)
print(f"Producto aleatorio de la lista: {producto_aleatorio}")

# Reordenar aleatoriamente una lista (mezclar)
lista_numeros = [1, 2, 3, 4, 5]
print(f"Lista original: {lista_numeros}")
random.shuffle(lista_numeros) # Mezcla la lista 'in-place' (la modifica directamente)
print(f"Lista mezclada: {lista_numeros}")

print("--- Fin de la demostración de random ---")
