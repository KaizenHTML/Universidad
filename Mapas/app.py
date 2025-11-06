import tkinter as tk
from tkinter import ttk, messagebox
import requests
import folium
from folium import PolyLine
import webbrowser
import threading
import os
from config import API_KEY, MAP_FILE, MAX_DESTINOS 

# Ciudades establecidas
CIUDADES = [
    "Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena",
    "Ibague", "Pereira", "Manizales", "Bucaramanga", "Cucuta"
]


RUTAS_SUGERIDAS = {
    "Ibague": ["Bogota", "Medellin", "Cali", "Pereira"],
    "Bogota": ["Medellin", "Cali", "Ibague", "Villavicencio"],
    "Medellin": ["Bogota", "Cali", "Pereira", "Cartagena"],
    "Cali": ["Bogota", "Medellin", "Pereira"],
    "Barranquilla": ["Cartagena", "Bogota", "Medellin"],
    "Cartagena": ["Barranquilla", "Bogota", "Medellin"],
    "Pereira": ["Medellin", "Cali", "Bogota", "Manizales"],
    "Manizales": ["Pereira", "Medellin", "Bogota"],
    "Bucaramanga": ["Bogota", "Medellin", "Cucuta"],
    "Cucuta": ["Bucaramanga", "Bogota", "Medellin"]
}


# APIs
BASE_URL_DISTANCE = "https://maps.googleapis.com/maps/api/distancematrix/json"
BASE_URL_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json"


# Estilos de la aplicación
BLUE_PRIMARY = "#007BFF"  
WHITE_BACKGROUND = "#FFFFFF" 
LIGHT_GRAY_BG = "#F8F9FA" 
TEXT_COLOR = "#343A40" 


# personalización
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', 
                fieldbackground=WHITE_BACKGROUND, 
                background=WHITE_BACKGROUND, 
                foreground=TEXT_COLOR,
                selectbackground=BLUE_PRIMARY, 
                selectforeground=WHITE_BACKGROUND, 
                padding=5,
                font=("Helvetica", 11))
style.map('TCombobox', 
          fieldbackground=[('readonly', WHITE_BACKGROUND)],
          selectbackground=[('readonly', BLUE_PRIMARY)])


