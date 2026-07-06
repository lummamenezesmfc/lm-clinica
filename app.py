from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from pathlib import Path
from src.database import inicializar
from src.pacientes.paciente import Paciente
from src.pacientes import repositorio as repo_pacientes
from src.agenda.agenda import Agendamento
from src.agenda import repositorio as repo_agenda
from src.financeiro.financeiro import TipoLancamento, Lancamento
from src.financeiro import repositorio as repo_financeiro
from src.prontuario.prontuario import Evolucao
from src.prontuario import repositorio as repo_prontuario
from src.estoque.produto import Produto
from src.estoque import repositorio as repo_estoque

UPLOAD_DIR = Path(__file__).parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
    lista = repo_pacientes.listar_com_ids()
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


# --- Estoque ---

@app.route("/estoque")
def estoque():
    produtos = repo_estoque.listar_todos()
    alertas = [(p, pid) for p, pid in produtos if p.abaixo_do_minimo or p.vencido or p.vence_em_breve]
    return render_template("estoque.html", produtos=produtos, alertas=alertas)


@app.route("/estoque/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        validade = request.form.get("validade")
        produto = Produto(
            nome=request.form["nome"],
            quantidade=float(request.form["quantidade"]),
            unidade=request.form["unidade"],
            validade=__import__('datetime').date.fromisoformat(validade) if validade else None,
            fornecedor=request.form.get("fornecedor", ""),
            quantidade_minima=float(request.form.get("quantidade_minima") or 0),
        )
        repo_estoque.salvar(produto)
        return redirect(url_for("estoque"))
    return render_template("novo_produto.html")


@app.route("/estoque/<int:produto_id>/ajustar", methods=["POST"])
def ajustar_estoque(produto_id):
    nova_qtd = float(request.form["quantidade"])
    repo_estoque.atualizar_quantidade(produto_id, nova_qtd)
    return redirect(url_for("estoque"))


# --- Prontuário ---

@app.route("/pacientes/<int:paciente_id>/prontuario")
def prontuario(paciente_id):
    paciente = repo_pacientes.buscar_por_id(paciente_id)
    evolucoes = repo_prontuario.listar_por_paciente(paciente_id)
    return render_template("prontuario.html", paciente=paciente, evolucoes=evolucoes, paciente_id=paciente_id)


@app.route("/pacientes/<int:paciente_id>/prontuario/nova", methods=["GET", "POST"])
def nova_evolucao(paciente_id):
    paciente = repo_pacientes.buscar_por_id(paciente_id)
    if request.method == "POST":
        foto_antes = ""
        foto_depois = ""

        for campo, nome_var in [("foto_antes", "foto_antes"), ("foto_depois", "foto_depois")]:
            arquivo = request.files.get(campo)
            if arquivo and arquivo.filename:
                caminho = UPLOAD_DIR / f"{paciente_id}_{campo}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{arquivo.filename}"
                arquivo.save(caminho)
                if campo == "foto_antes":
                    foto_antes = f"uploads/{caminho.name}"
                else:
                    foto_depois = f"uploads/{caminho.name}"

        evolucao = Evolucao(
            procedimento=request.form["procedimento"],
            descricao=request.form["descricao"],
            profissional=request.form["profissional"],
            foto_antes=foto_antes,
            foto_depois=foto_depois,
        )
        repo_prontuario.salvar_evolucao(paciente_id, evolucao)
        return redirect(url_for("prontuario", paciente_id=paciente_id))
    return render_template("nova_evolucao.html", paciente=paciente)


if __name__ == "__main__":
    app.run(debug=True)
