from flask import Flask, jsonify
from .config import Config
from .database.database import init_db
from .routes.health import health_bp
from .routes.solicitacoes import solicitacoes_bp
from .routes.tokens import tokens_bp
from .routes.estoque import estoque_bp
from .routes.maquinas import maquinas_bp
from .routes.iot import iot_bp
from .routes.painel import painel_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        init_db()

    @app.get("/api/")
    def api_inicio():
        return {"servico": "TechCampus IoT", "status": "online", "painel": "/"}

    @app.get("/")
    def inicio():
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TechCampus IoT</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    min-height: 100vh;
                    font-family: Arial, sans-serif;
                    background: #080b10;
                    color: #f5f7fa;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 24px;
                }
                .container {
                    width: 100%;
                    max-width: 900px;
                    background: #101722;
                    border: 1px solid #1d2a3a;
                    border-radius: 18px;
                    padding: 36px;
                    box-shadow: 0 20px 60px rgba(0,0,0,.35);
                }
                h1 { margin: 0 0 8px; }
                .subtitle { color: #aeb9c8; margin-bottom: 28px; }
                .status {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 12px;
                    border-radius: 999px;
                    background: #12301f;
                    color: #7ee2a8;
                    margin-bottom: 28px;
                }
                .dot {
                    width: 9px;
                    height: 9px;
                    border-radius: 50%;
                    background: #39d353;
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                    gap: 14px;
                }
                a {
                    display: block;
                    padding: 18px;
                    border: 1px solid #26364a;
                    border-radius: 12px;
                    color: #f5f7fa;
                    text-decoration: none;
                    background: #0d131c;
                    transition: .2s;
                }
                a:hover {
                    transform: translateY(-2px);
                    border-color: #3d6ea8;
                    background: #121c29;
                }
                .name { font-weight: bold; margin-bottom: 6px; }
                .path { color: #7f91a8; font-size: 14px; }
                footer {
                    margin-top: 28px;
                    color: #718096;
                    font-size: 13px;
                }
            </style>
        </head>
        <body>
            <main class="container">
                <h1>TechCampus IoT</h1>
                <p class="subtitle">Servidor Python responsável pela camada IoT do TechCampus.</p>

                <div class="status">
                    <span class="dot"></span>
                    Servidor online
                </div>

                <h2>API</h2>

                <div class="grid">
                    <a href="/api/health">
                        <div class="name">Saúde do servidor</div>
                        <div class="path">GET /api/health</div>
                    </a>

                    <a href="/api/estoque">
                        <div class="name">Estoque</div>
                        <div class="path">GET /api/estoque</div>
                    </a>

                    <a href="/api/maquinas">
                        <div class="name">Máquinas</div>
                        <div class="path">GET /api/maquinas</div>
                    </a>

                    <a href="/api/tokens/">
                        <div class="name">Tokens</div>
                        <div class="path">GET /api/tokens/&lt;token&gt;</div>
                    </a>
                </div>

                <footer>
                    TechCampus IoT • Flask + SQLite • API para integração com ESP8266
                </footer>
            </main>
        </body>
        </html>
        """

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(solicitacoes_bp, url_prefix="/api")
    app.register_blueprint(tokens_bp, url_prefix="/api")
    app.register_blueprint(estoque_bp, url_prefix="/api")
    app.register_blueprint(maquinas_bp, url_prefix="/api")
    app.register_blueprint(iot_bp, url_prefix="/api")
    app.register_blueprint(painel_bp)

    return app
