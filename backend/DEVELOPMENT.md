# 🛠️ Guia de Desenvolvimento - Gestock Backend

Este documento serve como a referência técnica definitiva para desenvolvedores que atuam no núcleo do sistema, garantindo a consistência na manutenção da API e na orquestração dos módulos especializados.

> Se você quer apenas usar o módulo no Gestock, consulte o [README](README.md) 

## 💻 Stack Tecnológica
* **Linguagem:** Python `>= 3.11`.
* **Framework:** `FastAPI` (com suporte a operações assíncronas).
* **Gestão de Dependências:** `Poetry`.
* **Banco de Dados:** `PostgreSQL` via `SQLAlchemy` e `psycopg2`.
* **Qualidade de Código:** `Ruff` (Linting e Formatação).
* **Automação de Tasks:** `Taskipy`.

## 📂 Arquitetura do Projeto e Responsabilidades

O backend segue uma arquitetura modular baseada em separação de preocupações (SoC), onde o fluxo de dados atravessa camadas bem definidas:

```text
backend/
├── backend/
│   ├── main.py                # Ponto de entrada e registro de routers
│   ├── app.py                 # Configuração de middlewares e app FastAPI
│   ├── routers/               # Camada de Interface (Endpoints)
│   ├── services/              # Camada de Negócio (Lógica e Regras)
│   ├── database/              # Camada de Dados (Conexão e Repositórios)
│   └── utils/                 # Auxiliares (Exportação, Validação, Env)
├── tests/                     # Suíte de testes unitários e de integração
└── pyproject.toml             # Manifesto de dependências e automação
```

### Detalhamento das Camadas:
* **`routers/`**: Responsável apenas por receber a requisição, validar o esquema de entrada e chamar o serviço correspondente. Nunca deve conter lógica de negócio complexa.
* **`services/`**: É o motor do sistema. Aqui os dados são processados, cálculos são realizados e as regras de inventário são aplicadas antes da persistência.
* **`database/`**: Abstrai o acesso ao banco de dados. O arquivo `repository.py` centraliza as consultas SQL para evitar duplicação de queries.
* **`utils/env_loader.py`**: Garante que o sistema carregue as variáveis de ambiente necessárias para todos os módulos integrados, como chaves JWT e configurações de IA.

## ⚙️ Setup do Ambiente Local

### 1. Preparação
Certifique-se de ter o `pipx` e o `poetry` instalados.
```bash
pipx install poetry
pipx inject poetry poetry-plugin-shell
```

### 2. Instalação e Ativação
Dentro da pasta `/backend`, sincronize o ambiente:
```bash
poetry install
```
Ative o ambiente virtual conforme sua preferência:
* **Recomendado:** `iex (poetry env activate)` (ativação direta no terminal).
* **Sub-shell:** `poetry shell`.

### 3. Execução
Inicie o servidor de desenvolvimento com hot-reload:
```bash
task run
```

## 🚀 Padrões de Desenvolvimento e Qualidade

### Automação de Rotinas (Taskipy)
Antes de enviar qualquer código para o repositório, é obrigatório passar pelas checagens automáticas:
* **Verificar estilo:** `task lint` (Ruff check).
* **Corrigir estilo:** `task format` (Ruff format).
* **Validar lógica:** `task test` (Pytest com cobertura).

### Fluxo de Trabalho Git
* **Commits Semânticos:** Utilize o padrão Conventional Commits (ex: `feat(stock): implementar lógica de transferência interna`).
* **Gestão de Branches:** Crie branches a partir da `develop` seguindo o padrão `feature/nome-da-task` ou `fix/nome-do-bug`.
* **Code Review:** Todo Pull Request deve passar por validação de um par antes do merge para a `develop`.

## 🔌 Integração de Novos Módulos

O backend foi desenhado para ser extensível. Para adicionar um novo módulo (biblioteca interna):
1. Adicione a dependência local no `pyproject.toml` com a flag `develop = true`.
2. Registre os novos roteadores no `backend/main.py` utilizando `app.include_router()`.
3. Garante que o novo módulo utilize o `env_loader` central do backend para manter a consistência das variáveis de configuração.