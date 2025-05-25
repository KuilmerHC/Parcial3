
# Batalla tipo Pokemon

El proyecto se basa un juego dos personajes (usuario y juagador predefinido) con distintos ataques, el ganador es el que logre derrotar al otro.


## Documentación

Para el proyecto se uso la libreria SFML version 2.6.1


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


