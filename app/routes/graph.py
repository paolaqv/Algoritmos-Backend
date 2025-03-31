from flask import Blueprint, request, jsonify
from app.services.graph_service import create_adjacency_matrix
from app.services.johnson_services import johnson 

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/adjacency_matrix', methods=['POST'])
def adjacency_matrix():
    data = request.get_json()
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    matrix = create_adjacency_matrix(nodes, edges)
    
    return jsonify({'matrix': matrix})

@bp.route('/johnson', methods=['POST'])
def johnson_shortest_paths():
    """
    Endpoint para ejecutar el algoritmo de Johnson y obtener los caminos más cortos
    entre todos los pares de nodos.
    
    Se espera recibir un JSON con:
      - nodes: Lista de nodos, cada uno con al menos el atributo 'name'.
      - edges: Lista de aristas en el siguiente formato:
          {
              "node1": { "name": "A" },
              "node2": { "name": "B" },
              "weight": 4,
              "direction": "directed"  // o "undirected"
          }
    """
    data = request.get_json()
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    
    # Formateamos las aristas: convertimos cada arista a una tupla (u, v, peso)
    formatted_edges = []
    for edge in edges:
        node1 = edge.get('node1')
        node2 = edge.get('node2')
        # Convertir el peso a float para admitir negativos y decimales
        weight = float(edge.get('weight', 1))
        formatted_edges.append((node1.get('name'), node2.get('name'), weight))
    
    # Extraemos la lista de nombres de nodos
    node_names = [node.get('name') for node in nodes]
    
    try:
        distances = johnson(node_names, formatted_edges)
        return jsonify({'distances': distances})
    except Exception as e:
        return jsonify({'error': str(e)}), 400