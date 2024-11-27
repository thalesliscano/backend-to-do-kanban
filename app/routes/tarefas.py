from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.tarefa_service import TaskService
import jwt
from ..models import conectar_bd



tarefas_bp = Blueprint('tasks', __name__)

# Chave secreta usada para assinar o token
SECRET_KEY = 'sua_chave_secreta_aqui'

# Função para obter o user_id do token JWT
def obter_user_id_do_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})  # Verifica a expiração
        return decoded_token.get("user_id")
    except jwt.ExpiredSignatureError:
        print("Erro: Token expirado!")
        return None  # Token expirado
    except jwt.InvalidTokenError:
        print("Erro: Token inválido!")
        return None  # Token inválido


@tarefas_bp.route('/tasks', methods=['POST'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Cria uma nova tarefa associada a um board de um usuário autenticado',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Token JWT para autenticação',
            'required': True
        },
        {
            'name': 'tarefa',
            'in': 'body',
            'type': 'object',
            'required': True,
            'properties': {
                'title': {'type': 'string', 'description': 'Título da tarefa'},
                'description': {'type': 'string', 'description': 'Descrição da tarefa'},
                'status': {'type': 'string', 'enum': ['toDo', 'doing', 'done'], 'default': 'toDo', 'description': 'Status da tarefa'}
            },
            'example': {
                'title': 'Nova Tarefa',
                'description': 'Descrição da tarefa'
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Tarefa criada com sucesso',
            'examples': {
                'application/json': {
                    'id': 1,
                    'title': 'Nova Tarefa',
                    'description': 'Descrição da tarefa',
                    'user_id': 1,
                    'board_id': 1,
                    'status': 'doing'
                }
            }
        },
        '400': {
            'description': 'Campos obrigatórios ausentes',
            'examples': {
                'application/json': {'erro': 'Campos obrigatórios ausentes!'}
            }
        }
    }
})
def criar_tarefa():
    try:
        # Pegando os dados da requisição
        data = request.get_json()
        print("Dados recebidos:", data)

        title = data.get('title')
        description = data.get('description')
        status = data.get('status', 'toDo')  # Se o status não for enviado, será 'doing' por padrão

        if not title:
            print("Erro: Título não fornecido!")
            return jsonify({"erro": "Título é obrigatório!"}), 400

        # Pegando o token JWT do cabeçalho Authorization
        token = request.headers.get('Authorization')
        print("Token recebido:", token)
        if token:
            token = token.split(" ")[1]  # Pega o token depois do "Bearer"
        else:
            print("Erro: Token não fornecido!")
            return jsonify({"erro": "Token JWT não fornecido!"}), 400

        # Obtendo o user_id a partir do token JWT
        user_id = obter_user_id_do_token(token)
        print("User ID decodificado:", user_id)
        if not user_id:
            print("Erro: Token inválido ou expirado!")
            return jsonify({"erro": "Token inválido ou expirado!"}), 400

        # Buscar o board associado ao usuário
        board_id = TaskService.obter_board_do_usuario(user_id)
        print("Board ID associado:", board_id)
        if not board_id:
            print("Erro: Nenhum board encontrado para o usuário!")
            return jsonify({"erro": "Board não encontrado para o usuário!"}), 400

        # Criando a tarefa
        tarefa = TaskService.criar_tarefa(title, description, user_id, board_id, status)
        print("Tarefa criada:", tarefa)

        return jsonify(tarefa), 201

    except Exception as e:
        print("Erro inesperado:", str(e))
        return jsonify({"erro": "Erro interno do servidor!"}), 500

@tarefas_bp.route('/tasks', methods=['GET'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Busca as tarefas associadas a um usuário',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'integer',
            'description': 'ID do usuário para filtrar as tarefas',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'Lista de tarefas encontradas',
            'examples': {
                'application/json': [
                    {'title': 'Tarefa 1', 'description': 'Descrição da tarefa 1', 'user_id': 1, 'board_id': 1},
                    {'title': 'Tarefa 2', 'description': 'Descrição da tarefa 2', 'user_id': 1, 'board_id': 2}
                ]
            }
        },
        '400': {
            'description': 'user_id é necessário',
            'examples': {
                'application/json': {'erro': 'user_id é necessário!'}
            }
        },
        '404': {
            'description': 'Nenhuma tarefa encontrada',
            'examples': {
                'application/json': {'erro': 'Nenhuma tarefa encontrada!'}
            }
        }
    }
})
def buscar_tarefas():
    # Pegando o user_id da requisição
    user_id = request.args.get('user_id')  # Você pode pegar isso do token JWT ou como parâmetro
    
    if not user_id:
        return jsonify({"erro": "user_id é necessário!"}), 400
    
    tarefas = TaskService.buscar_tarefas_por_usuario(user_id)
    
    if tarefas:
        return jsonify(tarefas), 200
    else:
        return jsonify({"erro": "Nenhuma tarefa encontrada!"}), 404

