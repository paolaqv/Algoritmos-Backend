from flask import Blueprint, request, jsonify
from app.services.graph_service import create_adjacency_matrix

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/adjacency_matrix', methods=['POST'])
def adjacency_matrix():
    data = request.get_json()
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    matrix = create_adjacency_matrix(nodes, edges)
    
    return jsonify({'matrix': matrix})
