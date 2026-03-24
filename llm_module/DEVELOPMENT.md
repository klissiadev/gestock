
***
**Autoria:** Thais Carolina Braga de Magalhães | **Projeto:** Gestock
```

---

### Arquivo 2: `DEVELOPMENT.md`
*(Focado exclusivamente nas instruções para quem vai alterar o motor de IA do Gestock).*

```markdown
# 🛠️ Guia de Desenvolvimento - LLM Module (Minerva)

Este documento é destinado aos desenvolvedores que precisam calibrar os prompts da Inteligência Artificial, adicionar novas ferramentas (Tools) para o agente ou ajustar o middleware de sumarização **exclusivamente dentro do código do `llm_module`**.

## 💻 Tecnologias e Dependências Base
* **Python:** `>= 3.11`
* **IA & Orquestração:** `langchain`, `langchain-ollama`, `langgraph-checkpoint-postgres`.
* **Core & BD:** `fastapi`, `psycopg` (driver assíncrono para PostgreSQL).
* **Dependências Locais:** O desenvolvimento requer que as pastas `auth_module` e `llm_report` estejam acessíveis no diretório pai.

## 📂 Arquitetura do Projeto

A arquitetura isola os contratos de API, as regras do Agente, as integrações de BD e a auditoria:

```text
llm_module/
├── pyproject.toml        
└── src/
    └── llm_module/   
        ├── audit/        # Gravação de logs de interação com a LLM
        ├── database/     # Configuração do Checkpointer (LangGraph) para persistência de memória
        ├── models/       # Configuração do Agente (ChatOllama), Middleware de Sumarização e Classificadores
        ├── routers/      # Endpoints HTTP FastAPI e injeção de dependências web
        ├── services/     # Orquestradores principais (Gateway, Serviço de LLM e Gestão de Sessões)
        ├── tools/        # Ferramentas Python/SQL (@tool) que ensinam a IA a consultar o Gestock
        └── utils/        # Configurações de ambiente e clientes de banco de dados
```

### 🧠 Guia de Responsabilidades Focadas

* **`src/llm_module/models/`**: É onde reside a lógica "cognitiva". Alterações na temperatura, escolha do modelo base (ex: trocar de *qwen* para *llama*) ou lógicas de raciocínio devem ser feitas aqui.
* **`src/llm_module/tools/`**: Adicione novas funções decoradas com `@tool` sempre que a IA precisar consultar uma nova tabela ou dado financeiro do Gestock.
* **`src/prompts/`**: Mantenha o System Prompt fora do código Python. Para ajustar o tom de voz da Minerva ou as regras de negócio que ela deve obedecer por padrão, edite os arquivos `.md` desta pasta.
* **`src/llm_module/services/`**: Esta camada serve como "cola". O `MinervaGateway` (`router_service.py`) intercepta o request web, chama o `intent_classifier`, e decide se manda pro `llm_service` ou para o módulo de relatórios externo.
* **`tests/`**: Antes de subir qualquer alteração nos prompts ou ferramentas, adicione a nova intenção no `test_cases.json` e valide rodando `uv run tests/test.py`.


## ⚙️ Configurando o Ambiente Local

Como este projeto utiliza o build system para múltiplos pacotes locais, o uso do `uv` é altamente recomendado para gestão rápida do ambiente.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `llm_module`, execute:
```bash
uv sync
```
*Atenção:* O `pyproject.toml` mapeia o `auth-module` e `llm-report` como caminhos locais. Certifique-se de que essas pastas existem na mesma raiz do seu monorepo/diretório de trabalho.

### 2. Ativar o ambiente virtual
**Em ambientes Windows:**
```bash
.venv\Scripts\activate
```
**Em ambientes Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Ajustando o Prompt de Sistema
A personalidade da Minerva não está chumbada no código. O Agente carrega dinamicamente seu `System Prompt` a partir de um arquivo externo apontado pela variável de ambiente configurada na inicialização do sistema. Para alterar o comportamento base da IA, edite o arquivo de Markdown correspondente (normalmente em `src/prompts/chat_bot.md`).
```

---

E, para completar o pacote com chave de ouro, aqui está a sugestão ideal de descrição para o seu ficheiro `pyproject.toml` deste módulo:

**Sugestão de Descrição para o `pyproject.toml`:**
```toml
description = "Módulo base da inteligência artificial (Minerva) do Gestock, responsável por roteamento de intenções, chamadas a ferramentas de banco de dados e gestão conversacional."
```