import sqlite3
from flask import Flask
from flasgger import Swagger
from .routes.usuarios import usuarios_bp

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('database.db')  # Ou o nome do seu arquivo de banco de dados

# Função para criar o aplicativo Flask
def create_app():
    app = Flask(__name__)

    # Configuração do Swagger
    Swagger(app)  # Isso ativa o Swagger UI na URL /apidocs

    # Configurações do aplicativo
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Registrar rotas, blueprints, etc.
    from .routes import usuarios
    app.register_blueprint(usuarios.usuarios_bp)

    return app
