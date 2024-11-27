import sqlite3
from ..models import conectar_bd
from app.services.auth import AuthService  # Corrigido
class UsuarioService:
    
    @staticmethod
    def criar_usuario(nome, email, senha):
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Verifica se o e-mail já está em uso
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return {'erro': 'E-mail já em uso'}
        
        # Insere o novo usuário
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (nome, email, senha)
        )
        conn.commit()
        
        # Retorna o ID do usuário recém-criado
        user_id = cursor.lastrowid
        conn.close()
        
        return {
            'usuario': {
                'id': user_id,
                'name': nome,
                'email': email
            }
        }

    @staticmethod
    def login(email, senha):
        conn = conectar_bd()  # Conectar ao banco de dados
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, senha))
        usuario = cursor.fetchone()  # Pega o primeiro resultado que corresponde

        conn.close()

        if usuario:
            return {
                'id': usuario[0],  # Ajuste conforme necessário
                'name': usuario[1],
                'email': usuario[2],
                'board': {
                    'id': usuario[3],  # O board pode estar em outro campo
                    'name': 'Board de ' + usuario[1]  # Exemplo de board associado
                }
            }
        return None

    @staticmethod
    def buscar_todos_usuarios():
        conn = conectar_bd()
        cursor = conn.cursor()

        # Buscar todos os usuários
        cursor.execute("SELECT id, name, email FROM users")
        usuarios = cursor.fetchall()
        conn.close()

        if usuarios:
            return usuarios
        else:
            return None

    @staticmethod
    def buscar_usuario_por_id(user_id):
        conn = conectar_bd()
        cursor = conn.cursor()

        # Buscar o usuário pelo ID
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return usuario  # Retorna o usuário se encontrado
        return None  # Retorna None caso não encontre o usuário
