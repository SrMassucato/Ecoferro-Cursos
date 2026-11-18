# Cursos Ecoferro

Portfólio de cursos da empresa voltado ao **setor de eletrônica**. Cada curso é dividido em **itens**, e cada item traz o **processo detalhado, passo a passo**.

> Projeto individual de um curso de programação. Nível: iniciante.

## Objetivo

Reduzir a falta de conhecimento técnico no setor, oferecendo material de ensino e aprendizado organizado e fácil de consultar.

**Público-alvo:** funcionários da empresa.

## Como funciona

- **Frontend (HTML, CSS e JavaScript):** páginas que o funcionário vê no navegador, com a lista de cursos e o passo a passo de cada item.
- **Backend (Python + Flask):** uma API simples que lê o arquivo de dados e entrega as informações ao frontend.
- **Dados (`data/cursos.json`):** o conteúdo dos cursos. Não há banco de dados; para adicionar ou alterar um curso, basta editar esse arquivo.

## Tecnologias

- Python 3 e Flask
- HTML, CSS e JavaScript
- Git e GitHub (controle de versão)
- VS Code (desenvolvimento)
- Google Colab (apenas para experimentos, fora da aplicação)

## Estrutura do projeto

```text
cursos-ecoferro/
├── README.md
├── .gitignore
├── requirements.txt
├── docs/
│   └── arquitetura.md
├── data/
│   └── cursos.json
├── frontend/
│   ├── index.html
│   ├── curso.html
│   ├── css/estilo.css
│   └── js/app.js
├── backend/
│   └── app.py
└── notebooks/
    └── exploracao.ipynb   (opcional)
```

Esta estrutura é uma proposta inicial e pode mudar durante o desenvolvimento.

## Como rodar

1. Clone o repositório e entre na pasta:
   ```bash
   git clone <endereço-do-repositório>
   cd cursos-ecoferro
   ```
2. (Recomendado) Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/Mac
   .venv\Scripts\activate         # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie o servidor:
   ```bash
   python backend/app.py
   ```
5. Abra no navegador: <http://127.0.0.1:5000>

## API

| Rota | Retorna |
|---|---|
| `GET /` | Página inicial (`frontend/index.html`) |
| `GET /api/cursos` | Lista resumida de cursos |
| `GET /api/cursos/<curso_id>` | Um curso com a lista de itens |
| `GET /api/cursos/<curso_id>/itens/<item_id>` | Um item com o passo a passo completo |

## Formato do `data/cursos.json`

```json
[
  {
    "id": "soldagem",
    "titulo": "Soldagem de componentes",
    "descricao": "Descrição do curso",
    "nivel": "iniciante",
    "carga_horaria": 4,
    "itens": [
      {
        "id": "solda-resistor",
        "titulo": "Soldando um resistor",
        "resumo": "Resumo do item",
        "passos": [
          { "ordem": 1, "titulo": "Preparar a bancada", "descricao": "..." }
        ]
      }
    ]
  }
]
```

## Segurança

Não envie ao repositório senhas, tokens, chaves de API ou o arquivo `.env`. O `.gitignore` já deve ignorá-los.

## Status do projeto

- [x] Estrutura de pastas definida
- [x] Backend (`backend/app.py`) e `requirements.txt`
- [ ] Conteúdo dos cursos em `data/cursos.json`
- [ ] Frontend (`index.html`, `curso.html`, `estilo.css`, `app.js`)
- [ ] Revisão final e aprovação do professor

## Autor

Bruno Felipe Silva Massucato
