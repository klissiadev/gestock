# 📊 LLM Report Module - Gerador de Relatórios com IA

O **LLM Report Module** é a biblioteca de inteligência artificial do **Gestock** dedicada exclusivamente à formatação, sumarização e geração de relatórios avançados. Utilizando um modelo focado no processamento de dados (como o `llama3.1:8b`), este módulo transforma listagens massivas de banco de dados em relatórios gerenciais organizados e de fácil leitura.

> **Vai dar manutenção neste código ou criar novos layouts de relatório?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para entender a arquitetura de Agentes, Builders e Formatters.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo foi desenhado para processar grandes volumes de dados sem estourar o limite de tokens da LLM, operando sob uma arquitetura de orquestração:

* **1. Orquestração de Relatórios (`ReportOrchestratorService`)**
  * Recebe o tipo de relatório desejado e seus parâmetros, aciona os repositórios para buscar os dados brutos e valida a integridade das informações antes de invocar a IA.
* **2. Agente Especializado em Dados (`ReportAgent`)**
  * Utiliza a LLM `llama3.1:8b` (via `ChatOllama` com temperatura = 0 para máxima precisão determinística).
  * Implementa um sistema de processamento em *Chunks* (lotes de 10 em 10 registros, até o limite de 10.000) para evitar alucinações da IA em datasets muito grandes.
  * Possui *System Prompts* estritos ("Nunca invente informações", "Nunca interprete dados") garantindo que o relatório contenha apenas a verdade do banco de dados.
* **3. Motores de Cálculos e Análises (`AnalysisBuilder`)**
  * Realiza sumarizações matemáticas pré-IA (como o cálculo de total de entradas, saídas e saldo líquido de movimentações) para injetar métricas exatas no relatório.
* **4. Fábrica de Formatadores (`formatter_factory`)**
  * Suporta múltiplos domínios de relatório, incluindo: Inventário, Estoque Baixo, Saldo, Movimentação por Período, Curva ABC, Giro de Estoque, Validade Próxima, entre outros.

## 🌐 Endpoints da API REST
O módulo expõe as seguintes rotas via FastAPI para interagir com o gerador de relatórios e suas sessões:

* **Chat (Síncrono e Streaming):** `POST /chat` e `POST /chat/stream` (para receber o relatório em tempo real).
* **Gestão de Sessões:** `GET /sessions`, `POST /sessions` e `GET /sessions/{session_id}/messages` para resgatar o histórico de relatórios de uma sessão específica.

## 🔌 Como Integrar no Backend Principal

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório raiz do backend do Gestock, instale o pacote localmente:
```bash
poetry add ../llm_report
```

**Alternativa (Adição Manual no `pyproject.toml`):**
Para garantir o hot-reload de edições locais sem reinstalação:
```toml
[tool.poetry.dependencies]
llm_report = { path = "../caminho/para/llm_report", develop = true }
```
Sincronize o ambiente rodando `poetry install`.

**2. Registrando no FastAPI (`main.py`):**
```python
from fastapi import FastAPI
from llm_report.routers.llm_router import router as report_router

app = FastAPI(title="Gestock Backend")
# Sugestão: prefixar com /report ou /analytics para separar do llm_module convencional
app.include_router(report_router, prefix="/report")
```
