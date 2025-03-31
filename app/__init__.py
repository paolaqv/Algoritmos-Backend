from flask import Flask
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

    return app