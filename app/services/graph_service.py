# app/services/graph_service.py
def create_adjacency_matrix(nodes, edges):
    n = len(nodes)
    # Inicializamos la matriz de n x n con ceros
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Creamos un diccionario para mapear el nombre del nodo a su índice
    node_index = { node.get('name'): i for i, node in enumerate(nodes) }
    
    for edge in edges:
        node1 = edge.get('node1')
        node2 = edge.get('node2')
        # Se toma el peso de la arista (por defecto 1)
        weight = int(edge.get('weight', 1))
        
        # Se obtienen los índices usando el nombre
        index1 = node_index.get(node1.get('name'))
        index2 = node_index.get(node2.get('name'))
        
        if index1 is not None and index2 is not None:
            if edge.get('direction', 'directed') == 'directed':
                matrix[index1][index2] = weight
            else:
                # Para aristas no dirigidas se actualiza de forma simétrica
                matrix[index1][index2] = weight
                matrix[index2][index1] = weight
    return matrix
