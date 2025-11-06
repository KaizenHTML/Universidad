import requests

class ErrorGrafo(Exception):
    """Excepción base para errores relacionados con el grafo y la API."""
    pass

class ErrorConexionAPI(ErrorGrafo):
    """Se lanza cuando falla la conexión con la PokéAPI o la respuesta es errónea."""
    pass

class ErrorPokemonNoEncontrado(ErrorGrafo):
    """Se lanza cuando la Búsqueda Binaria no encuentra el Pokémon objetivo."""
    pass

class Pokegrafo:
    """
    Clase que gestiona la cadena de evolución de un Pokémon como un grafo
    y permite la búsqueda optimizada (Binaria) de nodos.
    """


    # URL
    URL_EVOLUCION_BULBASAUR = "https://pokeapi.co/api/v2/evolution-chain/1/"


    def __init__(self):
        self.grafo = {}
        self.nodos_ordenados = []


    def _consumir_api(self, url: str) -> dict:
       
       # Controlando errores
        try:
            # Haciendo solicitud GET a la API
            print(f"-> Conectando a la API: {url}")

            respuesta = requests.get(url, timeout=10)

            respuesta.raise_for_status()  
            return respuesta.json()
        
        except requests.exceptions.RequestException as e:
            raise ErrorConexionAPI(f"Fallo al consumir la PokéAPI: {e}")
        


    def _construir_grafo_recursivo(self, etapa_evolucion: dict):
      
        nombre_pokemon = etapa_evolucion['species']['name']
        self.grafo[nombre_pokemon] = []

        # Recorriendo evoluciones
        for siguiente_etapa in etapa_evolucion.get('evolves_to', []):

            nombre_siguiente = siguiente_etapa['species']['name']
            self.grafo[nombre_pokemon].append(nombre_siguiente)
            
            # Llamadando recursiva 
            self._construir_grafo_recursivo(siguiente_etapa)



    def inicializar_grafo(self):
       
        try:
            datos_json = self._consumir_api(self.URL_EVOLUCION_BULBASAUR)

            # Limpiando
            self.grafo = {}
            self.nodos_ordenados = []
            
            # Iniciando la construcción recursiva 
            self._construir_grafo_recursivo(datos_json['chain'])
            
            # Tomando - ordenando los nodos para Búsqueda Binaria
            self.nodos_ordenados = sorted(self.grafo.keys())
            print("Grafo de evolución construido y nodos ordenados exitosamente.")
            print(f"Total de Pokémon en el grafo: {len(self.nodos_ordenados)}")
            print(f"Nodos: {self.nodos_ordenados}")

        except ErrorGrafo as e:
            print(f"ERROR: {e}")

        except Exception as e:
            print(f" ERROR INESPERADO al inicializar el grafo: {e}")



    def busqueda_binaria_recursiva(self, objetivo: str, izquierda: int, derecha: int) -> bool:
     
        # Caso base
        if izquierda > derecha:
            return False

        medio = (izquierda + derecha) // 2
        
        if self.nodos_ordenados[medio] == objetivo:
            return True  # Encontrado
        
        elif self.nodos_ordenados[medio] < objetivo:
            return self.busqueda_binaria_recursiva(objetivo, medio + 1, derecha)
        
        else:
            return self.busqueda_binaria_recursiva(objetivo, izquierda, medio - 1)



    def verificar_existencia_pokemon(self, nombre_pokemon: str) -> bool:
       
        if not self.nodos_ordenados:
            print(" El grafo no ha sido inicializado o está vacío.")
            return False
        
        objetivo = nombre_pokemon.lower()
        
        try:
            encontrado = self.busqueda_binaria_recursiva(
                objetivo, 
                0, 
                len(self.nodos_ordenados) - 1
            )
            
            if not encontrado:
                raise ErrorPokemonNoEncontrado(f"El Pokémon '{nombre_pokemon}' no se encontró en la cadena de evolución de Bulbasaur.")
            
            print(f"¡Éxito! El Pokémon '{nombre_pokemon}' está en el grafo.")
            return True
            
        except ErrorPokemonNoEncontrado as e:
            print(f"BÚSQUEDA FALLIDA: {e}")
            return False
        
        except Exception as e:
            print(f"ERROR INESPERADO durante la búsqueda: {e}")
            return False
        


    def mostrar_grafo(self):

        if not self.grafo:
            print("El grafo está vacío. Inicialízalo primero.")
            return
        
        print("\n--- Estructura de la Cadena de Evolución ---")
        
        # Recorriendo cada Pokémon con su evolución 
        for pokemon, evoluciones in self.grafo.items():
            
            nombre_actual = pokemon.capitalize()
            
            # Comprobando si existen evoluciones
            if evoluciones:

                # Arreglando las evoluciones
                nombres_siguientes = [e.capitalize() for e in evoluciones]
                lista_evoluciones = ", ".join(nombres_siguientes)
                
                print(f"  {nombre_actual} evoluciona a: {lista_evoluciones}")

            else:
                print(f"  {nombre_actual}: ¡Fin de la cadena!")
                
        print("------------------------------------------------------")