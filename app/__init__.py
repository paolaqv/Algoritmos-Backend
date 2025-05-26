from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    CORS(app, resources={r"/graph/*": {"origins": "http://localhost:5173"}})


    # db.init_app(app)
    # migrate.init_app(app, db)

    # las rutas definidas en routes
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Blueprint de MATLAB
    from .routes.matlab import matlab_bp  # Importa el blueprint
    app.register_blueprint(matlab_bp, url_prefix='/api/matlab')  # Registra

    # Ruta para renderizar el HTML
    @app.route('/matlab')
    def matlab_launcher():
        try:
            return render_template('matlab_gui.html')
        except Exception as e:
            return f"Error en Flask: {str(e)}", 500  # Debug de errores

    if __name__ == '__main__':
        app.run(debug=True)  # ¡Ejecuta en modo debug!
    return app