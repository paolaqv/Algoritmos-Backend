def create_adjacency_matrix(nodes, edges):
    n = len(nodes)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    node_index = { node.get('name'): i for i, node in enumerate(nodes) }
    
    for edge in edges:
        node1 = edge.get('node1')
        node2 = edge.get('node2')
        weight = int(edge.get('weight', 1))
        index1 = node_index.get(node1.get('name'))
        index2 = node_index.get(node2.get('name'))
        
        if index1 is not None and index2 is not None:
            if edge.get('direction', 'directed') == 'directed':
                matrix[index1][index2] = weight
            else:
                matrix[index1][index2] = weight
                matrix[index2][index1] = weight
    return matrix
