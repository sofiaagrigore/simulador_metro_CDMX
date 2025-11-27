# /// script
# dependencies = [
#    "networkx",
# ]
# ///
import asyncio
import pygame # Necesario para pygbag a veces aunque no se use directo aqui

# Importamos nuestros modulos
import metroCDMX
import aStarNetworkX
import ui

async def main():
    # 1. Obtenemos los datos (MODELO)
    print("Cargando datos del metro...")
    metro_grafo = metroCDMX.getMetro()

    # 2. Inicializamos el algoritmo con esos datos (LOGICA)
    # Esto es crucial: le pasamos el grafo al modulo de A* para que pueda calcular distancias
    aStarNetworkX.inicializar_algoritmo(metro_grafo)

    # 3. Lanzamos la interfaz grafica (VISTA)
    # Le pasamos el grafo (para pintar estaciones) y la funcion 'caminoOptimo' (para calcular rutas)
    print("Iniciando interfaz grafica...")
    await ui.initGUI(metro_grafo, aStarNetworkX.caminoOptimo)

    # Bucle infinito final para mantener vivo el proceso async (requerido por pygbag)
    while True:
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())