from datetime import datetime


class Agendamento:
    def __init__(self, paciente: str, procedimento: str, data_hora: datetime, profissional: str):
        self.paciente = paciente
        self.procedimento = procedimento
        self.data_hora = data_hora
        self.profissional = profissional
        self.confirmado = False

    def confirmar(self):
        self.confirmado = True

    def __repr__(self):
        status = "confirmado" if self.confirmado else "pendente"
        return f"[{status}] {self.paciente} — {self.procedimento} — {self.data_hora.strftime('%d/%m/%Y %H:%M')} com {self.profissional}"


class Agenda:
    def __init__(self):
        self._agendamentos: list[Agendamento] = []

    def agendar(self, paciente: str, procedimento: str, data_hora: datetime, profissional: str) -> Agendamento:
        agendamento = Agendamento(paciente, procedimento, data_hora, profissional)
        self._agendamentos.append(agendamento)
        return agendamento

    def listar_do_dia(self, data: datetime) -> list[Agendamento]:
        return [a for a in self._agendamentos if a.data_hora.date() == data.date()]

    def listar_todos(self) -> list[Agendamento]:
        return sorted(self._agendamentos, key=lambda a: a.data_hora)
