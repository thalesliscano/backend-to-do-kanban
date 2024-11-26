from app import create_app
import sqlite3

def conectar_bd():
    return sqlite3.connect('database.db')  # Substitua 'database.db' pelo nome do arquivo de banco de dados

# Função para criar o banco de dados e as tabelas necessárias
def criar_tabelas():
    conn = sqlite3.connect('database.db')  # Conecta ao banco de dados SQLite
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

    # Criar tabela 'tasks'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        board_id INTEGER NOT NULL,
        task_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL CHECK (status IN ('toDo', 'doing', 'done')),
        completed_date TEXT,
        FOREIGN KEY (board_id) REFERENCES boards(id)
    );
    ''')

    conn.commit()
    conn.close()

# Executar a criação das tabelas
criar_tabelas()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
