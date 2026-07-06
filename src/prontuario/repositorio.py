from datetime import datetime
from src.database import conectar
from src.prontuario.prontuario import Evolucao


def salvar_evolucao(paciente_id: int, evolucao: Evolucao) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            """INSERT INTO evolucoes
               (paciente_id, procedimento, descricao, profissional, data, foto_antes, foto_depois)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (paciente_id, evolucao.procedimento, evolucao.descricao,
             evolucao.profissional, evolucao.data.isoformat(),
             evolucao.foto_antes, evolucao.foto_depois),
        )
        return cursor.lastrowid


def listar_por_paciente(paciente_id: int) -> list[dict]:
    with conectar() as conn:
        rows = conn.execute(
            "SELECT * FROM evolucoes WHERE paciente_id = ? ORDER BY data DESC",
            (paciente_id,)
        ).fetchall()
    return [dict(r) for r in rows]
