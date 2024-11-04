import firebase_admin
from firebase_admin import credentials, firestore

class Tarefa:
    def __init__(self, titulo, descricao, status='A Fazer'):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status

class GerenciadorTarefas:
    def __init__(self, json_path):
        # Inicializa o Firebase
        cred = credentials.Certificate(json_path)
        self.db = firestore.client()  # Inicializa o Firestore aqui

    def adicionar_tarefa(self, tarefa):
        # Referência para a coleção "tarefas"
        doc_ref = self.db.collection('tarefas').document()  # Corrigido para 'tarefas'
        # Dados da tarefa
        dados_tarefa = {
            'titulo': tarefa.titulo,
            'descricao': tarefa.descricao,
            'status': tarefa.status,
            'criado_em': firestore.SERVER_TIMESTAMP,
            'atualizado_em': firestore.SERVER_TIMESTAMP
        }
        # Adicionando a tarefa ao Firestore
        doc_ref.set(dados_tarefa)
        print(f'Tarefa "{tarefa.titulo}" adicionada com sucesso.')

    def listar_tarefas(self):
        # Referência para a coleção "tarefas"
        tarefas_ref = self.db.collection('tarefas').stream()
        # Listar todas as tarefas
        lista_tarefas = []
        for tarefa in tarefas_ref:
            dados_tarefa = tarefa.to_dict()
            dados_tarefa['id'] = tarefa.id  # Adiciona o ID da tarefa
            lista_tarefas.append(dados_tarefa)
        return lista_tarefas

    def atualizar_status_tarefa(self, tarefa_id, novo_status):
        # Referência para o documento da tarefa
        doc_ref = self.db.collection('tarefas').document(tarefa_id)
        # Atualizar o status da tarefa
        doc_ref.update({
            'status': novo_status,
            'atualizado_em': firestore.SERVER_TIMESTAMP
        })
        print(f'Tarefa {tarefa_id} atualizada para o status "{novo_status}".')

    def excluir_tarefa(self, tarefa_id):
        # Obtém a referência do documento pela ID
        tarefa_ref = self.db.collection('tarefas').document(tarefa_id)

        # Verifica se o documento existe antes de tentar excluí-lo
        if tarefa_ref.get().exists:
            tarefa_ref.delete()
            print(f'Tarefa {tarefa_id} excluída com sucesso.')
        else:
            print(f'Tarefa {tarefa_id} não encontrada.')
