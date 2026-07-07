from datetime import datetime
from src.database import conectar
from src.agenda.agenda import Agendamento


def salvar(agendamento: Agendamento, paciente_id: int) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            "INSERT INTO agendamentos (paciente_id, procedimento, data_hora, profissional, confirmado) VALUES (?, ?, ?, ?, ?)",
            (paciente_id, agendamento.procedimento, agendamento.data_hora.isoformat(), agendamento.profissional, int(agendamento.confirmado)),
        )
        return cursor.lastrowid


def atualizar(agendamento_id: int, procedimento: str, data_hora: datetime, profissional: str):
    with conectar() as conn:
        conn.execute(
            "UPDATE agendamentos SET procedimento=?, data_hora=?, profissional=? WHERE id=?",
            (procedimento, data_hora.isoformat(), profissional, agendamento_id),
        )


def confirmar(agendamento_id: int):
    with conectar() as conn:
        conn.execute("UPDATE agendamentos SET confirmado = 1 WHERE id = ?", (agendamento_id,))


def buscar_por_id(agendamento_id: int) -> dict | None:
    with conectar() as conn:
        row = conn.execute("""
            SELECT a.id, p.nome as paciente, a.paciente_id, a.procedimento, a.data_hora, a.profissional, a.confirmado
            FROM agendamentos a
            JOIN pacientes p ON p.id = a.paciente_id
            WHERE a.id = ?
        """, (agendamento_id,)).fetchone()
    return dict(row) if row else None


def listar_do_dia(data: datetime) -> list[dict]:
    with conectar() as conn:
        rows = conn.execute("""
            SELECT a.id, p.nome as paciente, a.procedimento, a.data_hora, a.profissional, a.confirmado
            FROM agendamentos a
            JOIN pacientes p ON p.id = a.paciente_id
            WHERE date(a.data_hora) = ?
            ORDER BY a.data_hora
        """, (data.date().isoformat(),)).fetchall()
    return [dict(r) for r in rows]


def listar_todos() -> list[dict]:
    with conectar() as conn:
        rows = conn.execute("""
            SELECT a.id, p.nome as paciente, a.procedimento, a.data_hora, a.profissional, a.confirmado
            FROM agendamentos a
            JOIN pacientes p ON p.id = a.paciente_id
            ORDER BY a.data_hora
        """).fetchall()
    return [dict(r) for r in rows]
