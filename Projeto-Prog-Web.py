import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
from classes import Tarefa, GerenciadorTarefas

# Caminho para o arquivo JSON com as credenciais
cred = credentials.Certificate('credenciais.json')

# Inicializar o Firebase
firebase_admin.initialize_app(cred)

# Inicializar o Firestore
db = firestore.client()

# Teste de conexão: tentar acessar uma coleção
try:
    tasks = db.collection('tasks').get()
    print("Conexão com o Firestore bem-sucedida. Número de tarefas encontradas: ", len(tasks))
except Exception as e:
    print("Erro ao conectar ao Firestore: ", e)

# Criar a instância do Flask
app = Flask(__name__)
CORS(app)
gerenciador_tarefas = GerenciadorTarefas('credenciais.json')

# Rota para criar uma nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.json
    tarefa = Tarefa(titulo=dados['titulo'], descricao=dados['descricao'], status=dados.get('status', 'A Fazer'))
    gerenciador_tarefas.adicionar_tarefa(tarefa)
    return jsonify({'mensagem': 'Tarefa criada com sucesso'}), 201

# Rota para listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    lista_tarefas = gerenciador_tarefas.listar_tarefas()
    return jsonify(lista_tarefas), 200

# Rota para atualizar o status de uma tarefa
@app.route('/tarefas/<tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    dados = request.json
    gerenciador_tarefas.atualizar_status_tarefa(tarefa_id, dados['status'])
    return jsonify({'mensagem': 'Tarefa atualizada com sucesso'}), 200

# Rota para excluir uma tarefa
@app.route('/tarefas/excluir/<tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
    gerenciador_tarefas.excluir_tarefa(tarefa_id)
    return jsonify({'mensagem': 'Tarefa excluída com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)