# 🧠 LLM Module - Módulo de IA do Gestock

O **LLM Module** é a biblioteca central de Inteligência Artificial do **Gestock**. Este módulo é o motor por trás da "Minerva" (a assistente virtual do sistema), responsável por processar linguagem natural, classificar intenções do usuário, buscar dados no banco via ferramentas (Tools) e orquestrar conversas síncronas e em streaming.

> **Vai dar manutenção neste código ou criar novas ferramentas (Tools)?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para saber como configurar o ecossistema LangChain localmente.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo funciona como um ecossistema completo de IA baseado em Agentes:

* **1. Agente Conversacional e Ferramentas (`ChatBotService` & `sql_tools`)**
  * Utiliza o modelo `qwen2.5:7B` (via Ollama) como motor de raciocínio principal.
  * O Agente possui acesso a um catálogo de ferramentas (Tools) para interagir com o banco de dados em tempo real (ex: `tool_buscar_produto`, `tool_listar_movimentacoes`, `buscar_produtos_a_vencer`) utilizando buscas semânticas e normalização textual.
  * Integra um modelo menor (`gemma3:1b`) exclusivamente para atuar como middleware de sumarização e economizar tokens de contexto.
* **2. Roteamento Inteligente de Intenções (`MinervaGateway`)**
  * Antes de processar a resposta, classifica a intenção do usuário (`IntentClassifier`). Se o usuário solicitar um relatório, a requisição é desviada para o serviço especializado em relatórios (`ReportLLMService`); caso contrário, segue o fluxo conversacional padrão.
* **3. Persistência de Memória (`Checkpointer`)**
  * Mantém o histórico e contexto das conversas (memória) salvo diretamente no PostgreSQL utilizando a biblioteca `langgraph-checkpoint-postgres`.
* **4. Auditoria e Background Tasks (`LLMService`)**
  * Gera títulos automaticamente para as sessões de chat em segundo plano e salva logs de auditoria de cada interação utilizando transações assíncronas para não bloquear a resposta ao usuário.

## 🔒 Dependências Internas
Este módulo é uma peça central e interage com dois outros pacotes locais:
* **`auth-module`**: Protege os endpoints garantindo que apenas usuários com a role `gestor` acessem o chat.
* **`llm-report`**: Módulo acionado pelo Gateway caso o usuário deseje gerar relatórios avançados.

## 🌐 Endpoints da API REST
O módulo expõe as seguintes rotas via FastAPI (todas sob o prefixo `/llm`):

* **Chat Síncrono e Streaming:** `POST /llm/chat` e `POST /llm/chat/stream`.
* **Sessões:** `GET /llm/sessions`, `POST /llm/sessions`, e consultas de histórico de mensagens e título das sessões.

## 🔌 Como Integrar no Backend Principal

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório do backend do Gestock, adicione:
```bash
poetry add ../llm_module
```

**Alternativa (Adição Manual no `pyproject.toml`):**
```toml
[tool.poetry.dependencies]
llm_module = { path = "../caminho/para/llm_module", develop = true }
```
E sincronize o ambiente com `poetry install`.

**2. Registrando no FastAPI (`main.py`):**
```python
from fastapi import FastAPI
from llm_module.routers.llm_router import router as llm_router

app = FastAPI(title="Gestock Backend")
app.include_router(llm_router)
```