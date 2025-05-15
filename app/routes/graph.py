from flask import Blueprint, request, jsonify
from app.services.graph_service import create_adjacency_matrix
from app.services.johnson_services import johnson 
from app.services.northwest_services import solve_transportation_problem
from app.services.kruskal_services import find_spanning_tree, create_paths

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/adjacency_matrix', methods=['POST'])
def adjacency_matrix():
    data = request.get_json()
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    matrix = create_adjacency_matrix(nodes, edges)
    
    return jsonify({'matrix': matrix})


def convert_infinity_to_null(data):
    if isinstance(data, dict):
        return {k: convert_infinity_to_null(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_infinity_to_null(v) for v in data]
    elif data == float('inf'):
        return None
    return data

@bp.route('/johnson', methods=['POST'])
def johnson_shortest_paths():
    try:
        data = request.get_json()
        nodes = [node['name'] for node in data.get('nodes', [])]
        edges = []

        for edge in data.get('edges', []):
            edges.append((
                edge['node1']['name'],
                edge['node2']['name'],
                float(edge['weight'])
            ))

        result = johnson(nodes, edges)

        if result is None:
            return jsonify({"error": "El grafo contiene un ciclo de peso negativo."}), 400

        result['distances'] = convert_infinity_to_null(result['distances'])
        result['early_times'] = convert_infinity_to_null(result['early_times']) 
        result['late_times'] = convert_infinity_to_null(result['late_times'])

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/northwest', methods=['POST'])
def northwest_solver():
    try:
        data = request.get_json()
        maximize = request.args.get('maximize', 'false').lower() == 'true'

        result = solve_transportation_problem(data, maximize)

        if "error" in result:
            return jsonify({"error": result["error"]}), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/spanning_tree', methods=['POST'])
def spanning_tree():
    data = request.get_json()
    maximize = request.args.get('maximize', 'false').lower() == 'true'

    data_mst = find_spanning_tree(data, maximize)
    paths = create_paths(data_mst)

    return jsonify({"data_mst": data_mst, "paths": paths}), 200
