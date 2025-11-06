import tkinter as tk
from tkinter import scrolledtext
import threading
from simulador_furgonetas import Furgoneta

# ULR
API_KEY = 'AIzaSyCWA8EOMmd6Gl-PKN7WhH0h7hwRQFaSwys'

# Punto de inicio
ALMACEN = "Centro de Distribución, Cra 7 ##45-67, Bogotá, Colombia"


# 100 direcciones aleatorias
CLIENTES = [
    "Calle 100 #15-20, Bogotá, Colombia",
    "Av. Boyacá #78-90, Bogotá, Colombia",
    "Cra 14 #93-10, Bogotá, Colombia",
    "Calle 80 #12-34, Bogotá, Colombia",
    "Av. Chile #56-78, Bogotá, Colombia",
    "Cra 13 #59-80, Bogotá, Colombia",
    "Calle 72 #11-45, Bogotá, Colombia",
    "Av. Caracas #45-23, Bogotá, Colombia",
    "Cra 15 #102-34, Bogotá, Colombia",
    "Calle 127 #19-04, Bogotá, Colombia",
    "Av. Suba #145-67, Bogotá, Colombia",
    "Cra 68 #98-76, Bogotá, Colombia",
    "Calle 26 #15-90, Bogotá, Colombia",
    "Av. El Dorado #88-45, Bogotá, Colombia",
    "Cra 30 #40-12, Bogotá, Colombia",
    "Calle 53 #18-77, Bogotá, Colombia",
    "Av. 68 #90-21, Bogotá, Colombia",
    "Cra 50 #26-50, Bogotá, Colombia",
    "Calle 140 #22-33, Bogotá, Colombia",
    "Av. Ciudad de Cali #123-45, Bogotá, Colombia",
    "Cra 72 #100-50, Bogotá, Colombia",
    "Calle 116 #17-88, Bogotá, Colombia",
    "Av. Jiménez #4-30, Bogotá, Colombia",
    "Cra 45 #87-65, Bogotá, Colombia",
    "Calle 63 #20-10, Bogotá, Colombia",
    "Av. Circunvalar #50-22, Bogotá, Colombia",
    "Cra 19 #92-15, Bogotá, Colombia",
    "Calle 153 #9-41, Bogotá, Colombia",
    "Av. Autopista Norte #197-30, Bogotá, Colombia",
    "Cra 53 #134-22, Bogotá, Colombia",
    "Calle 45 #25-66, Bogotá, Colombia",
    "Av. Calle 26 #34-55, Bogotá, Colombia",
    "Cra 24 #70-12, Bogotá, Colombia",
    "Calle 170 #10-90, Bogotá, Colombia",
    "Av. Boyacá #154-30, Bogotá, Colombia",
    "Cra 60 #50-70, Bogotá, Colombia",
    "Calle 94 #13-44, Bogotá, Colombia",
    "Av. Primero de Mayo #20-45, Bogotá, Colombia",
    "Cra 36 #80-20, Bogotá, Colombia",
    "Calle 123 #18-50, Bogotá, Colombia",
    "Av. Ciudad de Quito #45-60, Bogotá, Colombia",
    "Cra 80 #90-100, Bogotá, Colombia",
    "Calle 76 #14-25, Bogotá, Colombia",
    "Av. Las Américas #68-30, Bogotá, Colombia",
    "Cra 26 #63-44, Bogotá, Colombia",
    "Calle 134 #22-18, Bogotá, Colombia",
    "Av. Batallón Palacé #15-90, Bogotá, Colombia",
    "Cra 9 #50-60, Bogotá, Colombia",
    "Calle 57 #19-33, Bogotá, Colombia",
    "Av. El Mochuelo #77-22, Bogotá, Colombia",
    "Cra 70 #100-10, Bogotá, Colombia",
    "Calle 145 #20-30, Bogotá, Colombia",
    "Av. Guayacanes #88-44, Bogotá, Colombia",
    "Cra 40 #60-50, Bogotá, Colombia",
    "Calle 106 #15-25, Bogotá, Colombia",
    "Av. Villavicencio #30-45, Bogotá, Colombia",
    "Cra 22 #88-99, Bogotá, Colombia",
    "Calle 85 #12-34, Bogotá, Colombia",
    "Av. Calle 100 #20-30, Bogotá, Colombia",
    "Cra 16 #90-100, Bogotá, Colombia",
    "Calle 160 #10-20, Bogotá, Colombia",
    "Av. Suba #200-45, Bogotá, Colombia",
    "Cra 55 #70-80, Bogotá, Colombia",
    "Calle 68 #22-33, Bogotá, Colombia",
    "Av. Córdoba #45-60, Bogotá, Colombia",
    "Cra 12 #80-90, Bogotá, Colombia",
    "Calle 180 #5-15, Bogotá, Colombia",
    "Av. Carrera 9 #54-32, Bogotá, Colombia",
    "Cra 48 #100-110, Bogotá, Colombia",
    "Calle 95 #18-22, Bogotá, Colombia",
    "Av. Ciudad de Cartagena #40-55, Bogotá, Colombia",
    "Cra 71 #95-75, Bogotá, Colombia",
    "Calle 120 #25-35, Bogotá, Colombia",
    "Av. La Esperanza #60-70, Bogotá, Colombia",
    "Cra 28 #70-85, Bogotá, Colombia",
    "Calle 138 #16-28, Bogotá, Colombia",
    "Av. Ciudad de Medellín #33-44, Bogotá, Colombia",
    "Cra 62 #88-99, Bogotá, Colombia",
    "Calle 110 #20-25, Bogotá, Colombia",
    "Av. Boyacá #200-10, Bogotá, Colombia",
    "Cra 33 #75-80, Bogotá, Colombia",
    "Calle 150 #12-18, Bogotá, Colombia",
    "Av. Ciudad de Cali #200-30, Bogotá, Colombia",
    "Cra 44 #90-100, Bogotá, Colombia",
    "Calle 92 #14-24, Bogotá, Colombia",
    "Av. Suba #250-60, Bogotá, Colombia",
    "Cra 59 #85-95, Bogotá, Colombia",
    "Calle 78 #16-26, Bogotá, Colombia",
    "Av. El Dorado #150-20, Bogotá, Colombia",
    "Cra 21 #70-80, Bogotá, Colombia",
    "Calle 165 #8-18, Bogotá, Colombia",
    "Av. Autopista Sur #100-45, Bogotá, Colombia",
    "Cra 65 #90-100, Bogotá, Colombia",
    "Calle 102 #19-29, Bogotá, Colombia",
    "Av. Ciudad de Barranquilla #55-65, Bogotá, Colombia",
    "Cra 18 #85-95, Bogotá, Colombia",
    "Calle 130 #21-31, Bogotá, Colombia",
    "Av. Las Vegas #70-80, Bogotá, Colombia",
    "Cra 52 #80-90, Bogotá, Colombia",
    "Calle 88 #23-33, Bogotá, Colombia",
    "Av. Boyacá #250-20, Bogotá, Colombia",
    "Cra 27 #75-85, Bogotá, Colombia",
    "Calle 155 #10-20, Bogotá, Colombia"
]

