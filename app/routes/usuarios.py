from flask import Blueprint, request, jsonify
from flasgger import swag_from
from functools import wraps
from ..services.usuario_service import UsuarioService
from ..services.board_service import BoardService
from app.services.auth import AuthService  # Corrigido

# Defina o decorador antes de usá-lo
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'erro': 'Token de autenticação não fornecido'}), 401
        
        token = token.split(" ")[1] if " " in token else token  # Remove "Bearer " do cabeçalho
        user_id = AuthService.validar_token(token)
        if not user_id:
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
        
        # Passa o user_id para a função protegida
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    return decorated

# Agora, defina as rotas normalmente
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Cria um novo usuário no sistema e um board padrão associado',
    'parameters': [
        {
            'name': 'usuario',
            'in': 'body',
            'type': 'object',
            'required': True,
            'properties': {
                'name': {'type': 'string', 'description': 'Nome do usuário'},
                'email': {'type': 'string', 'description': 'E-mail do usuário (deve ser único)'},
                'password': {'type': 'string', 'description': 'Senha do usuário'}
            },
            'example': {
                'name': 'João',
                'email': 'joao@exemplo.com',
                'password': 'senha123'
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Usuário e board padrão criados com sucesso',
            'examples': {
                'application/json': {
                    'mensagem': 'Usuário criado com sucesso',
                    'usuario': {'id': 1, 'name': 'João', 'email': 'joao@exemplo.com'},
                    'board': {'id': 1, 'name': 'Meu Board Padrão'}
                }
            }
        },
        '400': {
            'description': 'Erro ao criar usuário',
            'examples': {
                'application/json': {'erro': 'E-mail já em uso'}
            }
        }
    }
})
def criar_usuario():
    dados = request.json
    nome = dados.get('name')
    email = dados.get('email')
    senha = dados.get('password')
    
    if not nome or not email or not senha:
        return {"error": "Campos 'name', 'email' e 'password' são obrigatórios"}, 400

    resposta = UsuarioService.criar_usuario(nome, email, senha)
    
    if 'erro' in resposta:
        return jsonify(resposta), 400
    
    # Cria o board padrão
    user_id = resposta['usuario']['id']  # Obter ID do usuário criado
    board = BoardService.criar_board(user_id, 'Meu Board Padrão')
    
    return jsonify({
        'mensagem': 'Usuário criado com sucesso',
        'usuario': resposta['usuario'],
        'board': board
    }), 201

@usuarios_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Rota de login para autenticação do usuário',
    'parameters': [
        {
            'name': 'usuario',
            'in': 'body',
            'type': 'object',
            'required': True,
            'properties': {
                'email': {
                    'type': 'string',
                    'description': 'E-mail do usuário'
                },
                'password': {
                    'type': 'string',
                    'description': 'Senha do usuário'
                }
            },
            'example': {
                'email': 'joao@exemplo.com',
                'password': 'senha123'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Login bem-sucedido',
            'examples': {
                'application/json': {
                    'mensagem': 'Login bem-sucedido',
                    'token': 'exemplo_de_token_gerado_aqui'  # Apenas o token será retornado
                }
            }
        },
        '401': {
            'description': 'Credenciais inválidas',
            'examples': {
                'application/json': {'erro': 'Credenciais inválidas'}
            }
        }
    }
})
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('password')

    if not email or not senha:
        return jsonify({'erro': 'Campos "email" e "password" são obrigatórios'}), 400

    usuario = UsuarioService.login(email, senha)

    if not usuario:
        return jsonify({'erro': 'Credenciais inválidas'}), 401  # Caso o login falhe

    # Verifique se o retorno contém as informações esperadas
    if not isinstance(usuario, dict) or not all(key in usuario for key in ['id', 'name', 'email']):
        return jsonify({'erro': 'Erro no formato dos dados retornados'}), 500

    # Gera o token JWT
    token = AuthService.gerar_token(usuario['id'])
    if not token:
        return jsonify({'erro': 'Erro ao gerar o token'}), 500

    # Responde apenas com a mensagem de sucesso e o token
    return jsonify({
        'mensagem': 'Login bem-sucedido',
        'token': token  # Apenas o token será retornado
    }), 200

@usuarios_bp.route('/usuarios', methods=['GET'])
@token_required  # Protege o endpoint com a autenticação
@swag_from({
    'tags': ['Usuários'],
    'description': 'Retorna os dados do usuário logado com o board associado',
    'responses': {
        '200': {
            'description': 'Usuário encontrado com board associado',
            'examples': {
                'application/json': {
                    'usuario': {'id': 1, 'name': 'João', 'email': 'joao@exemplo.com', 'board': {'id': 1, 'name': 'Meu Board Padrão'}}
                }
            }
        },
        '404': {
            'description': 'Usuário não encontrado',
            'examples': {
                'application/json': {'erro': 'Usuário não encontrado'}
            }
        }
    }
})
def buscar_usuario_logado(user_id):
    # Buscar o usuário pelo ID (utilizando o user_id extraído do token)
    usuario = UsuarioService.buscar_usuario_por_id(user_id)

    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    # Buscar o board associado ao usuário
    board = BoardService.buscar_board_por_usuario(user_id)

    # Retornar os dados do usuário com o board
    usuario_dict = {
        'id': usuario[0],
        'name': usuario[1],
        'email': usuario[2],
        'board': {'id': board['id'], 'name': board['name']} if board else None
    }

    return jsonify({'usuario': usuario_dict}), 200
