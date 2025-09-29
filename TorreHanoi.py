#Función recursiva
def Torres_Hanoi(n, Origen, Destino, Auxiliar):
    
    # Moviendo el disco si solo queda uno
    if n == 1:
        print(f'Mover disco {n} de {Origen} a {Destino}')
        return
    
    # 1. Moviendo discos de Origen a Auxiliar
    Torres_Hanoi(n - 1, Origen, Auxiliar, Destino)

    # 2. Moviendo disco más grande de Origen a Destino.
    print(f'Mover disco {n} de {Origen} a {Destino}')

    # 3. Moviendo discos de Auxiliar a Destino, usando Origen como auxiliar.
    Torres_Hanoi(n - 1, Auxiliar, Destino, Origen)


# n
NUM_DISCOS = 3 

Varilla_A = 'A'
Varilla_B = 'B' 
Varilla_C = 'C'


# Menu
print(f"--- Solución para {NUM_DISCOS} discos ({Varilla_A} -> {Varilla_C}) ---")

# Movimiento que inicia el proceso
Torres_Hanoi(NUM_DISCOS, Varilla_A, Varilla_C, Varilla_B)

print("--- Movimiento completado ---")