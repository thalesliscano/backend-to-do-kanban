from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.tarefa_service import TaskService
import jwt

tarefas_bp = Blueprint('tasks', __name__)

# Chave secreta usada para assinar o token
SECRET_KEY = 'sua_chave_secreta_aqui'

# Função para obter o user_id do token JWT
def obter_user_id_do_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})  # Verifica a expiração
        return decoded_token.get("user_id")
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
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
                    'id': 1,  # Exemplo de ID gerado automaticamente
                    'title': 'Nova Tarefa',
                    'description': 'Descrição da tarefa',
                    'user_id': 1,
                    'board_id': 1,
                    'status': 'doing'  # Garantindo que o status seja "doing"
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
    # Pegando os dados da requisição
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'toDo')  # Se o status não for enviado, será 'doing' por padrão
    
    if not title:
        return jsonify({"erro": "Título é obrigatório!"}), 400
    
    # Pegando o token JWT do cabeçalho Authorization
    token = request.headers.get('Authorization')
    if token:
        token = token.split(" ")[1]  # Pega o token depois do "Bearer"
    else:
        return jsonify({"erro": "Token JWT não fornecido!"}), 400

    # Obtendo o user_id a partir do token JWT
    user_id = obter_user_id_do_token(token)
    print(user_id)
    if not user_id:
        return jsonify({"erro": "Token inválido ou expirado!"}), 400

    # Buscar o board associado ao usuário (lógica personalizada)
    board_id = TaskService.obter_board_do_usuario(user_id)
    if not board_id:
        return jsonify({"erro": "Board não encontrado para o usuário!"}), 400

    # Criando a tarefa
    tarefa = TaskService.criar_tarefa(title, description, user_id, board_id, status)
    
    return jsonify(tarefa), 201


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

