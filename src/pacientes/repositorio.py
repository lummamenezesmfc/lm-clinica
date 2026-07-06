from datetime import date
from src.database import conectar
from src.pacientes.paciente import Paciente


def salvar(paciente: Paciente) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO pacientes (nome, telefone, email, data_nascimento, observacoes) VALUES (?, ?, ?, ?, ?)",
            (paciente.nome, paciente.telefone, paciente.email, paciente.data_nascimento.isoformat(), paciente.observacoes),
        )
        return cursor.lastrowid


def buscar_por_id(paciente_id: int) -> Paciente | None:
    with conectar() as conn:
        row = conn.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,)).fetchone()
    if not row:
        return None
    return _row_para_paciente(row)


def buscar_por_nome(nome: str) -> list[Paciente]:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM pacientes WHERE nome LIKE ?", (f"%{nome}%",)).fetchall()
    return [_row_para_paciente(r) for r in rows]


def listar_todos() -> list[Paciente]:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
    return [_row_para_paciente(r) for r in rows]


def listar_com_ids() -> list[tuple[Paciente, int]]:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
    return [(_row_para_paciente(r), r["id"]) for r in rows]


def _row_para_paciente(row) -> Paciente:
    return Paciente(
        nome=row["nome"],
        telefone=row["telefone"],
        email=row["email"],
        data_nascimento=date.fromisoformat(row["data_nascimento"]),
        observacoes=row["observacoes"] or "",
    )
