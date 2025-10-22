#  Instalando librería
import requests 

class BuscadorPaises:
    
    def __init__(self, url):
        self.url = url
        # Guardando los datos de los países 
        self.countries_data = self._fech_countries()  
        

    # Método para obtener los países 
    def _fech_countries(self):
        
        print('Obteniendo paises...')
        
        # Controlando errores
        try:
            # Haciendo solicitud GET a la API
            response = requests.get(self.url, timeout=10) 

            response.raise_for_status() 
            
            return response.json()  
        
        except requests.RequestException as e:
            print(f'Error al traer los paises: {e}')
            return None
        
    
    # Método lineal para buscar un país 
    def linear_search(self, country_name):
        
        # Parando la función en caso de no haber datos
        if not self.countries_data:
            print('No existen datos de paises disponibles.')
            return None 
        
        # Recorriendo la lista de países
        for country in self.countries_data:
            # Comparando el país de la API con el país ingresado
            if country['name']['common'].lower() == country_name.lower(): 
                return {
                    "name": country['name']['common'],
                    "google_maps_url": country.get('maps', {}).get('googleMaps'),  
                }
        return None
    
    
    
    # Método binario para buscar un país 
    def binary_search(self, country_name):
        
        if not self.countries_data:
            print('No existen datos de paises disponibles.')
            return None 
        
        # Ordenando la lista de países por su nombre
        sorted_countries = sorted(self.countries_data, key=lambda x: x['name']['common'].lower())
        
        low, high = 0, len(sorted_countries) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Obteniendo el nombre del país en la posición media
            current_country = sorted_countries[mid]['name']['common'].lower()
            
            if current_country == country_name.lower():
                return {        
                    "name": sorted_countries[mid]['name']['common'],
                    "google_maps_url": sorted_countries[mid].get('maps', {}).get('googleMaps'),       
                }
            
            elif current_country < country_name.lower():
                low = mid + 1
            else:
                high = mid - 1
                
        return None
    
    
    def main():
        
        # Asignándolo al parámetro del constructor
        api_url = 'https://restcountries.com/v3.1/region/europe'
        
        # Creando una instancia
        searcher = BuscadorPaises(api_url)
        
        if not searcher.countries_data:
            print('No se pueden realizar búsquedas sin datos de países.')
            return
        
        while True:
            print("\n ----  Menú de Búsqueda de Países  ----")
            print("1. Búsqueda Lineal")
            print("2. Búsqueda Binaria")
            print("3. Salir")
            
            choice = input("Seleccione una opción (1-3): ")
            
            if choice == '3':
                print("Saliendo del programa...")
                break
            
            if choice in ['1', '2']:
                country_name = input("Ingrese el nombre del país a buscar: ")
                
                if choice == '1':
                    
                    print("\nRealizando búsqueda Lineal...")
                    result = searcher.linear_search(country_name)
                    
                elif choice == '2':
                    print("\nRealizando búsqueda Binaria...")
                    result = searcher.binary_search(country_name)
                    
                    
                if result:
                    print("\n--- Resultado de la Búsqueda ---")
                    print(f"País encontrado: {result['name']}")
                    print(f"Mapa de Google: {result['google_maps_url']}")
                else:
                    print("\n--- País no encontrado ---")
                    
            else: 
                print("Opción inválida. Por favor, seleccione una opción válida.")
                
                
if __name__ == "__main__":
    BuscadorPaises.main()