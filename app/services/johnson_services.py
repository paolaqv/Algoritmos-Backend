import heapq

def bellman_ford(nodes, edges, source):
    """
    Ejecuta Bellman-Ford para calcular distancias minimas desde 'source'.
    :param nodes: Lista de nodos (por ejemplo, ['A', 'B', 'C', ...]).
    :param edges: Lista de aristas en formato (u, v, peso).
    :param source: Nodo fuente.
    :return: Diccionario de distancias {nodo: distancia, ...} o None si hay ciclo negativo. 
    """
    dist = { node: float('inf') for node in nodes }
    dist[source] = 0
    
    # Relajación de aristas |nodes| - 1 veces
    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                
    # Verificar ciclo negativo
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # Ciclo negativo detectado
    return dist

def dijkstra(nodes, graph, source):
    """
    Ejecuta el algoritmo de Dijkstra para encontrar los caminos mas cortos
    desde 'source' en un grafo con pesos no negativos.
    
    :param nodes: Lista de nodos.
    :param graph: Diccionario de adyacencia {u: [(v, peso), ...], ...}.
    :param source: Nodo fuente.
    :return: Diccionario con las distancias minimas desde 'source'.
    """
    dist = { node: float('inf') for node in nodes }
    dist[source] = 0
    heap = [(0, source)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

def johnson(nodes, edges):
    """
    algoritmo de Johnson para obtener los caminos mas cortos entre todos los pares.
    
    :param nodes: Lista de identificadores de nodos (ej. ['A', 'B', 'C', ...]).
    :param edges: Lista de aristas en formato (u, v, peso).
    :return: Diccionario de distancias, donde distances[u][v] es la distancia minima de u a v.
    :raises Exception: Si se detecta un ciclo de peso negativo.
    """
    # Paso 1: Agregar un nodo ficticio 'q' conectado a todos con peso 0.
    q = 'q'
    extended_nodes = nodes.copy()
    extended_nodes.append(q)
    extended_edges = edges.copy()
    for node in nodes:
        extended_edges.append((q, node, 0))
    
    # Ejecutar Bellman-Ford desde 'q' para obtener h(v)
    h = bellman_ford(extended_nodes, extended_edges,                 q)
    if h is None:
        raise Exception("El grafo contiene un ciclo de peso negativo. Johnson no se puede aplicar.")
    
    # Reponderar las aristas: w'(u, v) = w(u, v) + h[u] - h[v]
    reweighted_edges = []
    for u, v, w in edges:
        new_weight = w + h[u] - h[v]
        reweighted_edges.append((u, v, new_weight))
    
    # Construir grafo reponderado en formato de lista de adyacencia
    graph = { node: [] for node in nodes }
    for u, v, w in reweighted_edges:
        graph[u].append((v, w))
    
    # Ejecutar Dijkstra desde cada nodo
    distances = {}
    for u in nodes:
        d = dijkstra(nodes, graph, u)
        distances[u] = {}
        # Revertir la reponderación: d(u, v) = d'(u, v) + h[v] - h[u]
        for v in nodes:
            if d[v] == float('inf'):
                distances[u][v] = float('inf')
            else:
                distances[u][v] = d[v] + h[v] - h[u]
    return distances
