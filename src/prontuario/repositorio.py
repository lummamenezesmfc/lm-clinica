from datetime import datetime, timedelta
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


def buscar_por_id(evolucao_id: int) -> dict | None:
    with conectar() as conn:
        row = conn.execute("SELECT * FROM evolucoes WHERE id = ?", (evolucao_id,)).fetchone()
    return dict(row) if row else None


def pode_editar(evolucao: dict) -> bool:
    criado_em = datetime.fromisoformat(evolucao["data"])
    return datetime.now() - criado_em <= timedelta(hours=24)


def atualizar_evolucao(evolucao_id: int, procedimento: str, descricao: str, profissional: str):
    with conectar() as conn:
        conn.execute(
            "UPDATE evolucoes SET procedimento=?, descricao=?, profissional=? WHERE id=?",
            (procedimento, descricao, profissional, evolucao_id),
        )


def listar_por_paciente(paciente_id: int) -> list[dict]:
    with conectar() as conn:
        rows = conn.execute(
            "SELECT * FROM evolucoes WHERE paciente_id = ? ORDER BY data DESC",
            (paciente_id,)
        ).fetchall()
    return [dict(r) for r in rows]
