from datetime import datetime
from src.database import conectar
from src.financeiro.financeiro import Lancamento, TipoLancamento


def salvar(lancamento: Lancamento) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO lancamentos (descricao, valor, tipo, data, paciente) VALUES (?, ?, ?, ?, ?)",
            (lancamento.descricao, lancamento.valor, lancamento.tipo.value, lancamento.data.isoformat(), lancamento.paciente),
        )
        return cursor.lastrowid


def saldo() -> float:
    with conectar() as conn:
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END) -
                SUM(CASE WHEN tipo = 'saida' THEN valor ELSE 0 END) as saldo
            FROM lancamentos
        """).fetchone()
    return row["saldo"] or 0.0


def extrato(mes: int | None = None, ano: int | None = None) -> list[dict]:
    query = "SELECT * FROM lancamentos"
    params = []
    if mes and ano:
        query += " WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?"
        params = [f"{mes:02d}", str(ano)]
    query += " ORDER BY data"
    with conectar() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]
