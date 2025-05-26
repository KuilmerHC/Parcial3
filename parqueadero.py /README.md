# PARQUEADERO PYTHON

### El proyecto esta basado en un sistema de parqueadero, comun y corriente, con todas sus funciones y siendo capaz de representar que tipo de vehiculo se estaciona en cada espacio dentro de su parqueadero (moto o carro)

## Documentación

Para el proyecto se usaron las librerias 
```python
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import math
import hashlib
```
del lenguaje de programación: Python
---
## 1. sys
Propósito: Proporciona acceso a variables y funciones específicas del sistema.

Uso en el código:

``` python
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
```
 Se usa para obtener la ruta del intérprete de Python actual (sys.executable) y asegurar que Pillow se instale usando la misma versión de Python que está ejecutando el script.
---
## 2. subprocess
Propósito: Permite la creación de nuevos procesos, conexión a sus canales de entrada/salida/error y obtención de sus códigos de retorno.

Uso en el código:
```python
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
```
Se utiliza para instalar automáticamente la librería Pillow si no está presente en el sistema, garantizando que el programa pueda funcionar sin requerir instalación manual de dependencias.
---
## 3. tkinter y ttk
   
Propósito: Crear la interfaz gráfica de usuario (GUI).

Uso en el código:
```python
import tkinter as tk
from tkinter import messagebox, ttk
```
Razón:

- **tkinter**: Librería estándar de Python para crear interfaces gráficas.

- **messagebox**: Para mostrar diálogos de alerta, información y confirmación.

- **ttk**: Proporciona widgets temáticos más modernos que los estándar de tkinter (como Treeview para la tabla de vehículos).
---
## 4. datetime

Propósito: Manipulación de fechas y horas.

Uso en el código:

```python
import datetime
datetime.datetime.now() # Para obtener la hora actual
```
Razón: 

- Registrar la hora de entrada/salida de vehículos y entragar una hora exacta a la hora de dar el recibo.

- Calcular el tiempo estacionado y el costo correspondiente.

- Mostrar la hora actual en la interfaz.
---
## 5. math
Propósito: Operaciones matemáticas.

Uso en el código:
```python
import math
math.ceil(hours * 2) / 2 # Redondeo a media hora
```

Razón: Para redondear el tiempo estacionado a medias horas (0.5) en el cálculo de tarifas.
---
## 6. hashlib
Propósito: Proporciona funciones hash seguras.

Uso en el código:
```python
import hashlib
hashlib.sha1(plate.encode()).hexdigest() # Generar hash de la placa
```
Razón:

- Generar un valor hash único a partir de la placa del vehículo.

- Se usa para asignar consistentemente una imagen o color a cada vehículo basado en su placa.
---
## 7. PIL (Pillow)
Propósito: Procesamiento de imágenes.

Uso en el código:
```python
from PIL import Image, ImageTk, ImageDraw, ImageFont
```

Razón:

- **Image**: Para crear y manipular imágenes de vehículos (carros y motos).

- **ImageTk**: Para convertir imágenes PIL en formato compatible con tkinter.

- **ImageDraw**: Para dibujar formas (cuerpos de vehículos, ruedas, etc.).

- **ImageFont**: Para renderizar texto en imágenes (usado en el logo).



## Referencias
**Imágenes:** Todas las imagenes usadas en el juego fueron creadas con inteligencia artificial (ChatGPT)
