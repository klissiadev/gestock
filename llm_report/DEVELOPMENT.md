# 🛠️ Guia de Desenvolvimento - LLM Report Module

Este documento é destinado aos desenvolvedores que precisam adicionar novos relatórios corporativos, alterar regras de sumarização matemática ou calibrar o Agente focando no ecossistema do **`llm_report`**.

## 💻 Tecnologias e Dependências Base
* **Python:** `>= 3.11`
* **IA & Orquestração:** `langchain`, `langchain-ollama`, `langgraph-checkpoint-postgres`.
* **Infra & API:** `fastapi`, `psycopg` (driver para PostgreSQL).

## 📂 Arquitetura do Projeto Detalhada

A arquitetura do módulo de relatórios é estritamente dividida por padrões de projeto estruturais (`Factory`, `Builder`, `Repository`) para facilitar a escala e a manutenção de dezenas de relatórios distintos sem ferir o princípio de responsabilidade única (SOLID).

```text
llm_report/
├── pyproject.toml             # Configuração principal (dependências e metadados)
├── main.py                    # Ponto de entrada local (caso executado isoladamente)
└── src/
    ├── llm_report/   
    │   ├── agents/            # Lógica central cognitiva
    │   │   └── report_agent.py      # Agente LangChain com prompts de formatação e Chunking
    │   ├── builders/          # Calculadoras e agregadores (Pré-IA)
    │   │   ├── analysis_builder.py  # Cálculos de saldos, totais e resumos de movimentação
    │   │   └── movement_builder.py  # Estruturação focada em entradas e saídas
    │   ├── database/          # Mapeamento e validação de dados
    │   │   └── schemas.py           # Modelos baseados no banco
    │   ├── formatters/        # Formatação final de saída visual (Templates Markdown/HTML)
    │   │   ├── base_formatter.py    # Classe abstrata para garantir a assinatura de todos os formatadores
    │   │   ├── formatter_factory.py # Ponto de registro de novos relatórios (Factory Pattern)
    │   │   ├── curva_abc_formatter.py
    │   │   └── inventario_formatter.py # (e outros formatadores específicos...)
    │   ├── reports/           # Regras de negócio de extração de dados brutos
    │   │   ├── report_intent.py     # Definição de intenções de relatório
    │   │   ├── report_repository.py # Consultas SQL diretas ao banco de dados
    │   │   └── report_service.py    # Busca e validação dos dados antes de enviar à IA
    │   ├── routers/           # Contratos web
    │   │   └── llm_router.py        # Endpoints FastAPI (/chat, /chat/stream, /sessions)
    │   ├── services/          # Orquestradores de alto nível
    │   │   ├── llm_service.py       # Integração base do chat
    │   │   ├── llm_sessions.py      # CRUD do histórico de sessões
    │   │   └── report_orchestrator.py # Core: Une dados brutos (Service) com formatação (Agent)
    │   ├── tools/             # Acessórios de consulta
    │   │   ├── llm_report_tool.py   # Tooling de relatório para o agente
    │   │   └── sql_tools.py         # Consultas auxiliares pontuais
    │   └── utils/             # Funções de apoio
    │       ├── llm_normalizer.py    # Sanitização de textos e datas
    │       └── postgres_client.py   # Conector direto com o PostgreSQL
    │
    └── prompts/               # Engenharia de Prompt isolada do código
        ├── report_prompts.py        # Dicionário mapeando cada relatório ao seu prompt específico
        ├── chat_bot.md              # Diretrizes de comportamento
        └── summarization.md         # Regras para condensação de textos
```

### 🧠 Guia de Responsabilidades

* **`agents/report_agent.py`**: É o motor da Inteligência Artificial. Este arquivo é crucial porque implementa o "Chunking": ele divide grandes conjuntos de dados (ex: `dados[i:i + self.CHUNK_SIZE]`) em lotes de no máximo 10 registros por vez para impedir que o modelo `llama3.1:8b` estoure a janela de contexto ou comece a alucinar informações. Edite este arquivo se precisar alterar o limite de registros (`MAX_RECORDS = 10000`) ou o *System Prompt* base ("Nunca invente informações").
* **`builders/` (`analysis_builder.py` / `movement_builder.py`)**: **Regra de Ouro: Nunca deixe a LLM fazer matemática.** O `AnalysisBuilder` deve ser usado para iterar listas de dados usando Python puro para descobrir totais de entrada, totais de saída e saldos. O resultado exato dessa soma é enviado para a IA como metadado, garantindo precisão absoluta no relatório financeiro.
* **`formatters/` (`formatter_factory.py`)**: Central de registro e montagem visual. Todas as classes aqui (ex: `InventarioFormatter`, `CurvaABCFormatter`) herdam de um formatador base. Elas pegam os pedaços (chunks) gerados pela IA e costuram em um único arquivo Markdown coeso. Se você criar um novo relatório, deve obrigatoriamente registrá-lo no dicionário `FORMATTERS` do `formatter_factory.py`.
* **`reports/` (`report_service.py` & `report_repository.py`)**: Responsáveis pela *extração da verdade*. O Repositório faz as querries SQL brutas, e o Serviço valida se os dados retornaram vazios ou não.
* **`services/report_orchestrator.py`**: O coração do fluxo. É ele que comanda a dança: 1) Pede os dados brutos ao `report_service`; 2) Verifica se há registros; 3) Formata a requisição; e 4) Chama o `report_agent` instanciando o modelo LLM com `temperature=0` (para evitar criatividade e focar em dados exatos).
* **`prompts/report_prompts.py`**: Local onde as instruções textuais de cada tipo de relatório ficam armazenadas. Em vez de sujar o código Python com strings gigantes de orientação para a LLM, todas as regras de "Como montar o relatório X" devem ser adicionadas neste dicionário centralizado.


## ⚙️ Configurando o Ambiente Local

Como o ecossistema Gestock utiliza o `uv` e `poetry` sob os panos, a preparação do ambiente é extremamente rápida.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `llm_report` (onde está o arquivo `pyproject.toml`), execute:
```bash
uv sync
```

### 2. Ativar o ambiente virtual
**Em ambientes Windows:**
```bash
.venv\Scripts\activate
```
**Em ambientes Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Executando testes locais
Para garantir que a LLM continua formatando relatórios corretamente após alterações nos builders, utilize o Pytest. Na raiz do projeto ativado:
```bash
uv run pytest
```

