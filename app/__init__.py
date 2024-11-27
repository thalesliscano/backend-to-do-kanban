import sqlite3
from flask import Flask
from flask_cors import CORS  # Importando o CORS
from flasgger import Swagger
from .routes.usuarios import usuarios_bp
from .routes.tarefas import tarefas_bp

# Função para criar o aplicativo Flask
def create_app():
    app = Flask(__name__)

    # Configuração do CORS para toda a aplicação
    CORS(app, origins=["http://localhost:8080"]) # Permitindo todas as origens (substitua conforme necessário)

    # Configuração do Swagger
    Swagger(app)  # Isso ativa o Swagger UI na URL /apidocs

    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

    # Registrar rotas, blueprints, etc.
    from .routes import usuarios
    app.register_blueprint(usuarios.usuarios_bp)

    # Registrar o blueprint de tarefas
    app.register_blueprint(tarefas_bp)  # Registrando o blueprint de tarefas

    return app