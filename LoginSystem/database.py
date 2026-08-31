import sqlite3
from werkzeug.security import generate_password_hash

BANCO = "banco.db"

def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel TEXT NOT NULL
    )
    """)

    # Cria o usuário admin padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        senha_hash = generate_password_hash("123456")
        cursor.execute(
            "INSERT INTO usuarios (nome, usuario, senha, nivel) VALUES (?, ?, ?, ?)",
            ("Administrador", "admin", senha_hash, "admin")
        )

    conn.commit()
    conn.close()