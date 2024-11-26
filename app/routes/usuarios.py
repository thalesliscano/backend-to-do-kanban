from flask import Blueprint, request, jsonify
from flasgger import swag_from
from ..services.usuario_service import UsuarioService
from ..services.board_service import BoardService  # Importa o serviço de Board

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
    usuario_id = resposta['usuario']['id']  # Obter ID do usuário criado
    board = BoardService.criar_board(usuario_id, 'Meu Board Padrão')
    
    return jsonify({
        'mensagem': 'Usuário criado com sucesso',
        'usuario': resposta['usuario'],
        'board': board
    }), 201


# Rota para login de usuário
@usuarios_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],  # Categoriza a rota na documentação
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
                    'usuario': {'id': 1, 'name': 'João', 'email': 'joao@exemplo.com'},
                    'token': 'exemplo_de_token_gerado_aqui'  # Exemplo estático para documentação
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
    
    usuario, token = UsuarioService.login(email, senha)
    
    if not usuario:
        return jsonify({'erro': 'Credenciais inválidas'}), 401  # Caso o login falhe

    return jsonify({
        'mensagem': 'Login bem-sucedido',
        'usuario': usuario,
        'token': token  # Retorna o token gerado na resposta
    }), 200

@usuarios_bp.route('/usuarios', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Retorna todos os usuários cadastrados no sistema',
    'responses': {
        '200': {
            'description': 'Lista de usuários encontrados',
            'examples': {
                'application/json': {
                    'usuarios': [
                        {'id': 1, 'nome': 'João', 'email': 'joao@exemplo.com'},
                        {'id': 2, 'nome': 'Maria', 'email': 'maria@exemplo.com'}
                    ]
                }
            }
        },
        '404': {
            'description': 'Nenhum usuário encontrado',
            'examples': {
                'application/json': {'erro': 'Nenhum usuário encontrado'}
            }
        }
    }
})
def buscar_usuarios():
    usuarios = UsuarioService.buscar_todos_usuarios()

    if not usuarios:
        return jsonify({'erro': 'Nenhum usuário encontrado'}), 404
    
    # Retorna os dados dos usuários
    usuarios_lista = [
        {'id': usuario[0], 'nome': usuario[1], 'email': usuario[2]}  # Ajuste conforme a estrutura da sua tabela
        for usuario in usuarios
    ]
    return jsonify({'usuarios': usuarios_lista}), 200
