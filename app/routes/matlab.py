from flask import Blueprint, jsonify
import subprocess
import os

matlab_bp = Blueprint('matlab', __name__)

# Ruta base de los scripts de MATLAB
MATLAB_SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '../matlab_scripts')

@matlab_bp.route('/open_fuzzy', methods=['POST'])
def open_fuzzy():
    try:
        # Ejecuta el script de Fuzzy Logic
        subprocess.Popen([
            "C:\\Program Files\\MATLAB\\R2024a\\bin\\matlab.exe",  # Asegúrate de que "matlab" esté en el PATH
            "-desktop",  # Abre la GUI de MATLAB
            "-r", 
            f"run('{MATLAB_SCRIPTS_DIR}/fuzzy_gui.m');"  # Ejecuta el script
        ], shell=True)
        return jsonify({"status": "Fuzzy Logic GUI abierta"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@matlab_bp.route('/open_laplace', methods=['POST'])
def open_laplace():
    # Similar a open_fuzzy, pero con el script de Laplace
    try:
        subprocess.Popen([
            "C:\\Program Files\\MATLAB\\R2024a\\bin\\matlab.exe",
            "-desktop",
            "-r",
            f"run('{MATLAB_SCRIPTS_DIR}/laplace_gui.m');"
        ], shell=True)
        return jsonify({"status": "Laplace GUI abierta"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@matlab_bp.route('/open_ilaplace', methods=['POST'])
def open_ilaplace():
    # Similar a open_fuzzy, pero con el script de Inverse Laplace
    try:
        subprocess.Popen([
            "C:\\Program Files\\MATLAB\\R2024a\\bin\\matlab.exe",
            "-desktop",
            "-r",
            f"run('{MATLAB_SCRIPTS_DIR}/ilaplace_gui.m');"
        ], shell=True)
        return jsonify({"status": "Inverse Laplace GUI abierta"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500