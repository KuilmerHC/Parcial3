#pragma once
#include <string>

class Ataque {
    public:
    Ataque(std::string nombre, int poderBase);
    
    std::string getNombre() const;
    int getPoderBase() const;

    private:
    std::string nombre;
    int poderBase;
    
};