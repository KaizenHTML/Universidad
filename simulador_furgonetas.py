
import requests


# Creando furgoneta con sus indicaciones
class Furgoneta:
    def __init__(self, id_furgoneta, api_key):
        self.id = id_furgoneta
        self.api_key = api_key
        self.clientes = []
        self.tiempo_total = 0.0
        self.pausas = 0
        
        # URL API
        self.url = "https://maps.googleapis.com/maps/api/distancematrix/json"


    # Asignando direcciones
    def agregar_clientes(self, lista_clientes):
        self.clientes = lista_clientes

    # Calculando el tiempo entre puntos
    def calcular_tiempo_tramo(self, origen, destino):
        params = {
            "origins": origen,
            "destinations": destino,
            "key": self.api_key,
            "mode": "driving"
        }

        # Haciendo solicitud a google MAPS
        try:
            resp = requests.get(self.url, params=params, timeout=10)
            data = resp.json()
            if data["status"] == "OK":
                elem = data["rows"][0]["elements"][0]
                if elem["status"] == "OK":
                    return round(elem["duration"]["value"] / 60, 1)
            return 999
        except:
            return 999

    # Calculando tiempo completo
    def calcular_ruta_completa(self, almacen):
        if not self.clientes:
            self.tiempo_total = 0
            return

        # Inicializando Ruta
        ruta = [almacen] + self.clientes
        tiempo = 0.0

        # Sumando los tiempos de cada parada
        for i in range(len(ruta) - 1):
            t = self.calcular_tiempo_tramo(ruta[i], ruta[i+1])
            tiempo += t
        self.tiempo_total = tiempo