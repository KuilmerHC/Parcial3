#include "Pokemon.h"
#include <iostream>



Pokemon::Pokemon(std::string nombre, Tipo tipo, int nivel,
                int vidaMaxima, int ataqueBase, int defensaBase){
    this->nombre = nombre;
    this->tipoElemental = tipo;
    this->nivel = nivel;
    this->vidaMaxima = vidaMaxima;
    this->vidaActual = vidaMaxima; // Inicia igual a MAX
    this->ataqueBase = ataqueBase;
    this->defensaBase = defensaBase;
}

//Getters, obtener info privada del pokemon
std::string Pokemon::getNombre() const {
    return nombre;
}
Tipo Pokemon::getTipo() const {
    return tipoElemental;
}
int Pokemon::getNivel() const {
    return nivel;
}
int Pokemon::getVidaActual() const {
    return vidaActual;
}
int Pokemon::getVidaMaxima() const {
    return vidaMaxima;
}
int Pokemon::getAtaqueBase() const {
    return ataqueBase;
}
int Pokemon::getDefensabase() const {
    return defensaBase;
}

const std::vector<Ataque>& Pokemon::getAtaques() const {
    return listaAtaques;
}

// Maxz 4 ataques por pokemon
void Pokemon::aprenderAtaque(const Ataque& nuevoataque) {
    if (listaAtaques.size() < 4) {
        listaAtaques.push_back(nuevoataque); //Añade una copia del ataque a la lista
    } else {
        std::cout << nombre << " ya tiene 4 ataques, NO puede aprender más" << std::endl;
    }
}

// NO puede haber daño negativo
void Pokemon::recibirDanio(int cantidadDanio){
    if (cantidadDanio < 0) {
        cantidadDanio = 0;
    }
    vidaActual -= cantidadDanio;
    if(vidaActual < 0) {
        vidaActual = 0; // La vida sera minimo 0
    }
}

bool Pokemon::estaVivo() const {
    return vidaActual > 0;
}