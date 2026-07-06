from src.database import conectar
from src.estoque.produto import Produto
from datetime import date


def salvar(produto: Produto) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            """INSERT INTO produtos
               (nome, quantidade, unidade, validade, fornecedor, quantidade_minima)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (produto.nome, produto.quantidade, produto.unidade,
             produto.validade.isoformat() if produto.validade else None,
             produto.fornecedor, produto.quantidade_minima),
        )
        return cursor.lastrowid


def atualizar_quantidade(produto_id: int, nova_quantidade: float):
    with conectar() as conn:
        conn.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))


def listar_todos() -> list[tuple[Produto, int]]:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    return [(_row_para_produto(r), r["id"]) for r in rows]


def buscar_por_id(produto_id: int) -> tuple[Produto, int] | None:
    with conectar() as conn:
        row = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
    if not row:
        return None
    return _row_para_produto(row), row["id"]


def _row_para_produto(row) -> Produto:
    return Produto(
        nome=row["nome"],
        quantidade=row["quantidade"],
        unidade=row["unidade"],
        validade=date.fromisoformat(row["validade"]) if row["validade"] else None,
        fornecedor=row["fornecedor"] or "",
        quantidade_minima=row["quantidade_minima"] or 0,
    )
