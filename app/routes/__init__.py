# app/routes/__init__.py
from flask import Blueprint
from .graph import bp as graph_bp

bp = Blueprint('routes', __name__)
bp.register_blueprint(graph_bp)
