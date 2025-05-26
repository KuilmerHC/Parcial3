# PARQUEADERO EN PYTHON

### El proyecto esta basado en un sistema de parqueadero, comun y corriente, con todas sus funciones y siendo capaz de representar que tipo de vehiculo se estaciona en cada espacio dentro de su parqueadero (moto o carro)

## Documentación

Para el proyecto se usaron las librerias 

import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import math
import hashlib 
de Python
1. sys
Propósito: Proporciona acceso a variables y funciones específicas del sistema.

Uso en el código:

```python 
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
```

Razón: Se usa para obtener la ruta del intérprete de Python actual (sys.executable) y asegurar que Pillow se instale usando la misma versión de Python que está ejecutando el script.


### Instrucciones para compilar y ejecutar el juego en Linux:

Instalar git:

```bash
  sudo apt update
  sudo apt install git
```
Instalar el Compilador C++ (g++):

```bash
  sudo apt install build-essential
```

Instalar biblioteca de SFML:
```bash
  sudo apt install libsfml-dev
```

Clonar el proyecto:

```bash
  git clone https://github.com/KuilmerHC/Parcial3.git
```

Ir al directorio del proyecto:

```bash
  cd Parcial3/PokemonCpp/
```

Compilar y ejecutar:

```bash
mkdir -p build && g++ -Iinclude src/main.cpp src/Pokemon.cpp src/Ataque.cpp -o build/PokemonBatalla -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio -std=c++17 -Wall -Wextra -g

./build/PokemonBatalla
```


## Implementaciones del Sistema de Combate

### 1. Sistema de Ataques Diferenciados por Pokémon

Cada Pokémon cuenta con un conjunto único de ataques disponibles, lo que proporciona mayor dinamismo y variabilidad al combate. Esta implementación garantiza que cada encuentro presente opciones estratégicas distintas y evita la monotonía en los resultados de las batallas.

---

### 2. Temporización Entre Turnos de Ataque

Se estableció un sistema de espera controlada entre ataques para permitir el procesamiento adecuado de cada turno. Esta funcionalidad facilita la comprensión visual del ataque utilizado y el daño infligido, mejorando la experiencia del usuario durante el combate.

**Desarrollo técnico:** Para esta implementación se utilizó asistencia del modelo LLM Google AI Studio para comprender el manejo correcto de las librerías de tiempo en SFML. Se emplearon las siguientes cabeceras:

```bash
  #include <SFML/System/Clock.hpp>
  #include <SFML/System/Time.hpp>

```

Estas librerías permitieron crear pausas controladas entre turnos y gestionar los tiempos de animación de manera precisa.

---

### 3. Selección Aleatoria de Ataques del Oponente

El sistema implementa una mecánica de selección automática y aleatoria de ataques para el contrincante.

**Desarrollo técnico:** Se recurrió al modelo LLM Google AI Studio para entender la implementación correcta de la generación de números aleatorios en C++. Se utilizó la cabecera:

```bash
  #include <random> 

```

La cual tiene herramientas modernas para la generación de números pseudoaleatorios, garantizando una selección equitativa y eficiente de los ataques del oponente.

---

### 4. Sistema Visual de Barras de Vida

Se desarrollaron indicadores visuales que representan la salud actual de cada Pokémon mediante barras de vida:
- **Verde**: Vida alta
- **Amarillo**: Vida media  
- **Rojo**: Vida crítica

Esta implementación facilita la interpretación inmediata del estado de salud de ambos combatientes.

---

### 5. Clasificación de Tipos de Pokémon

El sistema establece cuatro categorías principales de Pokémon basadas en el contexto del jugador:
- **NINGUNO**: Estado por defecto
- **NORMAL**: Pokémon estándar
- **ORIGINAL**: Pokémon base del jugador
- **COPIA**: Pokémon duplicado o secundario

Esta tipificación permite una mejor organización y gestión de los elementos de juego.

---

### 6. Ambientación Visual del Campo de Batalla

Se incorporó un fondo temático específico para las batallas, apropiado para los enfrentamientos.

## Referencias
**Imágenes:** Todas las imagenes usadas en el juego fueron creadas con inteligencia artificial (ChatGPT)

