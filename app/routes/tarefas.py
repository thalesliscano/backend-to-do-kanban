from flask import Blueprint, request, jsonify
from ..services.tarefa_service import TarefaService

tarefas_bp = Blueprint('tarefas', __name__)

@tarefas_bp.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.json
    titulo = dados['title']
    descricao = dados.get('description', '')
    status = dados.get('status', 'toDo')  # Padrão: 'toDo'
    board_id = dados['board_id']

    tarefa = TarefaService.criar_tarefa(board_id, titulo, descricao, status)
    return jsonify({'mensagem': 'Tarefa criada com sucesso'}), 201

@tarefas_bp.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = TarefaService.listar_tarefas()
    return jsonify(tarefas), 200

@tarefas_bp.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    dados = request.json
    novo_status = dados['status']
    TarefaService.atualizar_tarefa(tarefa_id, novo_status)
    return jsonify({'mensagem': 'Tarefa atualizada com sucesso'}), 200

@tarefas_bp.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
    TarefaService.excluir_tarefa(tarefa_id)
    return jsonify({'mensagem': 'Tarefa excluída com sucesso'}), 200
