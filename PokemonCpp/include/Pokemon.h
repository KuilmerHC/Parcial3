#pragma once
#include <string>
#include <vector>
#include "Ataque.h"
#include "Tipo.h"


class Pokemon {
    public:
        Pokemon(std::string nombre, Tipo tipo, int nivel,
                int vidaMaxima, int ataqueBase, int defensaBase);
        
        std::string getNombre() const;
        Tipo getTipo() const;
        int getNivel() const;
        int getVidaActual() const;
        int getVidaMaxima() const;
        int getAtaqueBase() const;
        int getDefensabase() const;
        // Devuelve una referencia constante a la lista vector porque pueden ser max 4
        const std::vector<Ataque>& getAtaques() const;

        // Pokemon aprende un nuevo ataque
        void aprenderAtaque(const Ataque& nuevoAtaque);

        //Reduce la vida del Pokemon
        void recibirDanio(int cantidadDanio);

        // Tiene vida?
        bool estaVivo() const;
    
    private:
        std::string nombre;
        Tipo tipoElemental;
        int nivel;
        int vidaMaxima;
        int vidaActual;
        int ataqueBase;
        int defensaBase;
        
        // Si un pokemon tienen varios ataques
        std::vector<Ataque> listaAtaques;
        
};