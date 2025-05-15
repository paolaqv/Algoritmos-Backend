import networkx as nx

### KRUSKAL MST ###

def create_graph(data):
    """
    Construye un grafo NetworkX a partir de:
     • data['nodes']: puede ser dict {id: {...}} o lista [{id, name, …}, …]
     • data['edges']: puede ser dict {eid: {...}} o lista [{id, node1:{…},node2:{…},weight}, …]
    Para lista, usa edge['id'] si existe; si no, genera IDs genéricos e1, e2, …
    """
    G = nx.Graph()

    # Añade nodos
    nodes = data.get('nodes', [])
    if isinstance(nodes, list):
        for node in nodes:
            nid = node.get('name', node.get('id'))
            G.add_node(nid)
    else:
        for node in nodes.values():
            G.add_node(node['id'])

    # Añade aristas
    edges = data.get('edges', [])
    if isinstance(edges, list):
        for i, edge in enumerate(edges, start=1):
            u = edge['node1'].get('name', edge['node1'].get('id'))
            v = edge['node2'].get('name', edge['node2'].get('id'))
            w = int(edge.get('weight', 0))
            # Usa el id original si viene del front; si no, crea uno genérico
            eid = edge.get('id', f"e{i}")
            G.add_edge(u, v, weight=w, id=eid)
    else:
        for eid, edge in edges.items():
            G.add_edge(
                edge['source'],
                edge['target'],
                weight=int(edge['label']),
                id=eid
            )

    return G

def create_data(G):
    """
    Convierte el grafo G en dict de aristas:
      {"edges": { eid: {source, target, label}, … }}
    """
    return {
        "edges": {
            attrs['id']: {
                "source": u,
                "target": v,
                "label": str(attrs['weight'])
            }
            for u, v, attrs in G.edges(data=True)
        }
    }

def find_spanning_tree(data, maximize=False):
    """
    Devuelve el MST (o máximo ST si maximize=True) en el mismo formato de 'edges'.
    """
    G = create_graph(data)
    if maximize:
        T = nx.maximum_spanning_tree(G, weight='weight')
    else:
        T = nx.minimum_spanning_tree(G, weight='weight')
    return create_data(T)

def create_paths(data):
    """
    A partir de {"edges":{eid:…}}, genera rutas individuales:
      {"path1":{"edges":[eid]},…}
    """
    return {
        f"path{i+1}": {"edges": [eid]}
        for i, eid in enumerate(data['edges'].keys())
    }
