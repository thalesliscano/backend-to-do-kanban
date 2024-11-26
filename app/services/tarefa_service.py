from ..models import conectar_bd

class TarefaService:
    @staticmethod
    def criar_tarefa(board_id, title, description, status):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (board_id, task_id, title, description, status) VALUES (?, NULL, ?, ?, ?)",
            (board_id, title, description, status)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def listar_tarefas_por_board(board_id):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE board_id = ?", (board_id,))
        tarefas = cursor.fetchall()
        conn.close()

        return [
            {
                'id': tarefa[0],
                'board_id': tarefa[1],
                'task_id': tarefa[2],
                'title': tarefa[3],
                'description': tarefa[4],
                'status': tarefa[5],
                'completed_date': tarefa[6]
            }
            for tarefa in tarefas
        ]

    @staticmethod
    def atualizar_tarefa(tarefa_id, novo_status):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (novo_status, tarefa_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def excluir_tarefa(tarefa_id):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (tarefa_id,))
        conn.commit()
        conn.close()
