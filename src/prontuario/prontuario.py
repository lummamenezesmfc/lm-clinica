from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Evolucao:
    procedimento: str
    descricao: str
    profissional: str
    data: datetime = field(default_factory=datetime.now)
    foto_antes: str = ""
    foto_depois: str = ""


@dataclass
class Prontuario:
    paciente_id: int
    evolucoes: list[Evolucao] = field(default_factory=list)

    def adicionar_evolucao(self, evolucao: Evolucao):
        self.evolucoes.append(evolucao)

    def ultima_evolucao(self) -> Evolucao | None:
        if not self.evolucoes:
            return None
        return sorted(self.evolucoes, key=lambda e: e.data)[-1]
