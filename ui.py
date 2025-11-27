import pygame
import sys
import asyncio
import os
from typing import Callable, List, Tuple

def transformar_coordenadas(coords, seccion_sup_izq, seccion_inf_der, tamaño_destino=None):
    x1, y1 = seccion_sup_izq
    x2, y2 = seccion_inf_der

    ancho = x2 - x1
    alto = y2 - y1

    transformadas = []
    for x, y in coords:
        x_rel = x - x1
        y_rel = y - y1

        if tamaño_destino:
            ancho_dest, alto_dest = tamaño_destino
            x_rel = (x_rel / ancho) * ancho_dest
            y_rel = (y_rel / alto) * alto_dest

        transformadas.append((x_rel, y_rel))

    return transformadas

async def initGUI(grafo, algorithm: Callable[[str, str], List[str]]):
    
    # Lista con los nombres de las estaciones
    nombres = list(grafo.nodes)
    
    # Lista con las coordenadas de las estaciones (Tus coordenadas hardcodeadas originales)
    coordsGrandes = [
        (115,693),(152,653),(189,617),(221,585),(258,548),(296,519),(336,519),(379,519), #L1
        (379,454),(379,552),(379,588),(379,653),(379,689),(379,722),(379,758),(379,793),(379,827),(379,863),(379,897),(379,932),(379,966), #L3
        (152,465),(152,531),(152,593),(152,713),(152,747),(152,793),(152,851), #L7
        (232,653),(322,653),(472,653), #L9
        (215,793),(291,793),(466,793),(520,873), #L12
    ]
    
    mapaPequeno=True
    if(mapaPequeno):
        coords = transformar_coordenadas(
            coordsGrandes,
            seccion_sup_izq=(13, 434),
            seccion_inf_der=(538, 1041),
            tamaño_destino=(705, 808)
        )
        imagen="MetroCDMX.png"
        tamano = (650,750)
    else:
        coords=coordsGrandes
        imagen="MapaMetroCDMX.png"
        tamano = (680,790)

    pygame.init()

    screen = pygame.display.set_mode(tamano)

    # Images folder path
    img_path = os.path.join(os.path.dirname(__file__), "img")
    print("Ruta de imagenes:", img_path)

    metroMap = pygame.image.load(os.path.join(img_path, imagen)).convert()

    # Scaling logic
    try:
        orig_w, orig_h = metroMap.get_size()
        if (orig_w, orig_h) != tamano:
            fx = tamano[0] / orig_w
            fy = tamano[1] / orig_h
            metroMap = pygame.transform.scale(metroMap, tamano)
            coords = [(int(x * fx), int(y * fy)) for (x, y) in coords]
    except Exception:
        pass

    # Start button
    startButton = pygame.image.load(os.path.join(img_path, "start.png")).convert_alpha()
    startButton = pygame.transform.scale(startButton, (100, 50))
    startButtonRect = startButton.get_rect()
    ButtonPos = (70,635)
    startButtonRect = startButtonRect.move(ButtonPos)

    # Reset button
    resetButton = pygame.image.load(os.path.join(img_path, "reset.png")).convert_alpha()
    resetButton = pygame.transform.scale(resetButton, (50, 50))
    resetButtonRect = resetButton.get_rect()
    resetButtonRect = resetButtonRect.move(ButtonPos)

    screen.blit(metroMap, (0, 0))
    screen.blit(startButton, ButtonPos)

    font = pygame.font.Font('freesansbold.ttf', 25)

    font = pygame.font.Font('freesansbold.ttf', 25)
    text1 = font.render('Seleccione un origen', True, (0,0,0), (255,255,255))
    text2 = font.render('Seleccione un destino', True, (0,0,0), (255,255,255))
    text3 = font.render('Mostrando ruta...', True, (0,0,0), (255,255,255))

    pygame.display.flip()

    # Variables de estado
    phase = 0
    origin = ""
    destiny = ""
    coordsOrigin = (0,0)
    coordsDestiny = (0,0)
    route = []

    # UI LOOP
    while True:
        if phase==0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if startButtonRect.collidepoint(pos):
                        screen.blit(metroMap, (0, 0))
                        screen.blit(text1, ButtonPos)
                        for i in coords:
                            pygame.draw.circle(screen,(0,0,0),i,6)
                            pygame.draw.circle(screen,(255,255,255),i,3)
                        pygame.display.flip()
                        phase=1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif phase==1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i in coords:
                        if abs(i[0]-pos[0])<=6 and abs(i[1]-pos[1])<=6:
                            origin = nombres[coords.index(i)]
                            print("Origen seleccionado: ", origin)
                            coordsOrigin = i
                            screen.blit(metroMap, (0, 0))
                            screen.blit(text2, (250,30))
                            for o in coords:
                                pygame.draw.circle(screen,(0,0,0),o,6)
                                pygame.draw.circle(screen,(255,255,255),o,3)
                            pygame.draw.circle(screen,(0,0,0),i,7)
                            pygame.display.flip()
                            phase = 2
                            break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif phase==2:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i in coords:
                        if abs(i[0]-pos[0])<=6 and abs(i[1]-pos[1])<=6:
                            destiny = nombres[coords.index(i)]
                            print("Destiny seleccionado: ", destiny)
                            coordsDestiny = i
                            screen.blit(metroMap, (0, 0))
                            for o in coords:
                                pygame.draw.circle(screen,(0,0,0),o,6)
                                pygame.draw.circle(screen,(255,255,255),o,3)
                            pygame.draw.circle(screen,(0,0,0),coordsOrigin,7)
                            pygame.draw.circle(screen,(0,0,0),coordsDestiny,7)
                            screen.blit(text3, (300,60))
                            pygame.display.flip()
                            
                            phase=3
                            # LLAMADA AL ALGORITMO
                            route = algorithm(origin, destiny)
                            break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif phase==3:
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Animacion de la ruta
            for station in route:
                await asyncio.sleep(0.2) 
                idx = nombres.index(station)
                pygame.draw.circle(screen,(255, 51, 153),coords[idx],7)
                pygame.draw.circle(screen,(0,0,0),coords[idx],3)
                pygame.display.flip()
            
            phase=4
        
        elif phase==4:
            screen.blit(metroMap, (0, 0))
            for station in route:
                idx = nombres.index(station)
                pygame.draw.circle(screen,(255, 255, 0),coords[idx],7)
                pygame.draw.circle(screen,(0,0,0),coords[idx],3)
            screen.blit(resetButton, ButtonPos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if resetButtonRect.collidepoint(pos):
                        screen.blit(metroMap, (0, 0))
                        screen.blit(startButton, ButtonPos)
                        pygame.display.flip()
                        phase=0
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        await asyncio.sleep(0)