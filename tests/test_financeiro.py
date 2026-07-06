import pytest
from src.financeiro.financeiro import Financeiro, TipoLancamento


def test_saldo_inicial_zero():
    fin = Financeiro()
    assert fin.saldo == 0.0


def test_entrada_aumenta_saldo():
    fin = Financeiro()
    fin.registrar("Consulta Ana", 250.0, TipoLancamento.ENTRADA)
    assert fin.saldo == 250.0


def test_saida_diminui_saldo():
    fin = Financeiro()
    fin.registrar("Consulta Ana", 250.0, TipoLancamento.ENTRADA)
    fin.registrar("Material", 50.0, TipoLancamento.SAIDA)
    assert fin.saldo == 200.0


def test_extrato_ordenado_por_data():
    fin = Financeiro()
    fin.registrar("Consulta Ana", 250.0, TipoLancamento.ENTRADA)
    fin.registrar("Material", 50.0, TipoLancamento.SAIDA)
    extrato = fin.extrato()
    assert len(extrato) == 2
