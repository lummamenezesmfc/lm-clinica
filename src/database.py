import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "clinica.db"


def conectar() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar():
    with conectar() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                data_nascimento TEXT NOT NULL,
                observacoes TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                procedimento TEXT NOT NULL,
                data_hora TEXT NOT NULL,
                profissional TEXT NOT NULL,
                confirmado INTEGER DEFAULT 0,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
            );

            CREATE TABLE IF NOT EXISTS evolucoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                procedimento TEXT NOT NULL,
                descricao TEXT NOT NULL,
                profissional TEXT NOT NULL,
                data TEXT NOT NULL,
                foto_antes TEXT DEFAULT '',
                foto_depois TEXT DEFAULT '',
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
            );

            CREATE TABLE IF NOT EXISTS lancamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                tipo TEXT NOT NULL,
                data TEXT NOT NULL,
                paciente TEXT DEFAULT ''
            );
        """)
