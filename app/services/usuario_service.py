from app.services.auth import gerar_token  # Importando a função para gerar o token
from app.db import conectar_bd  # Mantemos a conexão com o banco de dados

class UsuarioService:
    @staticmethod
    def criar_usuario(nome, email, senha):
        conn = conectar_bd()
        cursor = conn.cursor()

        # Verifica se o e-mail já está em uso
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return {"erro": "E-mail já em uso"}
        
        # Cria o usuário
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (nome, email, senha)
        )
        user_id = cursor.lastrowid  # ID do usuário recém-criado

        # Cria o board padrão para o usuário
        cursor.execute(
            "INSERT INTO boards (user_id, name) VALUES (?, ?)",
            (user_id, f"Board do {nome}")
        )

        conn.commit()
        conn.close()

        return {
            "mensagem": "Usuário criado com sucesso",
            "usuario": {"id": user_id, "name": nome, "email": email}
        }

    @staticmethod
    def login(email, senha):
        conn = conectar_bd()  # Conectando ao banco de dados
        cursor = conn.cursor()

        # Verificar se o usuário existe e se a senha está correta
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            # Gerar o token para o usuário com a função gerar_token
            token = gerar_token(usuario[0])  # Considerando que o ID do usuário está na primeira posição (indice 0)
            return usuario, token  # Retorna o usuário e o token gerado
        
        return None, None  # Se as credenciais forem inválidas
