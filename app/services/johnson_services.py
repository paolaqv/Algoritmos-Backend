import heapq
from collections import defaultdict, deque

def bellman_ford(nodes, edges, source):
    dist = {node: float('inf') for node in nodes}
    dist[source] = 0

    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None
    return dist

def calculate_h_values(nodes, edges):
    q = 'q'
    extended_nodes = nodes + [q]
    extended_edges = edges + [(q, node, 0) for node in nodes]
    
    h = bellman_ford(extended_nodes, extended_edges, q)
    if h is None:
        raise Exception("El grafo contiene un ciclo de peso negativo. Johnson no se puede aplicar.")

    # Eliminamos el nodo ficticio `q` del resultado
    del h[q]
    return h

def dijkstra(nodes, graph, source):
    dist = {node: float('inf') for node in nodes}
    dist[source] = 0
    heap = [(0, source)]
    paths = {node: [] for node in nodes}

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
                paths[v] = paths[u] + [u]

    return dist, paths

def calculate_early_times(nodes, graph):
    early_times = {node: 0 for node in nodes}
    for u in nodes:
        for v, w in graph.get(u, []):
            early_times[v] = max(early_times[v], early_times[u] + w)
    return early_times

def calculate_late_times(nodes, edges, early_times, final_node):
    late_times = {node: float('inf') for node in nodes}
    late_times[final_node] = early_times[final_node]

    reversed_edges = defaultdict(list)
    for u, v, w in edges:
        reversed_edges[v].append((u, w))
    
    queue = deque([final_node])
    
    while queue:
        current_node = queue.popleft()
        
        for prev_node, weight in reversed_edges[current_node]:
            if late_times[current_node] - weight < late_times[prev_node]:
                late_times[prev_node] = late_times[current_node] - weight
                queue.append(prev_node)
    
    return late_times

def find_critical_path(early_times, late_times):
    return [node for node in early_times if early_times[node] == late_times[node]]

def johnson(nodes, edges):
    # Calcular valores de h usando Bellman-Ford
    h = calculate_h_values(nodes, edges)

    # Reponderar las aristas usando los valores h
    reweighted_edges = []
    for u, v, w in edges:
        new_weight = w + h[u] - h[v]
        reweighted_edges.append((u, v, new_weight))

    graph = defaultdict(list)
    for u, v, w in reweighted_edges:
        graph[u].append((v, w))

    # Calcular los tiempos tempranos y tardíos
    early_times = calculate_early_times(nodes, graph)
    final_node = max(early_times, key=early_times.get)
    late_times = calculate_late_times(nodes, edges, early_times, final_node)
    critical_path = find_critical_path(early_times, late_times)

    edges_data = {}
    for index, (u, v, w) in enumerate(edges, 1):
        edge_id = f"edge{index}"
        early_start = early_times[u]
        early_finish = early_start + w
        late_start = late_times[v] - w if late_times[v] != float('inf') else None
        late_finish = late_times[v] if late_times[v] != float('inf') else None

        # Calcular el h correcto para cada arista
        h_value = late_times[v] - early_times[u] - w

        edges_data[edge_id] = {
            "source": u,
            "target": v,
            "label": f"{w}\n h= {h_value}",
            "earlyStart": early_start,
            "earlyFinish": early_finish,
            "lateStart": late_start,
            "lateFinish": late_finish
        }

    return {
        "distances": graph,
        "h_values": h,
        "critical_path": critical_path,
        "early_times": early_times,
        "late_times": late_times,
        "edges": edges_data
    }