# Funciones
def geocodificar(ciudad):
    # Obteniendo las coordenadas 
    try:
        params = {"address": f"{ciudad}, Colombia", "key": API_KEY}
        r = requests.get(BASE_URL_GEOCODE, params=params).json()

        if r["status"] == "OK":
            loc = r["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except: pass

    return None, None


def calcular_tramo(origen, destino, modo):
    # Calculando la distancia y el tiempo 
    params = {
        "origins": f"{origen}, Colombia",
        "destinations": f"{destino}, Colombia",
        "mode": modo,
        "units": "metric",
        "key": API_KEY
    }

    try:
        r = requests.get(BASE_URL_DISTANCE, params=params, timeout=10).json()

        if r["status"] == "OK" and r["rows"][0]["elements"][0]["status"] == "OK":
            el = r["rows"][0]["elements"][0]
            return {
                "distancia": el["distance"]["text"],
                "tiempo": el["duration"]["text"],
                "segundos": el["duration"]["value"]
            }
        
    except: pass

    return None


def generar_mapa(coords, nombres):
    # Creando un mapa interactivo con la ruta 
    if len(coords) < 2: return False

    # Centrar el mapa en la primera coordenada con un buen zoom inicial
    mapa = folium.Map(location=coords[0], zoom_start=6)

    # Añadir marcadores para cada punto
    for i, (lat, lng) in enumerate(coords):
        if i >= len(nombres): break

        color = "green" if i == 0 else ("red" if i == len(coords)-1 else "blue")
        folium.Marker([lat, lng], popup=f"<b>{nombres[i]}</b>",
                      icon=folium.Icon(color=color, icon="circle", prefix='fa')).add_to(mapa)
        
    # Dibujar la línea de la ruta
    PolyLine(coords, color="blue", weight=5).add_to(mapa)
    # Ajustar el mapa para que muestre todos los puntos
    mapa.fit_bounds(coords)
    mapa.save(MAP_FILE)
    # Abrir el archivo HTML del mapa
    webbrowser.open('file://' + os.path.realpath(MAP_FILE))
    
    return True


def generar_enlace_gmaps(inicio, destinos, modo):
    # Genera el enlace de Google Maps con la ruta y puntos intermedios.
    modo_gmaps = {"driving": "driving", "bicycling": "bicycling", "transit": "transit"}[modo]
    orig = f"{inicio}, Colombia"
    dest = f"{destinos[-1]}, Colombia" if destinos else orig
    # Puntos intermedios (todos menos el destino final)
    waypoints = "|".join([f"{d}, Colombia" for d in destinos[:-1]]) if len(destinos) > 1 else ""
    # El enlace se genera directamente con la estructura de Google Maps
    url = f"https://www.google.com/maps/dir/?api=1&origin={orig}&destination={dest}&travelmode={modo_gmaps}"
    if waypoints: url += f"&waypoints={waypoints}"

    return url

# App 
class RutaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Ruta Inteligente - Colombia")
        # Tamaño de ventana ajustado para el nuevo diseño
        self.root.geometry("650x780") 
        self.root.configure(bg=LIGHT_GRAY_BG)

        # La inicialización del tema Azure se elimina para evitar el error 'azure.tcl'
        
        self.destinos_extra = []
        self.combos_destinos = []
        self.crear_gui()

    def crear_gui(self):
        # Marco principal para contener todos los controles
        main_frame = tk.Frame(self.root, bg=LIGHT_GRAY_BG, padx=25, pady=25)
        main_frame.pack(pady=20, padx=20, fill="both")
        
        # Título principal
        tk.Label(main_frame, text="Planificador de Rutas 🇨🇴", 
                 font=("Helvetica", 18, "bold"), 
                 bg=LIGHT_GRAY_BG, 
                 fg=BLUE_PRIMARY).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Marco para las selecciones de ruta (Inicio, Destino Final, Intermedios)
        ruta_frame = tk.LabelFrame(main_frame, text="📍 Puntos de la Ruta", 
                                   font=("Helvetica", 12, "bold"), 
                                   bg=WHITE_BACKGROUND, 
                                   fg=TEXT_COLOR, 
                                   padx=15, pady=15)
        ruta_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ruta_frame.columnconfigure(1, weight=1) # Permitir que el combo se expanda

        # Controles de Inicio y Destino Final
        
        # Inicio
        tk.Label(ruta_frame, text="Inicio:", 
                 font=("Helvetica", 11), 
                 bg=WHITE_BACKGROUND, 
                 fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 10))
        self.combo_inicio = ttk.Combobox(ruta_frame, values=CIUDADES, state="readonly", width=30)
        self.combo_inicio.grid(row=0, column=1, sticky="ew", pady=10)
        self.combo_inicio.bind('<<ComboboxSelected>>', self.act_destino_final)

        # Destino final
        tk.Label(ruta_frame, text="Destino Final:", 
                 font=("Helvetica", 11), 
                 bg=WHITE_BACKGROUND, 
                 fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 10))
        self.combo_destino = ttk.Combobox(ruta_frame, state="readonly", width=30)
        self.combo_destino.grid(row=1, column=1, sticky="ew", pady=10)

        # Marco dinámico para destinos intermedios
        self.frame_din = tk.Frame(ruta_frame, bg=WHITE_BACKGROUND)
        self.frame_din.grid(row=2, column=0, columnspan=2, pady=(10, 5), sticky="ew")
        self.frame_din.columnconfigure(1, weight=1)

        # Botón de agregar intermedio (más pequeño y estilizado)
        style.configure('Add.TButton', font=('Helvetica', 10, 'bold'), foreground=WHITE_BACKGROUND, background=BLUE_PRIMARY, borderwidth=0)
        tk.Button(ruta_frame, text="+ Agregar parada intermedia", 
                  font=("Helvetica", 10, "bold"), 
                  bg=BLUE_PRIMARY, 
                  fg=WHITE_BACKGROUND, 
                  activebackground="#0056b3",
                  activeforeground=WHITE_BACKGROUND,
                  command=self.agregar_destino,
                  relief=tk.FLAT).grid(row=3, column=0, columnspan=2, pady=(15, 10), sticky="ew")

        # Marco para la selección de modo
        modo_frame = tk.LabelFrame(main_frame, text="🚗 Modo de Viaje", 
                                   font=("Helvetica", 12, "bold"), 
                                   bg=WHITE_BACKGROUND, 
                                   fg=TEXT_COLOR, 
                                   padx=15, pady=10)
        modo_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.modo = tk.StringVar(value="driving")
        modos = [("Coche", "driving"), ("Bicicleta", "bicycling"), ("Transporte público", "transit")]
        
        for i, (t, v) in enumerate(modos):
            # Usar Radiobuttons de tkinter y personalizar color y fuente
            rb = tk.Radiobutton(modo_frame, text=t, 
                                variable=self.modo, 
                                value=v, 
                                bg=WHITE_BACKGROUND, 
                                fg=TEXT_COLOR,
                                selectcolor=WHITE_BACKGROUND, 
                                activebackground=WHITE_BACKGROUND,
                                font=("Helvetica", 11))
            rb.pack(side=tk.LEFT, padx=15, pady=5)


        # Botón de CALCULAR
        tk.Button(main_frame, text="▶️ CALCULAR RUTA", 
                  font=("Arial", 14, "bold"), 
                  bg="#28A745", 
                  fg="white",
                  activebackground="#1e7e34",
                  activeforeground="white",
                  command=self.iniciar_calc,
                  relief=tk.FLAT).grid(row=3, column=0, columnspan=2, pady=(10, 20), sticky="ew", ipady=5)


        # Resultados
        tk.Label(main_frame, text="📝 Resultados del Cálculo", 
                 font=("Helvetica", 12, "bold"), 
                 bg=LIGHT_GRAY_BG, 
                 fg=TEXT_COLOR).grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 5))
                 
        self.txt = tk.Text(main_frame, height=10, 
                           font=("Courier", 10), 
                           bg=WHITE_BACKGROUND, 
                           fg=TEXT_COLOR,
                           relief=tk.FLAT, borderwidth=5)
        self.txt.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")
        
        sb = tk.Scrollbar(main_frame, command=self.txt.yview)
        sb.grid(row=5, column=2, sticky="ns")
        self.txt.config(yscrollcommand=sb.set)

        # Etiqueta de estado en la parte inferior de la ventana principal
        self.status = tk.Label(self.root, text="Listo", 
                               bg=LIGHT_GRAY_BG, 
                               fg=BLUE_PRIMARY, 
                               font=("Helvetica", 10))
        self.status.pack(pady=(0, 10))


    def act_destino_final(self, e=None):
        # Actualiza las opciones del destino final basándose en las rutas sugeridas.
        ini = self.combo_inicio.get()
        if ini in RUTAS_SUGERIDAS:
            self.combo_destino['values'] = RUTAS_SUGERIDAS[ini]


    def agregar_destino(self):
        # Añade una nueva línea de Combobox para un destino intermedio.
        if len(self.destinos_extra) >= MAX_DESTINOS - 1:
            messagebox.showinfo("Límite", f"Máximo {MAX_DESTINOS} puntos (incluyendo inicio y fin).")
            return
        
        idx = len(self.destinos_extra) + 1
        row = len(self.frame_din.winfo_children()) // 3

        # Etiqueta
        lbl = tk.Label(self.frame_din, text=f"Intermedio {idx}:", 
                       bg=WHITE_BACKGROUND, 
                       font=("Helvetica", 11))
        lbl.grid(row=row, column=0, sticky="w", padx=5)

        # Combobox
        combo = ttk.Combobox(self.frame_din, values=CIUDADES, state="readonly", width=30)
        combo.grid(row=row, column=1, pady=7, padx=5, sticky="ew")
        # Actualiza el siguiente Combobox si hay rutas sugeridas
        combo.bind('<<ComboboxSelected>>', lambda e: self.act_siguiente(combo))
        self.combos_destinos.append(combo)

        # Botón de eliminar
        btn = tk.Button(self.frame_din, text="X", 
                        fg=WHITE_BACKGROUND, 
                        bg="red", 
                        activebackground="#cc0000",
                        activeforeground=WHITE_BACKGROUND,
                        width=2, 
                        relief=tk.FLAT,
                        command=lambda: self.eliminar(row, lbl, combo, btn))
        
        btn.grid(row=row, column=2, padx=5, sticky="w")
        self.destinos_extra.append((lbl, combo, btn))


    def act_siguiente(self, combo):
        # Sugiere opciones para el siguiente destino intermedio basado en el actual.
        c = combo.get()
        if c in RUTAS_SUGERIDAS and self.combos_destinos:
            i = self.combos_destinos.index(combo)
            if i + 1 < len(self.combos_destinos):
                self.combos_destinos[i + 1]['values'] = RUTAS_SUGERIDAS[c]


    def eliminar(self, row, lbl, combo, btn):
        # Elimina un destino intermedio y reorganiza la lista.
        lbl.grid_forget(); combo.grid_forget(); btn.grid_forget()
        self.destinos_extra = [d for d in self.destinos_extra if d[1] != combo]
        self.combos_destinos = [c for c in self.combos_destinos if c != combo]
        # Actualizar las etiquetas de los intermedios restantes
        for i, (l, c, b) in enumerate(self.destinos_extra):
            l.config(text=f"Intermedio {i+1}:")
            l.grid(row=i, column=0)
            c.grid(row=i, column=1)
            b.grid(row=i, column=2)


    def iniciar_calc(self):
        # Inicia el cálculo de la ruta en un hilo separado para no bloquear la GUI.
        threading.Thread(target=self.calcular, daemon=True).start()


    def calcular(self):
        # Lógica principal para calcular distancias, tiempos y generar el mapa.
        self.status.config(text="Calculando...")
        self.txt.delete(1.0, tk.END)

        ini = self.combo_inicio.get()
        dest = self.combo_destino.get()
        inter = [c.get() for c in self.combos_destinos if c.get()]

        if not ini or not dest:
            messagebox.showerror("Error", "Inicio y destino final obligatorios.")
            self.status.config(text="Listo"); return

        puntos = [ini] + inter + [dest]
        modo = self.modo.get()

        self.mostrar(f"Ruta: {' → '.join(puntos)}\n")
        self.mostrar(f"Modo: {dict(driving='Coche', bicycling='Bicicleta', transit='Transporte público')[modo]}\n")
        self.mostrar("-" * 60 + "\n")

        total_km = total_seg = 0
        coords = []

        # Recorre los tramos 
        for i in range(len(puntos) - 1):
            o, d = puntos[i], puntos[i+1]
            self.mostrar(f"{o} → {d} ... ")
            res = calcular_tramo(o, d, modo)

            if res:
                self.mostrar(f"{res['distancia']} | {res['tiempo']}\n")
                # Sumar distancias y segundos totales
                try: 
                    # Limpia la cadena de distancia para suma (ej: 100 km -> 100.0)
                    dist_str = res['distancia'].replace(',', '').split()[0]
                    total_km += float(dist_str)
                except ValueError:
                    pass 

                total_seg += res['segundos']
                
                # Obtener coordenadas para el mapa
                l1 = geocodificar(o)

                # Asegurar que no se dupliquen coordenadas
                if i == 0 and l1: # Siempre añadir el origen
                    coords.append(l1)
                
                l2 = geocodificar(d)
                if l2:
                     # Evitar añadir el punto intermedio dos veces 
                    if i == len(puntos) - 2 or l2 != coords[-1]:
                        coords.append(l2)


            else:
                self.mostrar("Falló (No se pudo obtener la ruta o error de API)\n")
                messagebox.showerror("Error de Tramo", f"No se pudo calcular la ruta de {o} a {d} en el modo seleccionado.")
                self.status.config(text="Error"); 
                return


        # Formato de tiempo total (h, min)
        h = total_seg // 3600; m = (total_seg % 3600) // 60
        
        # Resumen de resultados
        self.mostrar("\n" + "="*60 + "\nRESUMEN\n" + "="*60 + "\n")
        # Formato de distancia con punto de mil y coma decimal
        total_km_fmt = f"{total_km:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.mostrar(f"TOTAL: {total_km_fmt} km | {h}h {m}min\n")

        # Generar y abrir el mapa
        nombres_para_mapa = [puntos[0]] + [puntos[i] for i in range(1, len(puntos)-1)] + [puntos[-1]]
        if generar_mapa(coords, nombres_para_mapa):
            self.mostrar(f"\nMapa abierto en el navegador: {MAP_FILE}\n")

        # Generar enlace de Google Maps
        self.mostrar(f"\n🔗 Enlace de Google Maps:\n{generar_enlace_gmaps(ini, inter + [dest], modo)}\n")
        self.status.config(text="Completado")


    def mostrar(self, t):
        # Inserta texto en la ventana de resultados y asegura que el scroll baje.
        self.txt.insert(tk.END, t)
        self.txt.see(tk.END)
        self.root.update_idletasks() # Asegura que la GUI se actualice

if __name__ == '__main__':
    root = tk.Tk()
    app = RutaApp(root)
    root.mainloop()