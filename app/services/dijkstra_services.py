import networkx as nx
from collections import deque
import heapq
from typing import Dict, List, Optional
from app.services.kruskal_services import create_paths

def vertices_edges_to_adjacency_list(VEGraph: Dict) -> Dict[str, Dict]:
    """
    Acepta VEGraph con:
      • 'nodes': lista [{id, name, …}, …] o dict {id: {...}, …}
      • 'edges': lista [{id?, node1:{…}, node2:{…}, weight}, …] o dict {id: {...}, …}
    Devuelve lista de adyacencia:
      { nodeId: {"name":…, "neighbors":{neighborId:{"edgeId", "label"},…}}, … }
    """
    # 1) Unifica nodos en dict nodeId→node
    raw_nodes = VEGraph.get('nodes', {})
    if isinstance(raw_nodes, list):
        nodes_dict = {
            node.get('name', node.get('id')): node
            for node in raw_nodes
        }
    else:
        nodes_dict = raw_nodes

    adjacency: Dict[str, Dict] = {
        node_id: {"name": node.get('name', node_id), "neighbors": {}}
        for node_id, node in nodes_dict.items()
    }

    # 2) Unifica aristas en dict edgeId→edge
    raw_edges = VEGraph.get('edges', {})
    if isinstance(raw_edges, list):
        edges_dict = {}
        for i, edge in enumerate(raw_edges, start=1):
            eid = edge.get('id', f"e{i}")
            # extrae source/target de node1/node2
            src = edge['node1'].get('name', edge['node1'].get('id'))
            tgt = edge['node2'].get('name', edge['node2'].get('id'))
            label = edge.get('weight', 0)
            edges_dict[eid] = {"source": src, "target": tgt, "label": label}
    else:
        edges_dict = raw_edges

    # 3) Rellena neighbors
    for eid, edge in edges_dict.items():
        label = edge.get('label', 0)
        if isinstance(label, str):
            label = int(label)
        src = edge['source']
        tgt = edge['target']
        adjacency[src]['neighbors'][tgt] = {"edgeId": eid, "label": label}
    return adjacency

def dijkstra(
    graph: Dict[str, Dict],
    start: str,
    maximize: bool = False
) -> Dict[str, Dict]:
    inf = float('-inf') if maximize else float('inf')
    dist = {n: inf for n in graph}
    dist[start] = 0
    paths = {n: [] for n in graph}
    visited = set()

    heap = [(-0 if maximize else 0, start)]  # (distance, node)

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        curr_dist = -curr_dist if maximize else curr_dist

        for v, meta in graph[u]['neighbors'].items():
            weight = meta['label']
            nd = curr_dist + weight
            if (maximize and nd > dist[v]) or (not maximize and nd < dist[v]):
                dist[v] = nd
                paths[v] = paths[u] + [meta['edgeId']]
                heapq.heappush(heap, (-nd if maximize else nd, v))

    # Marcar no alcanzables
    for n in graph:
        if dist[n] == inf or dist[n] == -inf:
            dist[n] = -1

    return {n: {"distance": dist[n], "path": paths[n]} for n in graph}

def dijkstra_with_paths(
    VEGraph: Dict,
    start: str,
    end: Optional[str] = None,
    maximize: bool = False
) -> Dict:
    """
    Orquesta Dijkstra:
      • vertices_edges_to_adjacency_list acepta el formato de front.
      • dijkstra calcula distancias y paths.
      • Si se pasa `end`, añade `targetPath` con create_paths().
    """
    adj = vertices_edges_to_adjacency_list(VEGraph)
    result = dijkstra(adj, start, maximize)
    response = {"nodes": result}

    if end and end in result:
        # create_paths espera {"edges":{eid:…}}
        response["targetPath"] = create_paths(
            {"edges": {eid: 0 for eid in result[end]["path"]}}
        )

    return response
