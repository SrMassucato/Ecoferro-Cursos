"""
Cursos Ecoferro - API em Python (Flask)

Este programa faz duas coisas:
  1. Lê o arquivo data/cursos.json (nosso "banco de dados" em texto).
  2. Entrega esses dados ao frontend por meio de uma API.

Como rodar (a partir da pasta raiz do projeto):
    pip install flask
    python backend/app.py
Depois abra no navegador: http://127.0.0.1:5000

Rotas disponíveis:
    GET /                                      -> página inicial (frontend/index.html)
    GET /api/cursos                            -> lista resumida de cursos
    GET /api/cursos/<curso_id>                 -> um curso, com a lista de itens
    GET /api/cursos/<curso_id>/itens/<item_id> -> um item, com o processo detalhado (passos)

Estrutura esperada do data/cursos.json:
[
  {
    "id": "soldagem",
    "titulo": "Soldagem de componentes",
    "descricao": "...",
    "nivel": "iniciante",
    "carga_horaria": 4,
    "itens": [
      {
        "id": "solda-resistor",
        "titulo": "Soldando um resistor",
        "resumo": "...",
        "passos": [
          {"ordem": 1, "titulo": "Preparar a bancada", "descricao": "..."}
        ]
      }
    ]
  }
]
"""

import json
from pathlib import Path

from flask import Flask, abort, jsonify, send_from_directory

# ---------------------------------------------------------------------------
# Caminhos: descobrimos as pastas a partir da localização deste arquivo,
# assim o programa funciona não importa de onde você o execute.
# ---------------------------------------------------------------------------
PASTA_BACKEND = Path(__file__).resolve().parent
PASTA_RAIZ = PASTA_BACKEND.parent
ARQUIVO_CURSOS = PASTA_RAIZ / "data" / "cursos.json"
PASTA_FRONTEND = PASTA_RAIZ / "frontend"

# O Flask também entrega os arquivos do frontend (HTML, CSS, JS).
# Assim, tudo roda em um único endereço e não precisamos configurar CORS.
app = Flask(__name__, static_folder=str(PASTA_FRONTEND), static_url_path="")


# ---------------------------------------------------------------------------
# Funções de apoio (leitura dos dados)
# ---------------------------------------------------------------------------
def carregar_cursos():
    """Lê o cursos.json e devolve a lista de cursos.

    O arquivo é lido a cada requisição: se você editar o JSON, basta
    atualizar a página, sem reiniciar o servidor.
    """
    try:
        with open(ARQUIVO_CURSOS, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        abort(500, description="Arquivo data/cursos.json não encontrado.")
    except json.JSONDecodeError as erro:
        abort(
            500,
            description=f"cursos.json com erro de formatação "
            f"(linha {erro.lineno}, coluna {erro.colno}).",
        )

    if not isinstance(dados, list):
        abort(500, description="cursos.json deve conter uma lista de cursos.")
    return dados


def buscar_curso(curso_id):
    """Procura um curso pelo id. Devolve erro 404 se não existir."""
    for curso in carregar_cursos():
        if curso.get("id") == curso_id:
            return curso
    abort(404, description=f"Curso '{curso_id}' não encontrado.")


def buscar_item(curso, item_id):
    """Procura um item dentro de um curso. Devolve erro 404 se não existir."""
    for item in curso.get("itens", []):
        if item.get("id") == item_id:
            return item
    abort(404, description=f"Item '{item_id}' não encontrado neste curso.")


# ---------------------------------------------------------------------------
# Rotas da API
# ---------------------------------------------------------------------------
@app.route("/api/cursos")
def listar_cursos():
    """Lista resumida: só o necessário para montar a página inicial."""
    resumo = []
    for curso in carregar_cursos():
        resumo.append(
            {
                "id": curso.get("id"),
                "titulo": curso.get("titulo"),
                "descricao": curso.get("descricao"),
                "nivel": curso.get("nivel"),
                "carga_horaria": curso.get("carga_horaria"),
                "total_itens": len(curso.get("itens", [])),
            }
        )
    return jsonify(resumo)


@app.route("/api/cursos/<curso_id>")
def detalhar_curso(curso_id):
    """Um curso com a lista de itens (sem os passos, para ficar leve)."""
    curso = buscar_curso(curso_id)
    itens_resumidos = [
        {
            "id": item.get("id"),
            "titulo": item.get("titulo"),
            "resumo": item.get("resumo"),
            "total_passos": len(item.get("passos", [])),
        }
        for item in curso.get("itens", [])
    ]
    return jsonify(
        {
            "id": curso.get("id"),
            "titulo": curso.get("titulo"),
            "descricao": curso.get("descricao"),
            "nivel": curso.get("nivel"),
            "carga_horaria": curso.get("carga_horaria"),
            "itens": itens_resumidos,
        }
    )


@app.route("/api/cursos/<curso_id>/itens/<item_id>")
def detalhar_item(curso_id, item_id):
    """Um item completo, com o processo detalhado (passo a passo)."""
    curso = buscar_curso(curso_id)
    item = buscar_item(curso, item_id)

    # Garante que os passos saiam na ordem correta.
    passos = sorted(item.get("passos", []), key=lambda p: p.get("ordem", 0))
    return jsonify(
        {
            "curso_id": curso.get("id"),
            "curso_titulo": curso.get("titulo"),
            "id": item.get("id"),
            "titulo": item.get("titulo"),
            "resumo": item.get("resumo"),
            "passos": passos,
        }
    )


# ---------------------------------------------------------------------------
# Página inicial e erros
# ---------------------------------------------------------------------------
@app.route("/")
def pagina_inicial():
    """Entrega o frontend/index.html."""
    return send_from_directory(PASTA_FRONTEND, "index.html")


@app.errorhandler(404)
@app.errorhandler(500)
def tratar_erro(erro):
    """Devolve os erros em JSON, para o frontend poder mostrar a mensagem."""
    return jsonify({"erro": erro.description}), erro.code


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True recarrega o servidor ao salvar o arquivo (bom para estudar).
    # Nunca use debug=True em um servidor real de produção.
    app.run(host="127.0.0.1", port=5000, debug=True)
