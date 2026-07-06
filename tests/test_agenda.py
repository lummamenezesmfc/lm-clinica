import pytest
from datetime import datetime
from src.agenda.agenda import Agenda, Agendamento


def test_agendar_cria_agendamento():
    agenda = Agenda()
    a = agenda.agendar("Ana", "Botox", datetime(2026, 8, 1, 10, 0), "Dra. Lima")
    assert a.paciente == "Ana"
    assert a.procedimento == "Botox"
    assert a.confirmado is False


def test_confirmar_agendamento():
    agendamento = Agendamento("Ana", "Botox", datetime(2026, 8, 1, 10, 0), "Dra. Lima")
    agendamento.confirmar()
    assert agendamento.confirmado is True


def test_listar_do_dia_filtra_corretamente():
    agenda = Agenda()
    agenda.agendar("Ana", "Botox", datetime(2026, 8, 1, 10, 0), "Dra. Lima")
    agenda.agendar("Bia", "Preenchimento", datetime(2026, 8, 2, 14, 0), "Dra. Lima")

    do_dia = agenda.listar_do_dia(datetime(2026, 8, 1))
    assert len(do_dia) == 1
    assert do_dia[0].paciente == "Ana"


def test_listar_todos_ordenado_por_data():
    agenda = Agenda()
    agenda.agendar("Bia", "Preenchimento", datetime(2026, 8, 2, 14, 0), "Dra. Lima")
    agenda.agendar("Ana", "Botox", datetime(2026, 8, 1, 10, 0), "Dra. Lima")

    todos = agenda.listar_todos()
    assert todos[0].paciente == "Ana"
    assert todos[1].paciente == "Bia"
