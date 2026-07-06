from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from src.database import inicializar
from src.pacientes.paciente import Paciente
from src.pacientes import repositorio as repo_pacientes
from src.agenda.agenda import Agendamento
from src.agenda import repositorio as repo_agenda
from src.financeiro.financeiro import TipoLancamento, Lancamento
from src.financeiro import repositorio as repo_financeiro

app = Flask(__name__)
inicializar()


@app.route("/")
def index():
    hoje = datetime.today()
    agendamentos = repo_agenda.listar_do_dia(hoje)
    saldo = repo_financeiro.saldo()
    total_pacientes = len(repo_pacientes.listar_todos())
    return render_template("index.html", agendamentos=agendamentos, saldo=saldo, total_pacientes=total_pacientes, hoje=hoje)


# --- Pacientes ---

@app.route("/pacientes")
def pacientes():
    lista = repo_pacientes.listar_todos()
    return render_template("pacientes.html", pacientes=lista)


@app.route("/pacientes/novo", methods=["GET", "POST"])
def novo_paciente():
    if request.method == "POST":
        paciente = Paciente(
            nome=request.form["nome"],
            telefone=request.form["telefone"],
            email=request.form["email"],
            data_nascimento=date.fromisoformat(request.form["data_nascimento"]),
            observacoes=request.form.get("observacoes", ""),
        )
        repo_pacientes.salvar(paciente)
        return redirect(url_for("pacientes"))
    return render_template("novo_paciente.html")


# --- Agenda ---

@app.route("/agenda")
def agenda():
    agendamentos = repo_agenda.listar_todos()
    return render_template("agenda.html", agendamentos=agendamentos)


@app.route("/agenda/novo", methods=["GET", "POST"])
def novo_agendamento():
    pacientes = repo_pacientes.listar_todos()
    if request.method == "POST":
        paciente_id = int(request.form["paciente_id"])
        agendamento = Agendamento(
            paciente=request.form["paciente_nome"],
            procedimento=request.form["procedimento"],
            data_hora=datetime.fromisoformat(request.form["data_hora"]),
            profissional=request.form["profissional"],
        )
        repo_agenda.salvar(agendamento, paciente_id)
        return redirect(url_for("agenda"))
    return render_template("novo_agendamento.html", pacientes=pacientes)


@app.route("/agenda/confirmar/<int:agendamento_id>")
def confirmar_agendamento(agendamento_id):
    repo_agenda.confirmar(agendamento_id)
    return redirect(url_for("agenda"))


# --- Financeiro ---

@app.route("/financeiro")
def financeiro():
    extrato = repo_financeiro.extrato()
    saldo = repo_financeiro.saldo()
    return render_template("financeiro.html", extrato=extrato, saldo=saldo)


@app.route("/financeiro/novo", methods=["GET", "POST"])
def novo_lancamento():
    if request.method == "POST":
        lancamento = Lancamento(
            descricao=request.form["descricao"],
            valor=float(request.form["valor"]),
            tipo=TipoLancamento(request.form["tipo"]),
            paciente=request.form.get("paciente", ""),
        )
        repo_financeiro.salvar(lancamento)
        return redirect(url_for("financeiro"))
    return render_template("novo_lancamento.html")


if __name__ == "__main__":
    app.run(debug=True)
