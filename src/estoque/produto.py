from dataclasses import dataclass
from datetime import date


@dataclass
class Produto:
    nome: str
    quantidade: float
    unidade: str
    validade: date | None
    fornecedor: str = ""
    quantidade_minima: float = 0

    @property
    def abaixo_do_minimo(self) -> bool:
        return self.quantidade <= self.quantidade_minima

    @property
    def vencido(self) -> bool:
        if not self.validade:
            return False
        return self.validade < date.today()

    @property
    def vence_em_breve(self) -> bool:
        if not self.validade:
            return False
        from datetime import timedelta
        return date.today() <= self.validade <= date.today() + timedelta(days=30)
