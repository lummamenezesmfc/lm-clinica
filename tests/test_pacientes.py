import pytest
from datetime import date
from src.pacientes.paciente import Paciente


def test_idade_calculada_corretamente():
    paciente = Paciente("Ana", "11999999999", "ana@email.com", date(1990, 1, 1))
    assert paciente.idade == date.today().year - 1990 - (
        (date.today().month, date.today().day) < (1, 1)
    )


def test_adicionar_anotacao():
    paciente = Paciente("Ana", "11999999999", "ana@email.com", date(1990, 1, 1))
    paciente.adicionar_anotacao("Primeira consulta")
    assert "Primeira consulta" in paciente.historico


def test_historico_vazio_por_padrao():
    paciente = Paciente("Ana", "11999999999", "ana@email.com", date(1990, 1, 1))
    assert paciente.historico == []
