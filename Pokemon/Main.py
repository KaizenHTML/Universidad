# Importaciones
from GrafoPokemon import Pokegrafo

from Menu import opcion_valida, opcion_elegida


def Menu():
    print("--------------------------------------")
    print("     Evoluciones Pokemon     ")
    print("--------------------------------------")
    print(" Cadena de Evolución de Bulbasaur ")
    print("--------------------------------------")
    print("[1] Cargar Cadena de Evolución de Bulbasaur")
    print("[2] Ver las Evoluciones")
    print("[3] Buscar Pokémon en la Cadena")
    print("[4] Salir")
    print("--------------------------------------")
   

def Main():
    
    # Inicializando clase principal
    pokegrafo_usuario = Pokegrafo() 
    opcion = None
    
    # Bucle del menú
    while opcion != 4:
        Menu()
        opcion = opcion_valida((1, 4))
        
        if opcion != 4:
            opcion_elegida(opcion, pokegrafo_usuario)


if __name__ == "__main__":
    Main()