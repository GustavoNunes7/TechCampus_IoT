from flask import Flask
from .config import Config
from .database.database import init_db
from .routes.health import health_bp
from .routes.solicitacoes import solicitacoes_bp
from .routes.tokens import tokens_bp
from .routes.estoque import estoque_bp
from .routes.maquinas import maquinas_bp
from .routes.iot import iot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db()
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(solicitacoes_bp, url_prefix="/api")
    app.register_blueprint(tokens_bp, url_prefix="/api")
    app.register_blueprint(estoque_bp, url_prefix="/api")
    app.register_blueprint(maquinas_bp, url_prefix="/api")
    app.register_blueprint(iot_bp, url_prefix="/api")
    return app
