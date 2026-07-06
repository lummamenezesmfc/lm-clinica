from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TipoLancamento(Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"


@dataclass
class Lancamento:
    descricao: str
    valor: float
    tipo: TipoLancamento
    data: datetime = field(default_factory=datetime.now)
    paciente: str = ""


class Financeiro:
    def __init__(self):
        self._lancamentos: list[Lancamento] = []

    def registrar(self, descricao: str, valor: float, tipo: TipoLancamento, paciente: str = "") -> Lancamento:
        lancamento = Lancamento(descricao, valor, tipo, paciente=paciente)
        self._lancamentos.append(lancamento)
        return lancamento

    @property
    def saldo(self) -> float:
        entradas = sum(l.valor for l in self._lancamentos if l.tipo == TipoLancamento.ENTRADA)
        saidas = sum(l.valor for l in self._lancamentos if l.tipo == TipoLancamento.SAIDA)
        return entradas - saidas

    def extrato(self) -> list[Lancamento]:
        return sorted(self._lancamentos, key=lambda l: l.data)
