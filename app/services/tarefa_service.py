from ..models import conectar_bd

class TaskService:

    @staticmethod
    def criar_tarefa(title, description, user_id, board_id, status):
        conn = conectar_bd()
        cursor = conn.cursor()

        # Obter o maior user_task_id para o usuário específico
        cursor.execute("SELECT MAX(user_task_id) FROM tasks WHERE user_id = ?", (user_id,))
        max_user_task_id = cursor.fetchone()[0]
        
        # Se o usuário ainda não tiver tarefas, inicia com user_task_id 1
        if max_user_task_id is None:
            user_task_id = 1
        else:
            user_task_id = max_user_task_id + 1  # Incrementa o maior user_task_id encontrado

        # Inserir a tarefa no banco de dados
        cursor.execute(
            "INSERT INTO tasks (user_task_id, title, description, user_id, board_id, status) VALUES (?, ?, ?, ?, ?, ?)",
            (user_task_id, title, description, user_id, board_id, status)
        )
        conn.commit()

        conn.close()

        return {
            'task': {
                'user_task_id': user_task_id,  # O ID específico do usuário
                'title': title,
                'description': description,
                'status': status,
                'user_id': user_id,
                'board_id': board_id
            }
        }

    @staticmethod
    def buscar_tarefas_por_usuario(user_id):
        conn = conectar_bd()
        cursor = conn.cursor()

        # Buscar todas as tarefas de um usuário específico
        cursor.execute("SELECT user_task_id, title, description, status, created_at FROM tasks WHERE user_id = ?", (user_id,))
        tarefas = cursor.fetchall()
        conn.close()

        # Se tarefas forem encontradas, converta para um formato de lista de dicionários
        if tarefas:
            tarefas_formatadas = [
                {
                    'user_task_id': tarefa[0],
                    'title': tarefa[1],
                    'description': tarefa[2],
                    'status': tarefa[3],
                    'created_at': tarefa[4]
                } for tarefa in tarefas
            ]
            return tarefas_formatadas
        else:
            return None

    @staticmethod
    def obter_board_do_usuario(user_id):
        """
        Busca o ID do board associado ao usuário.
        """
        conn = conectar_bd()
        cursor = conn.cursor()

        # Supondo que a tabela 'boards' associa boards aos usuários
        cursor.execute("SELECT id FROM boards WHERE user_id = ?", (user_id,))
        board = cursor.fetchone()
        conn.close()

        if board:
            return board[0]  # Retorna o ID do board
        return None  # Retorna None se nenhum board for encontrado
