#include "Ataque.h"

Ataque::Ataque(std::string nombreAtaque, int poder)
    : nombre(nombreAtaque), poderBase(poder){
    }

std::string Ataque::getNombre() const {
    return nombre;
}

int Ataque::getPoderBase() const {
    return poderBase;
}
