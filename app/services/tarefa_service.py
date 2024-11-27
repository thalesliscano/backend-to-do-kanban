from ..models import conectar_bd
# tarefa_services.py
class TaskService:

    @staticmethod
    def criar_tarefa(title, description, user_id, board_id, status):
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Inserir a tarefa no banco de dados, o campo 'id' será gerado automaticamente
        cursor.execute(
            "INSERT INTO tasks (title, description, user_id, board_id, status) VALUES (?, ?, ?, ?, ?)",
            (title, description, user_id, board_id, status)
        )
        conn.commit()
        
        task_id = cursor.lastrowid  # Pega o ID da tarefa recém-criada
        conn.close()
        
        return {
            'task': {
                'id': task_id,  # O ID gerado automaticamente pelo banco de dados
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
        cursor.execute("SELECT id, title, description, status, created_at FROM tasks WHERE user_id = ?", (user_id,))
        tarefas = cursor.fetchall()
        conn.close()

        if tarefas:
            return tarefas
        else:
            return None


# class TarefaService:
#     @staticmethod
#     def criar_tarefa(board_id, titulo, descricao, status, user_id):
#         # Cria a tarefa no banco de dados, associando ao board e ao usuário
#         tarefa = Tarefa(
#             titulo=titulo,
#             descricao=descricao,
#             status=status,
#             board_id=board_id,
#             user_id=user_id  # Associando a tarefa ao usuário autenticado
#         )
#         db.session.add(tarefa)
#         db.session.commit()
#         return tarefa
#     @staticmethod
#     def listar_tarefas_por_board(board_id):
#         conn = conectar_bd()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM tasks WHERE board_id = ?", (board_id,))
#         tarefas = cursor.fetchall()
#         conn.close()

#         return [
#             {
#                 'id': tarefa[0],
#                 'board_id': tarefa[1],
#                 'task_id': tarefa[2],
#                 'title': tarefa[3],
#                 'description': tarefa[4],
#                 'status': tarefa[5],
#                 'completed_date': tarefa[6]
#             }
#             for tarefa in tarefas
#         ]

#     @staticmethod
#     def atualizar_tarefa(tarefa_id, novo_status):
#         conn = conectar_bd()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE tasks SET status = ? WHERE id = ?",
#             (novo_status, tarefa_id)
#         )
#         conn.commit()
#         conn.close()

#     @staticmethod
#     def excluir_tarefa(tarefa_id):
#         conn = conectar_bd()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM tasks WHERE id = ?", (tarefa_id,))
#         conn.commit()
#         conn.close()

#     # Método para contar tarefas por status
#     @staticmethod
#     def contar_tarefas_por_status(board_id):
#         conn = conectar_bd()
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT status, COUNT(*) FROM tasks WHERE board_id = ? GROUP BY status", (board_id,))
#         resultado = cursor.fetchall()
        
#         conn.close()

#         # Retorna um dicionário com as contagens
#         contagens = {status: count for status, count in resultado}
#         return contagens
#     @staticmethod
#     def login(email, senha):
#         conn = conectar_bd()  # Conectando ao banco de dados
#         cursor = conn.cursor()

#         # Verifica se o usuário existe e a senha está correta
#         cursor.execute("SELECT id, name, email FROM users WHERE email = ? AND password = ?", (email, senha))
#         usuario = cursor.fetchone()  # Retorna a tupla com os dados do usuário
        
#         conn.close()

#         if usuario:
#             # Retorna um dicionário
#             return {
#                 'id': usuario[0],
#                 'name': usuario[1],
#                 'email': usuario[2]
#             }
#         return None  # Login falhou
