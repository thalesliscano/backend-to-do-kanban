from ..models import conectar_bd

class BoardService:
    @staticmethod
    def criar_board(user_id, name):
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Insere o novo board
        cursor.execute(
            "INSERT INTO boards (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        conn.commit()
        
        # Retorna o ID e nome do board recém-criado
        board_id = cursor.lastrowid
        conn.close()
        
        return {
            'id': board_id,
            'name': name
        }
