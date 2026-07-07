from dataclasses import dataclass, field
from datetime import date


@dataclass
class Paciente:
    nome: str
    telefone: str
    email: str
    data_nascimento: date
    cpf: str = ""
    endereco: str = ""
    observacoes: str = ""
    historico: list[str] = field(default_factory=list)

    def adicionar_anotacao(self, anotacao: str):
        self.historico.append(anotacao)

    @property
    def idade(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
