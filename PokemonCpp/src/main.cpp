#include <SFML/Graphics.hpp>
#include <SFML/System/Clock.hpp> 
#include <SFML/System/Time.hpp> 
#include <iostream> 
#include <string>
#include <random>
#include "Pokemon.h"
#include "Ataque.h"

int main () {

    // ----------------------------------- Definir ataques ---------------------------------------------
    Ataque mordisco("FrisMordisco",7);
    Ataque exclusivo("Nadie, como Frisby lo Hace", 8);
    Ataque pollo("FrisTerapia", 10);

    Ataque picotazo("Frispicotazo", 6);
    Ataque fiebre("Fiebre de frisby", 5);
    Ataque patada("Frispatada", 13);

    Pokemon jugador ("Frisby Colombiano", Tipo::ORIGINAL, 1, 45, 20, 49);
    jugador.aprenderAtaque(mordisco);
    jugador.aprenderAtaque(exclusivo);
    jugador.aprenderAtaque(pollo);

    Pokemon oponente ("Frisby Copia", Tipo::COPIA, 1, 45, 20, 42);
    oponente.aprenderAtaque(picotazo);
    oponente.aprenderAtaque(fiebre);
    oponente.aprenderAtaque(patada);

    // -------------------------------------- Consola -----------------------------------------------------
    // jugador
    std::cout << "Jugador: " << jugador.getNombre() << "(nivel " << jugador.getNivel() << ")" << std::endl;
    std::cout << "Vida: " << jugador.getVidaActual() << "/" << jugador.getVidaMaxima() << std::endl;
    std::cout << "Ataques aprendidos: " << std::endl;
    for (const Ataque& atk : jugador.getAtaques()) {
        std::cout << " - " << atk.getNombre() << " (Poder: " << atk.getPoderBase() << ")" << std::endl;
    }
    // oponente
    std::cout << "\nOponente: " << oponente.getNombre() << "(Nivel " << oponente.getNivel() << ")" << std::endl; 
    std::cout << " Vida: " << oponente.getVidaActual() << "/" << oponente.getVidaMaxima() << std::endl;



    // ------------------------------- SFML Y VENTANA DE JUEGO --------------------------------------------
    sf::RenderWindow window(sf::VideoMode(800, 600), "Frisby Game");
    window.setFramerateLimit(60); // fps

    sf::Font font;
    if (!font.loadFromFile("assets/fonts/Pokemon_Hollow.ttf")) { 
        std::cerr << "Error al cargar la fuente desde assets/fonts/" << std::endl;
        return 1;
    }

    // Texturas Pokemones
    sf::Texture pokemonTexture;
    if (!pokemonTexture.loadFromFile("assets/images/frisbyoriginal.png")) { 
        std::cerr << "Error: No se pudo cargar la textura desde assets/images/" << std::endl;
        return 1;
    }

    sf::Texture oponenteTexture;
    if (!oponenteTexture.loadFromFile("assets/images/frisbycopia.png")) { 
        std::cerr << "Error: No se pudo cargar la textura del oponente desde assets/images/" << std::endl;
        return 1;
    }

    // Fondo

    sf::Texture fondoBatalla;
    if(!fondoBatalla.loadFromFile("assets/images/fondo.jpg")){
            std::cerr << "Error: No se pudo cargar la textura del oponente desde assets/images/" << std::endl;
        return 1;
    }

    // ----------------------------------------  Menu de Ataques --------------------------------------
    // Momentos del combate
    enum class EstadoTurno {JUGADOR_ELIGE_ATAQUE, JUGADOR_ATACA, OPONENTE_ATACA, COMBATE_TERMINADO};
    EstadoTurno turnoActual = EstadoTurno::JUGADOR_ELIGE_ATAQUE;

    sf::Clock delayClock; // mide tiempo
    sf::Time delayDuration = sf::milliseconds(2500); // cuanto tiempo
    bool esperandoFinDeAccion = false; // saber si es una pausa
    EstadoTurno proximoTurnoLuegoDelay = EstadoTurno::JUGADOR_ELIGE_ATAQUE; //flujo despues de la pausa

    std::vector<sf::Text> textosAtaquesJugador;
    const int MAX_ATAQUES = 4;

    for (int i = 0; i < MAX_ATAQUES; i++) {
    sf::Text textoAtaque;
    textoAtaque.setFont(font);
    textoAtaque.setCharacterSize(20);
    textoAtaque.setFillColor(sf::Color::White);
    //pos
    textoAtaque.setPosition(200.f, 70.f +(i * 25.f));
    textosAtaquesJugador.push_back(textoAtaque);
    }

    // Mensajes de Combate
    sf::Text mensajeCombateText;
    mensajeCombateText.setFont(font);
    mensajeCombateText.setCharacterSize(23);
    mensajeCombateText.setFillColor(sf::Color::White);
    mensajeCombateText.setPosition(200.f, 30.f);
    mensajeCombateText.setString("¿Cómo debería atacar " + jugador.getNombre() + "?" );

    // ------------------------- Creación de SPRITE JUGADOR -----------------------
    sf::Sprite pokemonSprite;
    pokemonSprite.setTexture(pokemonTexture);
    // Escala Y posición
    pokemonSprite.setScale(1.f, 1.f);
    pokemonSprite.setPosition(50.f, 280.f);
    // Nombre Pokemon 
    sf::Text nombrePokemonText;
    nombrePokemonText.setFont(font);
    nombrePokemonText.setString(jugador.getNombre());
    nombrePokemonText.setCharacterSize(24);
    nombrePokemonText.setFillColor(sf::Color::White);
    // posicion de acuerdo al Sprite
    nombrePokemonText.setPosition(60.f, 160.f);
    // Vida POkemon
    sf::Text vidaPokemonText;
    vidaPokemonText.setFont(font);
    std::string vidaStr = "HP: " + std::to_string(jugador.getVidaActual()) + "/" + std::to_string(jugador.getVidaMaxima());
    vidaPokemonText.setString(vidaStr);
    vidaPokemonText.setCharacterSize(20);
    vidaPokemonText.setFillColor(sf::Color::White);
    vidaPokemonText.setPosition(nombrePokemonText.getPosition().x, nombrePokemonText.getPosition().y + 30.f);

 // ------------------------- Creación de SPRITE OPONENTE -----------------------
    sf::Sprite oponenteSprite;
    oponenteSprite.setTexture(oponenteTexture);
    // Escala Y posición
    oponenteSprite.setScale(1.f, 1.f);
    oponenteSprite.setPosition(500.f, 230.f);
    // Nombre Pokemon 
    sf::Text nombreOponenteText;
    nombreOponenteText.setFont(font);
    nombreOponenteText.setString(oponente.getNombre());
    nombreOponenteText.setCharacterSize(24);
    nombreOponenteText.setFillColor(sf::Color::White);
    // posicion 
    nombreOponenteText.setPosition(550.f, 160.f);

    sf::Text vidaOponenteText;
    vidaOponenteText.setFont(font);
    std::string vidaOpStr = "HP: " + std::to_string(oponente.getVidaActual()) + "/" + std::to_string(oponente.getVidaMaxima());
    vidaOponenteText.setString(vidaOpStr);
    vidaOponenteText.setCharacterSize(20);
    vidaOponenteText.setFillColor(sf::Color::White);
    vidaOponenteText.setPosition(nombreOponenteText.getPosition().x, nombreOponenteText.getPosition().y + 35.f);

    // Sprite Fondo
    sf::Sprite fondoBatallaSprite;
    fondoBatallaSprite.setTexture(fondoBatalla);
    float escalaX = static_cast<float>(window.getSize().x) / fondoBatalla.getSize().x;
    float escalaY = static_cast<float>(window.getSize().y) / fondoBatalla.getSize().y;
    fondoBatallaSprite.setScale(escalaX, escalaY);
    fondoBatallaSprite.setPosition(0.f, 0.f);

    int alfa = 110; //opacidad de fondo
    fondoBatallaSprite.setColor(sf::Color(255, 255, 255, alfa));

    // ------------------------ BARRAS DE VIDA (UI) ----------------------------------------
    // Jugador
    sf::RectangleShape barraVidaJugador(sf::Vector2f(150.f, 20.f)); // tamaño
    barraVidaJugador.setFillColor(sf::Color(50, 50, 50, 200)); // color
    barraVidaJugador.setOutlineColor(sf::Color::Black);
    barraVidaJugador.setOutlineThickness(1.f);
    barraVidaJugador.setPosition(60.f, 230.f);

    sf::RectangleShape barraVidaJugadorInterna(sf::Vector2f(100.f, 20.f));
    barraVidaJugadorInterna.setFillColor(sf::Color::Green);
    barraVidaJugadorInterna.setPosition(barraVidaJugador.getPosition());

    // Oponente
    sf::RectangleShape barraVidaOponente(sf::Vector2f(150.f, 20.f));
    barraVidaOponente.setFillColor(sf::Color(50, 50, 50, 200)); // color
    barraVidaOponente.setOutlineColor(sf::Color::Black);
    barraVidaOponente.setOutlineThickness(1.f);
    barraVidaOponente.setPosition(550.f, 230.f);

    sf::RectangleShape barraVidaOponenteInterna(sf::Vector2f(150.f, 20.f));
    barraVidaOponenteInterna.setFillColor(sf::Color::Green);
    barraVidaOponenteInterna.setPosition(barraVidaOponente.getPosition());

    // ------------------------------------------- BUCLE PRINCIPAL --------------------------------------------------
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }

            if (!esperandoFinDeAccion && event.type == sf::Event::KeyPressed) {
                // -------- SELECCIÓN DE ATAQUE DEL JUGADOR -------------------------------------
                if (turnoActual == EstadoTurno::JUGADOR_ELIGE_ATAQUE && jugador.estaVivo() && oponente.estaVivo()) {
                    int ataqueSeleccionadoIndex = -1;

                    if (event.key.code == sf::Keyboard::Num1 || event.key.code == sf::Keyboard::Numpad1) {
                        ataqueSeleccionadoIndex = 0;
                    } else if (event.key.code == sf::Keyboard::Num2 || event.key.code == sf::Keyboard::Numpad2) {
                        ataqueSeleccionadoIndex = 1;
                    } else if (event.key.code == sf::Keyboard::Num3 || event.key.code == sf::Keyboard::Numpad3) {
                        ataqueSeleccionadoIndex = 2;
                    } else if (event.key.code == sf::Keyboard::Num4 || event.key.code == sf::Keyboard::Numpad4) {
                        ataqueSeleccionadoIndex = 3;
                    }

                    // Pokemon conoce el ataque (menos que 4)
                    if (ataqueSeleccionadoIndex != -1 && ataqueSeleccionadoIndex < static_cast<int>(jugador.getAtaques().size())) {
                        const Ataque& ataqueJugador = jugador.getAtaques()[ataqueSeleccionadoIndex];
                        int danio = ataqueJugador.getPoderBase(); 

                        std::cout << "----------------------------------------" << std::endl;
                        mensajeCombateText.setString(jugador.getNombre() + " usa " + ataqueJugador.getNombre() + "!");
                        std::cout << jugador.getNombre() << " usa " << ataqueJugador.getNombre() << " contra " << oponente.getNombre() << "!" << std::endl;
                        std::cout << ataqueJugador.getNombre() << " hace " << danio << " de daño." << std::endl;

                        oponente.recibirDanio(danio);

                        if (!oponente.estaVivo()) {
                            std::cout << jugador.getNombre() << " ha ganado la pelea!" << std::endl;
                            mensajeCombateText.setString(jugador.getNombre() + " ha ganado la pelea!");
                            turnoActual = EstadoTurno::COMBATE_TERMINADO;
                            esperandoFinDeAccion = false;
                        } else {
                            esperandoFinDeAccion = true;
                            proximoTurnoLuegoDelay = EstadoTurno::OPONENTE_ATACA; // Pausa y Pasa al turno del oponente
                            delayClock.restart(); // reinicio reloj
                        }
                        std::cout << "----------------------------------------" << std::endl;
                    }
                }
            } 
        } 

        // ------------------------- ACTUALIZCACIONES------------------------------
        //Actualizar textos del menú de ataques del jugador 

        // Pausa activa finalizada pasa turno a oponente
        if (esperandoFinDeAccion) {
            if (delayClock.getElapsedTime() >= delayDuration) {
                esperandoFinDeAccion = false;
                turnoActual = proximoTurnoLuegoDelay;
            }
        }

        // Accion luego de NO estar esperando
        if(!esperandoFinDeAccion){
            if (turnoActual == EstadoTurno::JUGADOR_ELIGE_ATAQUE) {
                if (jugador.estaVivo() && oponente.estaVivo()) {
                    mensajeCombateText.setString("Que deberia hacer " + jugador.getNombre() + "?");
                }
                const auto& ataquesDelJugador = jugador.getAtaques();
                for (int i = 0; i < MAX_ATAQUES; ++i) {
                    if (i < static_cast<int>(ataquesDelJugador.size())) {
                        textosAtaquesJugador[i].setString(std::to_string(i + 1) + ". " + ataquesDelJugador[i].getNombre());
                    } else {
                        textosAtaquesJugador[i].setString("");
                    }
                }
            } else {
                for (int i = 0; i < MAX_ATAQUES; ++i) {
                    textosAtaquesJugador[i].setString("");
                }
                
            }

            // --- Turno del Oponente ---
            if (turnoActual == EstadoTurno::OPONENTE_ATACA) {
                if (oponente.estaVivo() && jugador.estaVivo()) {
                    if (!oponente.getAtaques().empty()) {
                        std::random_device rd;
                        std::mt19937 gen(rd());
                        std::uniform_int_distribution<> distrib(0,static_cast<int>(oponente.getAtaques().size()) - 1);
                        int indiceAtaqueOponenete = distrib(gen);
                        const Ataque& ataqueOponente = oponente.getAtaques()[indiceAtaqueOponenete];
                        int danioOponente = ataqueOponente.getPoderBase(); 

                        std::cout << "----------------------------------------" << std::endl;
                        mensajeCombateText.setString(oponente.getNombre() + " usa " + ataqueOponente.getNombre() + "!");
                        std::cout << oponente.getNombre() << " usa " << ataqueOponente.getNombre() << " contra " << jugador.getNombre() << "!" << std::endl;
                        std::cout << ataqueOponente.getNombre() << " hace " << danioOponente << " de daño." << std::endl;

                        jugador.recibirDanio(danioOponente);

                        if (!jugador.estaVivo()) {
                            std::cout << oponente.getNombre() << " ha ganado la pelea!" << std::endl;
                            mensajeCombateText.setString(oponente.getNombre() + " ha ganado la pelea!");
                            turnoActual = EstadoTurno::COMBATE_TERMINADO;
                            esperandoFinDeAccion = false;
                        } else {
                            esperandoFinDeAccion = true;
                            proximoTurnoLuegoDelay = EstadoTurno::JUGADOR_ELIGE_ATAQUE;
                            delayClock.restart();
                        }
                        std::cout << "----------------------------------------" << std::endl;
                    } else {
                        std::cout << oponente.getNombre() << " No conoce ningun ataque!" << std::endl;
                        esperandoFinDeAccion = true;
                        proximoTurnoLuegoDelay = EstadoTurno::JUGADOR_ELIGE_ATAQUE; // Oponente pasa el turno al jugador
                        delayClock.restart();
                    }
                } else { // Uno de los dos ya esta sin vida
                    turnoActual = EstadoTurno::COMBATE_TERMINADO;
                    esperandoFinDeAccion = false;
                }
            } 
            // Combate terminado
            if (turnoActual == EstadoTurno::COMBATE_TERMINADO) {
            
            }
        }

        // Actualizar la vida (txt)
        vidaStr = "HP: " + std::to_string(jugador.getVidaActual()) + "/" + std::to_string(jugador.getVidaMaxima());
        vidaPokemonText.setString(vidaStr);

        vidaOpStr = "HP: " + std::to_string(oponente.getVidaActual()) + "/" + std::to_string(oponente.getVidaMaxima());
        vidaOponenteText.setString(vidaOpStr);

        // -------------- Barras de Vida ----------------
        //Jugador
        float porcentajeVidaJugador = 0.f;
        if(jugador.getVidaMaxima() > 0){
            porcentajeVidaJugador = static_cast<float>(jugador.getVidaActual()) / jugador.getVidaMaxima();
        }
        barraVidaJugadorInterna.setSize(sf::Vector2f(barraVidaJugador.getSize().x * porcentajeVidaJugador, barraVidaJugador.getSize().y));
        if(porcentajeVidaJugador > 0.5f){
            barraVidaJugadorInterna.setFillColor(sf::Color::Green);
        } else if (porcentajeVidaJugador > 0.2f){
            barraVidaJugadorInterna.setFillColor(sf::Color::Yellow);
        } else {
            barraVidaJugadorInterna.setFillColor(sf::Color::Red);
        }

        //Oponente
        float porcentajeVidaOponente = 0.f;
        if(oponente.getVidaMaxima() > 0){
            porcentajeVidaOponente = static_cast<float>(oponente.getVidaActual()) / oponente.getVidaMaxima();
        }
        barraVidaOponenteInterna.setSize(sf::Vector2f(barraVidaOponente.getSize().x * porcentajeVidaOponente, barraVidaOponente.getSize().y));
        if(porcentajeVidaOponente > 0.5f){
            barraVidaOponenteInterna.setFillColor(sf::Color::Green);
        } else if (porcentajeVidaOponente > 0.2f){
            barraVidaOponenteInterna.setFillColor(sf::Color::Red);
        } else {
            barraVidaOponenteInterna.setFillColor(sf::Color::Red);
        }

        // ------------------------------------ Imagen Render ---------------------------------------
        window.clear(sf::Color::Black); 
        window.draw(fondoBatallaSprite);

        // Sprites
        window.draw(pokemonSprite);
        window.draw(oponenteSprite);

        // Textos de Nombres y Vidas
        window.draw(nombrePokemonText);
        window.draw(vidaPokemonText);
        window.draw(barraVidaJugador);
        window.draw(barraVidaJugadorInterna);

        window.draw(nombreOponenteText);
        window.draw(vidaOponenteText);
        window.draw(barraVidaOponente);
        window.draw(barraVidaOponenteInterna);

        // Mensaje de Combate General
        window.draw(mensajeCombateText);

        // Nombres de los Ataques del Jugador sin estar en espera
        if (!esperandoFinDeAccion && turnoActual == EstadoTurno::JUGADOR_ELIGE_ATAQUE && jugador.estaVivo() && oponente.estaVivo()) {
            for (const auto& textoAtaque : textosAtaquesJugador) {
                window.draw(textoAtaque);
            }
        }

        window.display();

    } 
    return 0;
}
