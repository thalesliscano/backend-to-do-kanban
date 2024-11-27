# board_service.py
from ..models import conectar_bd
from ..services.tarefa_service import TaskService

class BoardService:

    @staticmethod
    def criar_board(user_id, nome_board):
        # Conecte-se ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insira um novo board associado ao usuário
        cursor.execute(
            "INSERT INTO boards (name, user_id) VALUES (?, ?)",
            (nome_board, user_id)
        )
        conn.commit()

        # Obtenha o ID do board recém-criado
        board_id = cursor.lastrowid
        conn.close()

        return {
            'id': board_id,
            'name': nome_board
        }

    @staticmethod
    def buscar_board_com_tarefas_por_usuario(user_id):
        # Conecte-se ao banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Selecione o board associado ao usuário
        cursor.execute(
            "SELECT id, name FROM boards WHERE user_id = ?",
            (user_id,)
        )

        # Obtenha o board associado ao usuário
        board = cursor.fetchone()

        # Feche a conexão com o banco
        conn.close()

        if board:
            # Agora, busque as tarefas associadas a esse board
            tarefas = TaskService.buscar_tarefas_por_usuario(user_id)
            board_info = {
                'id': board[0],
                'name': board[1],
                'tarefas': tarefas if tarefas else []  # Inclui as tarefas ou uma lista vazia se não houver tarefas
            }
            return board_info
        return None

