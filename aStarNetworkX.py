import math
import networkx as nx

# Variable interna para almacenar el grafo una vez se inicialice
_grafo_global = None

def inicializar_algoritmo(grafo_recibido):
    """
    Recibe el grafo desde el main y lo guarda para usarlo en las funciones de ruta.
    """
    global _grafo_global
    _grafo_global = grafo_recibido

# Replace geopy with a simple haversine distance calculation
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 
    return c * r

def h_distanciaEuclidea(nodoActual, nodoObjetivo):
    """
    La funcion heuristica: por distancia haversine
    """
    if _grafo_global is None:
        raise ValueError("El algoritmo no ha sido inicializado con un grafo.")

    lat1 = _grafo_global.nodes[nodoActual]['lat']
    lon1 = _grafo_global.nodes[nodoActual]['lon']
    lat2 = _grafo_global.nodes[nodoObjetivo]['lat']
    lon2 = _grafo_global.nodes[nodoObjetivo]['lon']
    return haversine_distance(lat1, lon1, lat2, lon2)

def caminoOptimo(nodoOrigen, nodoDestino):
    """
    Funcion para obtener el camino optimo usando algoritmo de A*
    """
    if _grafo_global is None:
        raise ValueError("El algoritmo no ha sido inicializado con un grafo.")
        
    if nodoOrigen not in _grafo_global.nodes or nodoDestino not in _grafo_global.nodes:
        raise ValueError("Nodo origen o destino no existe en el grafo")
        
    return nx.astar_path(_grafo_global, nodoOrigen, nodoDestino, heuristic=h_distanciaEuclidea, weight="weight")

def lengthCaminoOptimo(nodoOrigen, nodoDestino):
    if _grafo_global is None:
        raise ValueError("El algoritmo no ha sido inicializado con un grafo.")
    return nx.astar_path_length(_grafo_global, nodoOrigen, nodoDestino, heuristic=h_distanciaEuclidea, weight="weight")

def lenCualquiera(camino):
    if _grafo_global is None:
        raise ValueError("El algoritmo no ha sido inicializado con un grafo.")
    distancia_total = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i+1]
        distancia_total += _grafo_global[origen][destino]["weight"]
    return distancia_total