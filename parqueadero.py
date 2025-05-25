import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import math

# Verificar e instalar Pillow si es necesario
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont # Ensure ImageFont is imported if used
except ImportError:
    print("Instalando Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageTk, ImageDraw, ImageFont

class ModernParkingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("JK PARKING - Sistema de Gestión de Estacionamiento")
        self.root.geometry("1200x1200")
        self.root.configure(bg="#f5f5f5")

        # Configuración del tamaño del parqueadero
        self.rows = 13 #  patrón de doble fila de parqueo y una salida conectada
        self.cols = 20 # Aumentado para mejor visualización del flujo
        self.cell_size = 40
        self.parking_spots = []
        self.vehicles = {}
        self.hourly_rate = 3000

        # Paleta de colores 
        self.primary_color = "#2c3e50"
        self.secondary_color = "#34495e"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.danger_color = "#e74c3c"
        self.light_color = "#ecf0f1"
        self.dark_color = "#2c3e50"

        # Fuentes 
        self.font_small = ("Segoe UI", 9)
        self.font_medium = ("Segoe UI", 10, "bold")
        self.font_large = ("Segoe UI", 14, "bold")
        self.font_title = ("Segoe UI", 18, "bold")

        # Crear estructura de la interfaz
        self.create_header()
        self.create_main_panel()
        self.create_parking_map() # Llama a la función para crear el mapa lógico
        self.draw_parking_lot()    # Dibuja el mapa en el canvas

        # Precargar imágenes de vehículos
        self.load_vehicle_images()

    def create_header(self):
        """Crea la cabecera de la aplicación, incluyendo el logo y la hora actual."""
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill=tk.X)

        # Logo y título
        logo_frame = tk.Frame(header, bg=self.primary_color)
        logo_frame.pack(side=tk.LEFT, padx=20)

        # Logo simulado
        self.logo_img = self.create_simple_logo()
        logo_label = tk.Label(logo_frame, image=self.logo_img, bg=self.primary_color)
        logo_label.pack(side=tk.LEFT)

        tk.Label(logo_frame, text="JK PARKING", font=self.font_title,
                 fg="white", bg=self.primary_color).pack(side=tk.LEFT, padx=10)

        # Barra de estado
        status_frame = tk.Frame(header, bg=self.primary_color)
        status_frame.pack(side=tk.RIGHT, padx=20)

        self.time_label = tk.Label(status_frame, text="", font=self.font_medium,
                                     fg="white", bg=self.primary_color)
        self.time_label.pack(side=tk.RIGHT)

        # Actualizar hora cada segundo
        self.update_time()

    def create_simple_logo(self):
        """Crea un logo simple para la aplicación usando PIL."""
        img = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dibujar un icono de estacionamiento
        draw.rectangle([10, 5, 40, 45], fill=self.accent_color, outline="white", width=2)

        
        try:
            
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
           
            font = ImageFont.load_default()
            print("Advertencia: 'arial.ttf' no encontrada. Usando la fuente por defecto de Pillow.")

        draw.text((25, 25), "P", fill="white", anchor="mm", font=font) # Usar la fuente cargada o por defecto

        return ImageTk.PhotoImage(img)

    def update_time(self):
        """Actualiza la hora en la barra de estado."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def create_main_panel(self):
        """Crea el panel principal de la aplicación, dividiendo en mapa y controles."""
        main_container = tk.Frame(self.root, bg=self.light_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Frame para el mapa del parqueadero
        self.map_frame = tk.Frame(main_container, bg="white", bd=0,
                                    highlightbackground="#ddd", highlightthickness=1)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas para dibujar el parqueadero
        self.canvas = tk.Canvas(self.map_frame, bg="white",
                                width=self.cols * self.cell_size,
                                height=self.rows * self.cell_size,
                                scrollregion=(0, 0, self.cols * self.cell_size, self.rows * self.cell_size))

        # Barras de desplazamiento para el canvas
        h_scroll = tk.Scrollbar(self.map_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(self.map_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de controles
        self.control_frame = tk.Frame(main_container, bg="white", width=300,
                                        bd=0, highlightbackground="#ddd", highlightthickness=1)
        # Asegurar que el panel de control se expande verticalmente
        self.control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Título del panel de control
        control_header = tk.Frame(self.control_frame, bg=self.primary_color, height=40)
        control_header.pack(fill=tk.X)
        tk.Label(control_header, text="Panel de Control", font=self.font_large,
                 fg="white", bg=self.primary_color).pack(pady=5)

        # Contenedor de controles con scroll
        control_container = tk.Frame(self.control_frame, bg="white")
        control_container.pack(fill=tk.BOTH, expand=True)

        # Canvas y scrollbar para controles
        control_canvas = tk.Canvas(control_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_container, orient="vertical", command=control_canvas.yview)
        scrollable_frame = tk.Frame(control_canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: control_canvas.configure(
                scrollregion=control_canvas.bbox("all")
            )
        )

        control_canvas.create_window((5, 5), window=scrollable_frame, anchor="nw")
        control_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        control_canvas.pack(side="left", fill="both", expand=True)

        # Sección de entrada de vehículo
        input_frame = tk.Frame(scrollable_frame, bg="white", padx=10, pady=15)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Registro de Vehículos", font=self.font_medium,
                 bg="white", fg=self.dark_color).pack(anchor=tk.W)

        # Entrada de placa
        tk.Label(input_frame, text="Placa del vehículo:", font=self.font_small,
                 bg="white", fg=self.dark_color).pack(anchor=tk.W, pady=(10, 0))

        self.plate_entry = ttk.Entry(input_frame, font=self.font_medium)
        self.plate_entry.pack(fill=tk.X, pady=5)

        # Botones de acción
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Ingresar Vehículo",
                 command=self.add_vehicle).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(btn_frame, text="Registrar Salida",
                 command=self.remove_vehicle).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Información de disponibilidad
        stats_frame = tk.Frame(scrollable_frame, bg="white", padx=10, pady=15)
        stats_frame.pack(fill=tk.X)

        tk.Label(stats_frame, text="Estadísticas", font=self.font_medium,
                 bg="white", fg=self.dark_color).pack(anchor=tk.W)

        self.availability_label = tk.Label(stats_frame, text="", font=self.font_small,
                                         bg="white", fg=self.dark_color, justify=tk.LEFT)
        self.availability_label.pack(anchor=tk.W, pady=10)

        # Lista de vehículos
        list_frame = tk.Frame(scrollable_frame, bg="white", padx=10, pady=15)
        list_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(list_frame, text="Vehículos Estacionados", font=self.font_medium,
                 bg="white", fg=self.dark_color).pack(anchor=tk.W)

        self.vehicle_tree = ttk.Treeview(list_frame, columns=("Placa", "Hora", "Espacio"),
                                         show="headings", height=10)

       
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.font_small)
        style.configure("Treeview", font=self.font_small, rowheight=25)

        self.vehicle_tree.heading("Placa", text="Placa")
        self.vehicle_tree.heading("Hora", text="Hora Entrada")
        self.vehicle_tree.heading("Espacio", text="Espacio")
        self.vehicle_tree.column("Placa", width=100, anchor=tk.W)
        self.vehicle_tree.column("Hora", width=120, anchor=tk.W)
        self.vehicle_tree.column("Espacio", width=80, anchor=tk.W)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.vehicle_tree.yview)
        self.vehicle_tree.configure(yscrollcommand=scrollbar.set)

        self.vehicle_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar evento de clic en el canvas
        self.canvas.bind("<Button-1>", self.spot_clicked)

    def load_vehicle_images(self):
        """Crea imágenes simples de vehículos para mostrar en los espacios."""
        self.vehicle_images = {}
        colors = ["#e74c3c", "#3498db", "#9b59b6", "#1abc9c", "#f39c12"]

        for i, color in enumerate(colors):
            # Crear imagen simple de un carro
            img = Image.new('RGBA', (60, 30), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Cuerpo del carro
            draw.rounded_rectangle([5, 10, 55, 25], radius=5, fill=color)
            draw.rounded_rectangle([15, 5, 45, 10], radius=3, fill=color)

            # Ventanas
            draw.rectangle([20, 7, 30, 10], fill="#ecf0f1")
            draw.rectangle([35, 7, 45, 10], fill="#ecf0f1")

            # Ruedas
            draw.ellipse([10, 20, 20, 30], fill="#2c3e50")
            draw.ellipse([40, 20, 50, 30], fill="#2c3e50")

            self.vehicle_images[f"car_{i}"] = ImageTk.PhotoImage(img)

    def create_parking_map(self):
        
        self.map = [[' ' for _ in range(self.cols)] for _ in range(self.rows)] # Iniciar

        
        for i in range(self.rows):
           
            if i % 3 == 1 or i % 3 == 2:
                for j in range(self.cols):
                    self.map[i][j] = 'P'

        
        for i in range(0, self.rows, 3): 
            if i == 0: 
                self.map[i][0] = 'E'
                for j in range(1, self.cols - 1):
                    self.map[i][j] = '→'
                
                if self.cols > 1:
                    self.map[i][self.cols - 1] = '↓'
            elif i == self.rows - 1: 
                for j in range(self.cols - 1): 
                    self.map[i][j] = '→' 
                if self.cols > 0:
                    self.map[i][self.cols - 1] = 'S'
            else: 
                if (i // 3) % 2 != 0: 
                    for j in range(self.cols): 
                        self.map[i][j] = '←'
                    
                    self.map[i][0] = '↓'
                else: 
                    for j in range(self.cols): 
                        self.map[i][j] = '→'
                    
                    if self.cols > 0:
                        self.map[i][self.cols - 1] = '↓'

    
        for i in range(0, self.rows - 1, 3):
            if i + 2 < self.rows: 
                if (i // 3) % 2 == 0 and self.cols > 0: 
                    if self.map[i][self.cols - 1] == '↓': 
                        self.map[i+1][self.cols - 1] = '↓'
                        self.map[i+2][self.cols - 1] = '↓'
                elif (i // 3) % 2 != 0 and self.cols > 0: 
                    if self.map[i][0] == '↓': 
                        self.map[i+1][0] = '↓'
                        self.map[i+2][0] = '↓'

    def draw_parking_lot(self):
        """
        Dibuja el parqueadero en el canvas, interpretando los caracteres del mapa lógico
        para aplicar colores y texto.
        """
        self.canvas.delete("all") # Limpiar el canvas antes de redibujar
        self.parking_spots = []    # Reiniciar la lista de espacios de parqueo

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell_type = self.map[i][j]
                fill_color = "white"
                outline_color = "#ddd"
                text = ""
                text_fill_color = self.dark_color # Color de texto por defecto

                if cell_type == 'E':  # Entrada
                    fill_color = self.success_color
                    text = "ENTRADA"
                    outline_color = self.success_color
                    text_fill_color = "white" # Texto blanco para la entrada
                elif cell_type == 'S':  # Salida
                    fill_color = self.danger_color
                    text = "SALIDA"
                    outline_color = self.danger_color
                    text_fill_color = "white" # Texto blanco para la salida
                elif cell_type in ['→', '←', '↑', '↓']:  # Vías de circulación con flechas
                    fill_color = "grey"
                    text = cell_type
                    outline_color = self.secondary_color
                    text_fill_color = "white" # Texto blanco para las flechas en vías grises
                elif cell_type == 'P':  # Parqueadero libre
                    fill_color = self.light_color
                    text = f"P-{i},{j}" # Mostrar el identificador del espacio
                    outline_color = "#ddd"
                    text_fill_color = self.dark_color
                    self.parking_spots.append((i, j, x1, y1, x2, y2)) # Registrar el espacio de parqueo

                    # Dibujar líneas de demarcación para espacios de parqueo
                    self.canvas.create_rectangle(x1+5, y1+5, x2-5, y2-5,
                                                 fill=fill_color, outline=outline_color, width=2)
                    # Dibujar número de espacio
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                             font=self.font_small, fill=text_fill_color)
                    continue # Continuar al siguiente ciclo para evitar redibujar el rectángulo base
                elif cell_type == 'X':  # Parqueadero ocupado
                    fill_color = "#fde8e8" # Color más claro para espacio ocupado
                    outline_color = "#f5b7b1" # Borde para espacio ocupado
                    text_fill_color = self.dark_color
                    # El texto de la placa se dibuja en draw_vehicles

                # Dibujar la celda base (excepto para 'P' que ya se dibujó)
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=fill_color, outline=outline_color, width=2)

                # Dibujar texto para celdas que no son 'P' o 'X' (vehículo)
                if text:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                             font=self.font_small, fill=text_fill_color)

        # Dibujar vehículos en los espacios ocupados
        self.draw_vehicles()
        self.update_availability()

    def draw_vehicles(self):
        """Dibuja los vehículos en los espacios ocupados y sus placas."""
        for plate, data in self.vehicles.items():
            i, j = data['spot']
            x_center = j * self.cell_size + self.cell_size / 2
            y_center = i * self.cell_size + self.cell_size / 2

            # Seleccionar imagen de vehículo basado en la placa (para consistencia visual)
            vehicle_idx = hash(plate) % len(self.vehicle_images)
            vehicle_img = list(self.vehicle_images.values())[vehicle_idx]

            # Dibujar imagen del vehículo centrada en el espacio
            self.canvas.create_image(x_center, y_center - 5, image=vehicle_img) # Ajuste para dejar espacio para la placa

            # Dibujar placa debajo del vehículo
            self.canvas.create_text(x_center, y_center + 15, text=plate[:7], # Limitar longitud de placa para visualización
                                     font=self.font_small, fill=self.dark_color)

    def update_availability(self):
        """Actualiza la información de disponibilidad y la lista de vehículos."""
        total = 0
        occupied = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] == 'P':
                    total += 1
                elif self.map[i][j] == 'X':
                    occupied += 1

        available = total - occupied
        self.availability_label.config(
            text=f"Espacios totales: {total}\n"
                 f"Ocupados: {occupied}\n"
                 f"Disponibles: {available}\n"
                 f"Tasa de ocupación: {occupied/total:.0%}" if total > 0 else "Tasa de ocupación: 0%"
        )

        # Actualizar lista de vehículos
        self.update_vehicle_list()

    def update_vehicle_list(self):
        """Actualiza la lista de vehículos en el Treeview."""
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)

        for plate, data in self.vehicles.items():
            time = data['entry_time'].strftime("%Y-%m-%d %H:%M:%S")
            spot = f"{data['spot'][0]},{data['spot'][1]}"
            self.vehicle_tree.insert("", tk.END, values=(plate, time, spot))

    def spot_clicked(self, event):
        """Maneja el clic en un espacio del parqueadero en el canvas."""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        for spot_info in self.parking_spots:
            i, j, x1, y1, x2, y2 = spot_info
            if x1 <= x <= x2 and y1 <= y <= y2:
                if self.map[i][j] == 'X':
                    # Espacio ocupado - mostrar información del vehículo
                    for plate, data in self.vehicles.items():
                        if data['spot'] == (i, j):
                            self.show_vehicle_info(plate, data)
                            break
                elif self.map[i][j] == 'P':
                    # Espacio libre
                    messagebox.showinfo("Espacio Libre",
                                         f"Espacio P-{i},{j} está disponible para estacionar.")
                break # Salir del bucle una vez que se encuentra el espacio

    def show_vehicle_info(self, plate, data):
        """Muestra información detallada de un vehículo en una nueva ventana."""
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Información del Vehículo {plate}")
        info_window.geometry("400x350")
        info_window.resizable(False, False)
        info_window.configure(bg="white")

        # Frame principal
        main_frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Mostrar imagen del vehículo
        vehicle_idx = hash(plate) % len(self.vehicle_images)
        vehicle_img = list(self.vehicle_images.values())[vehicle_idx]

        tk.Label(main_frame, image=vehicle_img, bg="white").pack(pady=10)

        # Información del vehículo (Placa y Espacio)
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=5)

        tk.Label(info_frame, text="Placa:", font=self.font_medium,
                 bg="white", fg=self.dark_color, width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(info_frame, text=plate, font=self.font_medium,
                 bg="white", fg=self.primary_color).pack(side=tk.LEFT)

        tk.Label(info_frame, text="Espacio:", font=self.font_medium,
                 bg="white", fg=self.dark_color, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(10,0))
        tk.Label(info_frame, text=f"{data['spot'][0]},{data['spot'][1]}", font=self.font_medium,
                 bg="white", fg=self.primary_color).pack(side=tk.LEFT)

        # Hora de entrada
        entry_frame = tk.Frame(main_frame, bg="white")
        entry_frame.pack(fill=tk.X, pady=5)

        tk.Label(entry_frame, text="Hora de entrada:", font=self.font_medium,
                 bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)
        tk.Label(entry_frame, text=data['entry_time'].strftime('%Y-%m-%d %H:%M:%S'),
                 font=self.font_small, bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)

        # Calcular tiempo estacionado y costo
        time_parked = datetime.datetime.now() - data['entry_time']
        hours = time_parked.total_seconds() / 3600
        cost = self.hourly_rate * math.ceil(hours * 2) / 2  # Redondeo a media hora

        # Tiempo y costo
        time_cost_frame = tk.Frame(main_frame, bg="white")
        time_cost_frame.pack(fill=tk.X, pady=5)

        tk.Label(time_cost_frame, text="Tiempo estacionado:", font=self.font_medium,
                 bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)
        tk.Label(time_cost_frame, text=str(time_parked).split('.')[0],
                 font=self.font_small, bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)

        tk.Label(time_cost_frame, text="Costo acumulado:", font=self.font_medium,
                 bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X, pady=(10,0))
        tk.Label(time_cost_frame, text=f"${cost:,.2f}", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.success_color, anchor=tk.W).pack(fill=tk.X)

        # Asegurarse de que la imagen no sea recolectada por el garbage collector
        info_window.vehicle_img = vehicle_img

    def add_vehicle(self):
        """Registra un nuevo vehículo en el parqueadero."""
        plate = self.plate_entry.get().strip().upper()

        if not plate:
            messagebox.showerror("Error", "Por favor ingrese una placa válida.")
            return

        if plate in self.vehicles:
            messagebox.showerror("Error", f"El vehículo {plate} ya está en el parqueadero.")
            return

        # Buscar espacio libre
        spot = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] == 'P': # Buscar un espacio de parqueo disponible
                    spot = (i, j)
                    break
            if spot:
                break

        if not spot:
            messagebox.showwarning("Parqueadero Lleno", "No hay espacios disponibles en este momento.")
            return

        # Registrar vehículo
        i, j = spot
        self.map[i][j] = 'X' # Marcar el espacio como ocupado
        self.vehicles[plate] = {
            'entry_time': datetime.datetime.now(),
            'spot': spot
        }

        # Actualizar interfaz
        self.draw_parking_lot()
        self.plate_entry.delete(0, tk.END)

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Vehículo Registrado",
                            f"Vehículo {plate} estacionado en espacio P-{i},{j}.")

    def remove_vehicle(self):
        """Registra la salida de un vehículo y calcula el costo."""
        plate = self.plate_entry.get().strip().upper()

        if not plate:
            messagebox.showerror("Error", "Por favor ingrese una placa válida.")
            return

        if plate not in self.vehicles:
            messagebox.showerror("Error", f"El vehículo {plate} no está en el parqueadero.")
            return

        # Obtener datos del vehículo
        data = self.vehicles[plate]
        entry_time = data['entry_time']
        exit_time = datetime.datetime.now()
        parked_time = exit_time - entry_time
        hours = parked_time.total_seconds() / 3600

        # Calcular tarifa (redondeando a medias horas)
        cost = self.hourly_rate * math.ceil(hours * 2) / 2

        # Liberar espacio
        i, j = data['spot']
        self.map[i][j] = 'P' # Marcar el espacio como libre
        del self.vehicles[plate]

        # Actualizar interfaz
        self.draw_parking_lot()
        self.plate_entry.delete(0, tk.END)

        # Mostrar recibo
        receipt = f"RECIBO DE SALIDA\n\n"
        receipt += f"Placa: {plate}\n"
        receipt += f"Espacio: P-{i},{j}\n"
        receipt += f"Entrada: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"Salida: {exit_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"Tiempo: {str(parked_time).split('.')[0]}\n"
        receipt += f"\nTotal a pagar: ${cost:,.2f}"

        messagebox.showinfo("Salida Registrada", receipt)

# Ejecutar la aplicación
if __name__ == "__main__":
    # Importar ImageFont aquí para asegurar que esté disponible cuando se use en create_simple_logo
    # La importación ya se realiza al inicio del script, pero se mantiene el bloque try-except
    # para robustez en caso de problemas con PIL.ImageFont.
    try:
        from PIL import ImageFont
    except ImportError:
        print("Advertencia: No se pudo importar ImageFont. El texto del logo podría no renderizarse correctamente.")
        ImageFont = None

    root = tk.Tk()
    app = ModernParkingSystem(root)
    root.mainloop()
