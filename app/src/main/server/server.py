from flask import Flask
from src.main.routes.user_routes import user_routes_bp
from src.main.routes.empresa_routes import empresa_routes_bp
from src.main.routes.produto_routes import produto_routes_bp
from src.main.routes.pedido_routes import pedido_routes_bp
from src.models.settings.db_connection_handler import db_connection_handler



def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_routes_bp)
    app.register_blueprint(empresa_routes_bp)
    app.register_blueprint(produto_routes_bp)
    app.register_blueprint(pedido_routes_bp)


    db_connection_handler.connect()

    return app