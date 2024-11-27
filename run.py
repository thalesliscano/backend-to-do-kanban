from app import create_app
import sqlite3

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('database.db')  # Substitua 'database.db' pelo nome do arquivo de banco de dados

# Função para criar o banco de dados e as tabelas necessárias
def criar_tabelas():
    conn = conectar_bd()  # Conecta ao banco de dados SQLite
    cursor = conn.cursor()

    # Criar tabela 'users'
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    ''')

    # Criar tabela 'boards'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS boards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # Criar tabela 'tasks' (alterado para ter os status 'fazer', 'fazendo', 'completa')
# Criar a tabela de tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_task_id INTEGER NOT NULL,  -- ID da tarefa por usuário
            title TEXT NOT NULL,
            description TEXT,
            user_id INTEGER NOT NULL,
            board_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('toDo', 'doing', 'done')) DEFAULT 'doing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (board_id) REFERENCES boards(id)
        );
    ''')

    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão com o banco de dados

# Executar a criação das tabelas
criar_tabelas()

def alterar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Primeiro, cria uma nova tabela com a coluna 'status' ajustada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_task_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        board_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('toDo', 'doing', 'done', 'archive')) DEFAULT 'doing',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (board_id) REFERENCES boards(id)
    );
    ''')

    # Copiar os dados da tabela antiga para a nova tabela
    cursor.execute('''
    INSERT INTO tasks_new (id, user_task_id, title, description, user_id, board_id, status, created_at)
    SELECT id, user_task_id, title, description, user_id, board_id, status, created_at FROM tasks;
    ''')

    # Deletar a tabela antiga
    cursor.execute('DROP TABLE tasks;')

    # Renomear a nova tabela para 'tasks'
    cursor.execute('ALTER TABLE tasks_new RENAME TO tasks;')

    conn.commit()
    conn.close()

# Executar a alteração da tabela
alterar_tabela()


# Inicializa a aplicação Flask
app = create_app()

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