# Caracteristicas del problema
NUM_FURGONETAS = 5
MINUTOS_MAX = 8 * 60  
PAUSA_REPOSTAJE = 8 * 60  # 

class AppFurgonetas:
    def __init__(self, root):
        self.root = root
        self.root.title("🚛 Simulador de Furgonetas - 100 Entregas con Google Maps")
        self.root.geometry("850x750")

        tk.Label(root, text="Simulación de 100 Entregas con Restricción de 8 Horas", font=("Arial", 14)).pack(pady=10)
        tk.Label(root, text=f"📍 Almacén: {ALMACEN}", fg="blue", wraplength=800).pack(pady=5)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.btn_simular = tk.Button(self.btn_frame, text="Iniciar Simulación", command=self.iniciar, bg="#2196F3", fg="white")
        self.btn_simular.pack(side=tk.LEFT, padx=5)

        self.btn_reiniciar = tk.Button(self.btn_frame, text="🔁 Reiniciar", command=self.reiniciar, state="disabled", bg="#9E9E9E", fg="white")
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)

        self.btn_pausa = None
        self.salida = scrolledtext.ScrolledText(root, height=30, width=100)
        self.salida.pack(pady=10)

        self.furgonetas = []
        self.furgoneta_actual = 0
        self.simulacion_activa = False

    def iniciar(self):
        self.simulacion_activa = True
        self.btn_simular.config(state="disabled")
        self.btn_reiniciar.config(state="disabled")
        self.salida.delete(1.0, tk.END)
        self.salida.insert(tk.END, "📡 Conectando con Google Maps API...\n")
        self.salida.insert(tk.END, "📦 Asignando 100 clientes a 5 furgonetas (20 cada una)...\n\n")
        self.root.update()

        # Creando Furgonetas
        self.furgonetas = []
        for i in range(NUM_FURGONETAS):
            f = Furgoneta(i+1, API_KEY)
            inicio = i * 20
            fin = inicio + 20
            f.agregar_clientes(CLIENTES[inicio:fin])
            self.furgonetas.append(f)

        self.furgoneta_actual = 0
        self.procesar_siguiente_furgoneta()


    def procesar_siguiente_furgoneta(self):
        if not self.simulacion_activa:
            return

        if self.furgoneta_actual >= len(self.furgonetas):
            self.finalizar_simulacion()
            return

        f = self.furgonetas[self.furgoneta_actual]
        self.salida.insert(tk.END, f"\n🚛 === FURGONETA {f.id} ===\n")
        self.salida.insert(tk.END, f"📍 Clientes asignados ({len(f.clientes)}):\n")
        for idx, cli in enumerate(f.clientes, 1):
            self.salida.insert(tk.END, f"  {idx}. {cli}\n")
        
        self.salida.insert(tk.END, f"\n🛣️ Ruta tomada (secuencia de visitas):\n")
        ruta_completa = [ALMACEN] + f.clientes
        for idx, parada in enumerate(ruta_completa):
            if idx == 0:
                self.salida.insert(tk.END, f"  {idx+1}. {parada} (Almacén)\n")
            else:
                self.salida.insert(tk.END, f"  {idx+1}. {parada}\n")
        
        self.salida.insert(tk.END, f"\n⏳ Calculando tiempos con Google Maps...\n")
        self.root.update()

        # Calcular ruta en hilo separado para no bloquear GUI
        threading.Thread(target=self.calcular_y_verificar, args=(f,)).start()


    def calcular_y_verificar(self, furgoneta):
        furgoneta.calcular_ruta_completa(ALMACEN)
        self.root.after(0, self.verificar_furgoneta, furgoneta)


    def verificar_furgoneta(self, f):
        self.salida.insert(tk.END, f"✅ Tiempo total estimado: {f.tiempo_total:.1f} minutos\n")
        
        if f.tiempo_total > MINUTOS_MAX:
            self.salida.insert(tk.END, f"\n⚠️ ⚠️ ¡ALERTA! Furgoneta {f.id} excede las 8 horas (480 min)!\n")
            self.salida.insert(tk.END, "Debe recargar gasolina antes de continuar.\n")
            
            if self.btn_pausa is None:
                self.btn_pausa = tk.Button(
                    self.btn_frame,
                    text="⛽ Recargar Gasolina",
                    command=self.continuar_con_pausa,
                    bg="#FF9800",
                    fg="white"
                )
                self.btn_pausa.pack(side=tk.LEFT, padx=5)
        else:
            self.salida.insert(tk.END, "-"*70 + "\n")
            self.furgoneta_actual += 1
            self.root.after(100, self.procesar_siguiente_furgoneta)


    def continuar_con_pausa(self):
        if self.btn_pausa:
            self.btn_pausa.pack_forget()
            self.btn_pausa = None

        f = self.furgonetas[self.furgoneta_actual]
        f.tiempo_total += PAUSA_REPOSTAJE  # ⬅️ Ahora añade 480 minutos (8 horas)
        f.pausas += 1
        self.salida.insert(tk.END, f"\n⛽ ¡Gasolina recargada! Se añadieron {PAUSA_REPOSTAJE} minutos (8 horas).\n")
        self.salida.insert(tk.END, f"Nuevo tiempo total: {f.tiempo_total:.1f} minutos\n")
        self.salida.insert(tk.END, "-"*70 + "\n")
        
        self.furgoneta_actual += 1
        self.root.after(100, self.procesar_siguiente_furgoneta)


    def finalizar_simulacion(self):
        self.salida.insert(tk.END, "\n" + "="*70 + "\n")
        self.salida.insert(tk.END, "✅ ¡VIAJE COMPLETADO! - 100 Entregas finalizadas\n")
        self.salida.insert(tk.END, "="*70 + "\n")
        for f in self.furgonetas:
            estado = "✅" if f.tiempo_total - f.pausas * PAUSA_REPOSTAJE <= MINUTOS_MAX else "⚠️"
            msg = f"{estado} Furgoneta {f.id}: {f.tiempo_total:.1f} min"
            if f.pausas > 0:
                msg += f" (+{f.pausas} recarga(s) de 8 horas)"
            self.salida.insert(tk.END, msg + "\n")
        self.salida.insert(tk.END, f"\n🎉 ¡Todas las entregas se completaron con éxito!\n")
        
        self.btn_reiniciar.config(state="normal")
        self.simulacion_activa = False


    def reiniciar(self):
        self.salida.delete(1.0, tk.END)
        self.btn_simular.config(state="normal")
        self.btn_reiniciar.config(state="disabled")
        if self.btn_pausa:
            self.btn_pausa.pack_forget()
            self.btn_pausa = None
        self.furgonetas = []
        self.furgoneta_actual = 0
        self.simulacion_activa = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFurgonetas(root)
    root.mainloop()