@tarefas_bp.route('/tasks/<int:user_task_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Atualiza o status de uma tarefa existente',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Token JWT para autenticação',
            'required': True
        },
        {
            'name': 'user_task_id',
            'in': 'path',
            'type': 'integer',
            'description': 'ID da tarefa a ser atualizada',
            'required': True
        },
        {
            'name': 'status',
            'in': 'body',
            'type': 'string',
            'enum': ['toDo', 'doing', 'done'],
            'description': 'Novo status da tarefa',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'Status da tarefa atualizado com sucesso',
            'examples': {
                'application/json': {
                    'user_task_id': 1,
                    'title': 'Nova Tarefa',
                    'description': 'Descrição da tarefa',
                    'status': 'done',
                    'user_id': 1,
                    'board_id': 1
                }
            }
        },
        '400': {
            'description': 'Campos obrigatórios ausentes',
            'examples': {
                'application/json': {'erro': 'Status é obrigatório!'}
            }
        },
        '404': {
            'description': 'Tarefa não encontrada',
            'examples': {
                'application/json': {'erro': 'Tarefa não encontrada!'}
            }
        }
    }
})
def editar_tarefa_status(user_task_id):
    try:
        # Pegando os dados da requisição
        data = request.get_json()
        status = data.get('status')

        if not status:
            return jsonify({"erro": "Status é obrigatório!"}), 400

        # Pegando o token JWT do cabeçalho Authorization
        token = request.headers.get('Authorization')
        if token:
            token = token.split(" ")[1]  # Pega o token depois do "Bearer"
        else:
            return jsonify({"erro": "Token JWT não fornecido!"}), 400

        # Obtendo o user_id a partir do token JWT
        user_id = obter_user_id_do_token(token)
        if not user_id:
            return jsonify({"erro": "Token inválido ou expirado!"}), 400

        # Buscar a tarefa no banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_task_id = ? AND user_id = ?", (user_task_id, user_id))
        tarefa = cursor.fetchone()

        if not tarefa:
            return jsonify({"erro": "Tarefa não encontrada!"}), 404

        # Atualizar o status da tarefa
        cursor.execute("UPDATE tasks SET status = ? WHERE user_task_id = ?", (status, user_task_id))
        conn.commit()
        conn.close()

        # Retornar a tarefa atualizada
        return jsonify({
            'user_task_id': user_task_id,
            'title': tarefa[1],
            'description': tarefa[2],
            'status': status,
            'user_id': tarefa[3],
            'board_id': tarefa[4]
        }), 200

    except Exception as e:
        print(f"Erro: {str(e)}")  # Imprime o erro no terminal
        return jsonify({"erro": "Erro interno do servidor!"}), 500



@tarefas_bp.route('/tasks/<int:user_task_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Exclui uma tarefa existente',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'description': 'Token JWT para autenticação',
            'required': True
        },
        {
            'name': 'user_task_id',
            'in': 'path',
            'type': 'integer',
            'description': 'ID da tarefa a ser excluída',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'Tarefa excluída com sucesso',
            'examples': {
                'application/json': {'message': 'Tarefa excluída com sucesso!'}
            }
        },
        '400': {
            'description': 'Token não fornecido ou inválido',
            'examples': {
                'application/json': {'erro': 'Token JWT não fornecido ou inválido!'}
            }
        },
        '404': {
            'description': 'Tarefa não encontrada',
            'examples': {
                'application/json': {'erro': 'Tarefa não encontrada!'}
            }
        }
    }
})
def excluir_tarefa(user_task_id):
    try:
        # Pegando o token JWT do cabeçalho Authorization
        token = request.headers.get('Authorization')
        if token:
            token = token.split(" ")[1]  # Pega o token depois do "Bearer"
        else:
            return jsonify({"erro": "Token JWT não fornecido!"}), 400

        # Obtendo o user_id a partir do token JWT
        user_id = obter_user_id_do_token(token)
        if not user_id:
            return jsonify({"erro": "Token inválido ou expirado!"}), 400

        # Buscar a tarefa no banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_task_id = ? AND user_id = ?", (user_task_id, user_id))
        tarefa = cursor.fetchone()

        if not tarefa:
            return jsonify({"erro": "Tarefa não encontrada!"}), 404

        # Excluir a tarefa do banco de dados
        cursor.execute("DELETE FROM tasks WHERE user_task_id = ? AND user_id = ?", (user_task_id, user_id))
        conn.commit()
        conn.close()

        # Retornar sucesso
        return jsonify({"message": "Tarefa excluída com sucesso!"}), 200

    except Exception as e:
        print(f"Erro: {str(e)}")  # Imprime o erro no terminal
        return jsonify({"erro": "Erro interno do servidor!"}), 500
