import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import math
import hashlib

# Verificar e instalar Pillow si es necesario
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
except ImportError:
    print("Instalando Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageTk, ImageDraw, ImageFont

class ModernParkingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("JK PARKING - Sistema de Gestión de Estacionamiento")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")

        # Configuración del tamaño del parqueadero
        self.rows = 15
        self.cols = 22
        self.cell_size = 40
        self.parking_spots = []
        self.vehicles = {}
        self.hourly_rate_car = 3000  # Tarifa para carros
        self.hourly_rate_motorcycle = 1500  # Tarifa para motos

        # Paleta de colores
        self.primary_color = "#2c3e50"
        self.secondary_color = "#34495e"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.light_color = "#ecf0f1"
        self.dark_color = "#2c3e50"
        self.road_color = "#7f8c8d"
        self.marking_color = "#f1c40f"
        self.parking_color = "#bdc3c7"

        # Fuentes
        self.font_small = ("Segoe UI", 9)
        self.font_medium = ("Segoe UI", 10, "bold")
        self.font_large = ("Segoe UI", 14, "bold")
        self.font_title = ("Segoe UI", 18, "bold")

        # Crear estructura de la interfaz
        self.create_header()
        self.create_main_panel()
        self.create_parking_map()
        self.draw_parking_lot()

        # Precargar imágenes de vehículos
        self.load_vehicle_images()

    def create_header(self):
        """Crea la cabecera de la aplicación con logo y hora."""
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

        # Actualizar hora
        self.update_time()

    def create_simple_logo(self):
        """Crea un logo simple para la aplicación."""
        img = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Dibujar un icono de estacionamiento
        draw.rectangle([10, 5, 40, 45], fill=self.accent_color, outline="white", width=2)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        draw.text((25, 25), "P", fill="white", anchor="mm", font=font)
        return ImageTk.PhotoImage(img)

    def update_time(self):
        """Actualiza la hora en la barra de estado."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def create_main_panel(self):
        """Crear el panel principal con mapa y controles."""
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

        # Barras de desplazamiento
        h_scroll = tk.Scrollbar(self.map_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(self.map_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de controles
        self.control_frame = tk.Frame(main_container, bg="white", width=300,
                                    bd=0, highlightbackground="#ddd", highlightthickness=1)
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

        # Selección de tipo de vehículo
        self.vehicle_type = tk.StringVar(value="car")
        type_frame = tk.Frame(input_frame, bg="white")
        type_frame.pack(fill=tk.X, pady=5)

        tk.Label(type_frame, text="Tipo de vehículo:", font=self.font_small,
                 bg="white", fg=self.dark_color).pack(side=tk.LEFT)

        ttk.Radiobutton(type_frame, text="Carro", variable=self.vehicle_type,
                       value="car").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Moto", variable=self.vehicle_type,
                       value="motorcycle").pack(side=tk.LEFT)

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

        self.vehicle_tree = ttk.Treeview(list_frame, columns=("Placa", "Tipo", "Hora", "Espacio"),
                                       show="headings", height=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.font_small)
        style.configure("Treeview", font=self.font_small, rowheight=25)

        self.vehicle_tree.heading("Placa", text="Placa")
        self.vehicle_tree.heading("Tipo", text="Tipo")
        self.vehicle_tree.heading("Hora", text="Hora Entrada")
        self.vehicle_tree.heading("Espacio", text="Espacio")
        self.vehicle_tree.column("Placa", width=80, anchor=tk.W)
        self.vehicle_tree.column("Tipo", width=60, anchor=tk.W)
        self.vehicle_tree.column("Hora", width=100, anchor=tk.W)
        self.vehicle_tree.column("Espacio", width=60, anchor=tk.W)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.vehicle_tree.yview)
        self.vehicle_tree.configure(yscrollcommand=scrollbar.set)

        self.vehicle_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar evento de clic en el canvas
        self.canvas.bind("<Button-1>", self.spot_clicked)

    def create_parking_map(self):
        """Crea el mapa lógico del parqueadero con vías de acceso."""
        self.map = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 1. Entrada principal (parte superior central)
        entrance_row = 0
        entrance_col = self.cols // 2 - 2
        self.map[entrance_row][entrance_col] = 'E'
        self.map[entrance_row][entrance_col+1] = 'E'
        
        # 2. Vía de acceso desde la entrada
        for i in range(1, 3):
            for j in range(entrance_col, entrance_col+2):
                self.map[i][j] = '↓'
        
        # 3. Vía principal horizontal
        main_road_row = 3
        for j in range(self.cols):
            self.map[main_road_row][j] = '↔'
        
        # 4. Vías secundarias verticales
        for i in range(main_road_row+1, self.rows):
            if (i - main_road_row) % 4 == 1:  # Cada 4 filas una vía de circulación
                for j in range(self.cols):
                    if 2 < j < self.cols-3:  # Dejar espacio para los parqueos
                        self.map[i][j] = '↔'
        
        # 5. Espacios de parqueo (en las filas entre vías)
        for i in range(main_road_row+1, self.rows):
            if (i - main_road_row) % 4 in [2, 3, 0]:  # Filas de parqueo
                for j in range(self.cols):
                    # Dejar espacio para las vías de circulación
                    if j < 2 or j >= self.cols-2:
                        continue
                    
                    # Patrón de parqueo en ángulo (alternando direcciones)
                    if (i - main_road_row) % 8 in [2, 3, 4]:  # Parqueo hacia la derecha
                        if j % 2 == 0:
                            self.map[i][j] = 'P'
                    else:  # Parqueo hacia la izquierda
                        if j % 2 == 1:
                            self.map[i][j] = 'P'
        
        # 6. Salida (parte inferior central)
        exit_row = self.rows - 1
        exit_col = self.cols // 2 - 2
        self.map[exit_row][exit_col] = 'S'
        self.map[exit_row][exit_col+1] = 'S'
        
        # 7. Vía de salida
        for i in range(self.rows-3, self.rows-1):
            for j in range(exit_col, exit_col+2):
                self.map[i][j] = '↑'

    def draw_parking_lot(self):
        """Dibuja el parqueadero con vías de acceso realistas."""
        self.canvas.delete("all")
        self.parking_spots = []

        # Dibujar el fondo primero (área total)
        self.canvas.create_rectangle(0, 0, 
                                   self.cols * self.cell_size, 
                                   self.rows * self.cell_size,
                                   fill=self.road_color, outline="")

        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell_type = self.map[i][j]
                fill_color = self.road_color
                outline_color = ""
                text = ""
                text_fill_color = "white"
                draw_cell = True

                if cell_type == 'E':  # Entrada
                    fill_color = self.success_color
                    text = "ENTRADA"
                    outline_color = "white"
                    text_fill_color = "white"
                elif cell_type == 'S':  # Salida
                    fill_color = self.danger_color
                    text = "SALIDA"
                    outline_color = "white"
                    text_fill_color = "white"
                elif cell_type in ['↔', '↓', '↑']:  # Vías de circulación
                    # Dibujar marcas viales
                    if cell_type == '↔':  # Vía horizontal
                        if j % 3 == 0:  # Línea central discontinua
                            self.canvas.create_line(x1, (y1+y2)/2, x1+self.cell_size//2, (y1+y2)/2,
                                                  fill=self.marking_color, width=2)
                    else:  # Vía vertical
                        if i % 3 == 0:  # Línea central discontinua
                            self.canvas.create_line((x1+x2)/2, y1, (x1+x2)/2, y1+self.cell_size//2,
                                                  fill=self.marking_color, width=2)
                    continue
                elif cell_type == 'P':  # Parqueadero
                    fill_color = self.light_color
                    outline_color = self.parking_color
                    text = f"{i}-{j}"
                    text_fill_color = self.dark_color
                    self.parking_spots.append((i, j, x1, y1, x2, y2))
                    
                    # Dibujar espacio de parqueo
                    self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2,
                                               fill=fill_color, outline=outline_color, width=2)
                    
                    # Líneas diagonales para ángulo de parqueo
                    if (i - 4) % 8 in [2, 3, 4]:  # Parqueo hacia derecha
                        self.canvas.create_line(x1+5, y1+5, x2-5, y2-5,
                                              fill="#95a5a6", width=1, dash=(2, 2))
                    else:  # Parqueo hacia izquierda
                        self.canvas.create_line(x2-5, y1+5, x1+5, y2-5,
                                              fill="#95a5a6", width=1, dash=(2, 2))
                    
                    # Número de espacio
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                          font=self.font_small, fill=text_fill_color)
                    continue
                elif cell_type == 'X':  # Parqueadero ocupado
                    fill_color = "#fde8e8"
                    outline_color = "#f5b7b1"
                    text_fill_color = self.dark_color

                # Dibujar la celda base
                if draw_cell:
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                               fill=fill_color, outline=outline_color, width=2)
                
                if text:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                          font=self.font_small, fill=text_fill_color)

        # Dibujar vehículos
        self.draw_vehicles()
        self.update_availability()

    def load_vehicle_images(self):
        """Crea imágenes de vehículos para mostrar en los espacios."""
        self.vehicle_images = {
            "car": [],  # Imágenes de carros
            "motorcycle": []  # Imágenes de motos
        }
        
        # Colores para carros
        car_colors = ["#e74c3c", "#3498db", "#9b59b6", "#1abc9c", "#f39c12"]
        
        # Crear imágenes de carros
        for color in car_colors:
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

            self.vehicle_images["car"].append(ImageTk.PhotoImage(img))
        
        # Colores para motos
        motorcycle_colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6"]
        
        # Crear imágenes de motos
        for color in motorcycle_colors:
            img = Image.new('RGBA', (40, 25), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Cuerpo de la moto
            draw.ellipse([5, 15, 15, 25], fill="#2c3e50")  # Rueda trasera
            draw.ellipse([25, 15, 35, 25], fill="#2c3e50")  # Rueda delantera
            
            # Chasis
            draw.line([10, 20, 30, 10], fill=color, width=3)
            draw.line([30, 10, 35, 20], fill=color, width=3)
            
            # Asiento
            draw.line([15, 15, 25, 10], fill=color, width=4)

            self.vehicle_images["motorcycle"].append(ImageTk.PhotoImage(img))

    def draw_vehicles(self):
        """Dibuja los vehículos en los espacios ocupados."""
        for plate, data in self.vehicles.items():
            i, j = data['spot']
            x_center = j * self.cell_size + self.cell_size / 2
            y_center = i * self.cell_size + self.cell_size / 2

            # Seleccionar imagen basada en tipo de vehículo y hash de la placa
            vehicle_type = data['type']
            images = self.vehicle_images[vehicle_type]
            vehicle_idx = int(hashlib.sha1(plate.encode()).hexdigest(), 16) % len(images)
            vehicle_img = images[vehicle_idx]

            # Dibujar vehículo
            self.canvas.create_image(x_center, y_center - 5, image=vehicle_img)
            self.canvas.create_text(x_center, y_center + 15, text=plate[:7],
                                 font=self.font_small, fill=self.dark_color)

    def update_availability(self):
        """Actualiza la información de disponibilidad."""
        total = len(self.parking_spots)
        occupied = len(self.vehicles)
        available = total - occupied

        # Contar vehículos por tipo
        cars = sum(1 for v in self.vehicles.values() if v['type'] == 'car')
        motorcycles = sum(1 for v in self.vehicles.values() if v['type'] == 'motorcycle')

        self.availability_label.config(
            text=f"Espacios totales: {total}\n"
                 f"Ocupados: {occupied} (Carros: {cars}, Motos: {motorcycles})\n"
                 f"Disponibles: {available}\n"
                 f"Tasa de ocupación: {occupied/total:.0%}" if total > 0 else "0%"
        )

        self.update_vehicle_list()

    def update_vehicle_list(self):
        """Actualiza la lista de vehículos en el Treeview."""
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)

        for plate, data in self.vehicles.items():
            time = data['entry_time'].strftime("%Y-%m-%d %H:%M:%S")
            spot = f"{data['spot'][0]}-{data['spot'][1]}"
            vehicle_type = "Carro" if data['type'] == 'car' else "Moto"
            self.vehicle_tree.insert("", tk.END, values=(plate, vehicle_type, time, spot))

    def spot_clicked(self, event):
        """Maneja clics en espacios del parqueadero."""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        for spot_info in self.parking_spots:
            i, j, x1, y1, x2, y2 = spot_info
            if x1 <= x <= x2 and y1 <= y <= y2:
                if self.map[i][j] == 'X':
                    for plate, data in self.vehicles.items():
                        if data['spot'] == (i, j):
                            self.show_vehicle_info(plate, data)
                            break
                elif self.map[i][j] == 'P':
                    messagebox.showinfo("Espacio Libre",
                                     f"Espacio {i}-{j} disponible")
                break

    def show_vehicle_info(self, plate, data):
        """Muestra información detallada de un vehículo."""
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Información del Vehículo {plate}")
        info_window.geometry("400x350")
        info_window.resizable(False, False)
        info_window.configure(bg="white")

        main_frame = tk.Frame(info_window, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Imagen del vehículo
        vehicle_type = data['type']
        images = self.vehicle_images[vehicle_type]
        vehicle_idx = int(hashlib.sha1(plate.encode()).hexdigest(), 16) % len(images)
        vehicle_img = images[vehicle_idx]

        tk.Label(main_frame, image=vehicle_img, bg="white").pack(pady=10)

        # Información
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=5)

        tk.Label(info_frame, text="Placa:", font=self.font_medium,
                 bg="white", fg=self.dark_color, width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(info_frame, text=plate, font=self.font_medium,
                 bg="white", fg=self.primary_color).pack(side=tk.LEFT)

        tk.Label(info_frame, text="Tipo:", font=self.font_medium,
                 bg="white", fg=self.dark_color, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(10,0))
        vehicle_type_text = "Carro" if vehicle_type == 'car' else "Moto"
        tk.Label(info_frame, text=vehicle_type_text, font=self.font_medium,
                 bg="white", fg=self.primary_color).pack(side=tk.LEFT)

        tk.Label(info_frame, text="Espacio:", font=self.font_medium,
                 bg="white", fg=self.dark_color, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(10,0))
        tk.Label(info_frame, text=f"{data['spot'][0]}-{data['spot'][1]}", font=self.font_medium,
                 bg="white", fg=self.primary_color).pack(side=tk.LEFT)

        # Hora de entrada
        entry_frame = tk.Frame(main_frame, bg="white")
        entry_frame.pack(fill=tk.X, pady=5)

        tk.Label(entry_frame, text="Hora de entrada:", font=self.font_medium,
                 bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)
        tk.Label(entry_frame, text=data['entry_time'].strftime('%Y-%m-%d %H:%M:%S'),
                 font=self.font_small, bg="white", fg=self.dark_color, anchor=tk.W).pack(fill=tk.X)

        # Calcular tiempo y costo
        time_parked = datetime.datetime.now() - data['entry_time']
        hours = time_parked.total_seconds() / 3600
        rate = self.hourly_rate_car if data['type'] == 'car' else self.hourly_rate_motorcycle
        cost = rate * math.ceil(hours * 2) / 2  # Redondeo a media hora

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

        info_window.vehicle_img = vehicle_img

    def add_vehicle(self):
        """Registra un nuevo vehículo en el parqueadero."""
        plate = self.plate_entry.get().strip().upper()
        vehicle_type = self.vehicle_type.get()

        if not plate:
            messagebox.showerror("Error", "Ingrese una placa válida.")
            return

        if plate in self.vehicles:
            messagebox.showerror("Error", f"El vehículo {plate} ya está en el parqueadero.")
            return

        # Buscar espacio libre
        spot = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] == 'P':
                    spot = (i, j)
                    break
            if spot:
                break

        if not spot:
            messagebox.showwarning("Parqueadero Lleno", "No hay espacios disponibles.")
            return

        # Registrar vehículo
        i, j = spot
        self.map[i][j] = 'X'
        self.vehicles[plate] = {
            'entry_time': datetime.datetime.now(),
            'spot': spot,
            'type': vehicle_type
        }

        self.draw_parking_lot()
        self.plate_entry.delete(0, tk.END)
        messagebox.showinfo("Vehículo Registrado",
                          f"Vehículo {plate} ({'Carro' if vehicle_type == 'car' else 'Moto'}) estacionado en espacio {i}-{j}.")

    def remove_vehicle(self):
        """Registra la salida de un vehículo y calcula el costo."""
        plate = self.plate_entry.get().strip().upper()

        if not plate:
            messagebox.showerror("Error", "Ingrese una placa válida.")
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
        rate = self.hourly_rate_car if data['type'] == 'car' else self.hourly_rate_motorcycle
        cost = rate * math.ceil(hours * 2) / 2

        # Liberar espacio
        i, j = data['spot']
        self.map[i][j] = 'P'
        del self.vehicles[plate]

        self.draw_parking_lot()
        self.plate_entry.delete(0, tk.END)

        # Mostrar recibo
        receipt = f"RECIBO DE SALIDA\n\n"
        receipt += f"Placa: {plate}\n"
        receipt += f"Tipo: {'Carro' if data['type'] == 'car' else 'Moto'}\n"
        receipt += f"Espacio: {i}-{j}\n"
        receipt += f"Entrada: {entry_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"Salida: {exit_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"Tiempo: {str(parked_time).split('.')[0]}\n"
        receipt += f"Tarifa por hora: ${rate:,.0f}\n"
        receipt += f"\nTotal a pagar: ${cost:,.2f}"

        messagebox.showinfo("Salida Registrada", receipt)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernParkingSystem(root)
    root.mainloop()
