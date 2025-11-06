# Importando
from GrafoPokemon import Pokegrafo


def opcion_valida(rango_valido: tuple) -> int:
  
    while True:
        try:
            opcion = input(f"\nIngrese su opción ({rango_valido[0]}-{rango_valido[1]}): ")
            opcion_int = int(opcion)

            if rango_valido[0] <= opcion_int <= rango_valido[1]:
                return opcion_int
            else:
                print(f"Opción no válida. Debe ser un número entre {rango_valido[0]} y {rango_valido[1]}.")
                
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")


def opcion_elegida(opcion: int, pokegrafo: Pokegrafo):
    
    if opcion == 1:
        print("\n--- Cargando Cadena de Evolución de Bulbasaur ---")
        pokegrafo.inicializar_grafo()
        
    elif opcion == 2:
        print("\n--- Viendo las Evoluciones ---")
        pokegrafo.mostrar_grafo()
        
    elif opcion == 3:
        print("\n--- Buscando Pokémon en la Cadena ---")
        if not pokegrafo.nodos_ordenados:
            print("Antes de buscar, selecciona la Opción 1 para cargar la cadena de evolución.")
            return
            
        nombre = input("Ingrese el nombre del Pokémon a buscar: ")
        if not nombre.strip():
            print("El nombre del Pokémon no puede estar vacío.")
            return

        pokegrafo.verificar_existencia_pokemon(nombre.strip())
        
    elif opcion == 4:
        print("\n¡Hasta pronto!")