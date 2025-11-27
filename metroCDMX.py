#import pandas as pd
import os
import networkx as nx
import csv
# import matplotlib.pyplot as plt  <-- COMENTADO: No lo necesitamos para la simulación y pesa mucho

'''
Funcion para obtener grafo del metro
'''
def getMetro():
    print("--- INICIANDO CARGA DEL GRAFO ---") # Mensaje para la consola

    # Crear un grafo vacio
    grafo = nx.Graph()

    # 1. Definir rutas
    # __file__ nos da la ruta de este script (CDMX/metroCDMX.py)
    # dirname nos da la carpeta (CDMX)
    directorio_actual = os.path.dirname(__file__)
    
    coordsPath = os.path.join(directorio_actual, "coordsCDMX.csv")
    conexionesPath = os.path.join(directorio_actual, "conexiones.csv")

    print(f"--> Buscando coordenadas en: {coordsPath}") # Para ver si la ruta está bien

    # 2. Leer coordsCDMX.csv
    try:
        with open(coordsPath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            coords = list(reader)
        print(f"--> Coordenadas cargadas: {len(coords)} estaciones encontradas.")
    except Exception as e:
        print(f"!!! ERROR FATAL leyendo coordsCDMX.csv: {e}")
        return nx.Graph() # Devuelve grafo vacío para que no crashee totalmente

    # 3. Leer conexiones.csv
    try:
        with open(conexionesPath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            conexiones = list(reader)
        print(f"--> Conexiones cargadas: {len(conexiones)} tramos encontrados.")
    except Exception as e:
        print(f"!!! ERROR FATAL leyendo conexiones.csv: {e}")
        # No retornamos aquí para permitir ver al menos los nodos si fallan las aristas

    # 4. Crear nodos
    for fila in coords:
        try:
            grafo.add_node(
                fila['Nombre'],
                lat=float(fila['Latitud']),
                lon=float(fila['Longitud'])
            )
        except ValueError:
            print(f"Error en datos de estación: {fila}")

    # 5. Crear aristas
    for fila in conexiones:
        try:
            grafo.add_edge(
                fila['Origen'],
                fila['Destino'],
                weight=float(fila['Peso'])
            )
        except ValueError:
            print(f"Error en datos de conexión: {fila}")

    print("--- GRAFO CARGADO EXITOSAMENTE ---")
    return grafo

if __name__ == "__main__":
    metro = getMetro()
    print("Nodos:", metro.number_of_nodes())
    print("Aristas:", metro.number_of_edges())