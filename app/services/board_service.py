from ..models import conectar_bd

# board_service.py

class BoardService:

    @staticmethod
    def criar_board(user_id, nome_board):
        # Conecte-se ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insira um novo board com o nome e associado ao usuário
        cursor.execute(
            "INSERT INTO boards (name, user_id) VALUES (?, ?)",
            (nome_board, user_id)
        )
        conn.commit()

        # Retorna o board criado com seu ID
        board_id = cursor.lastrowid
        conn.close()

        return {
            'id': board_id,
            'name': nome_board
        }
