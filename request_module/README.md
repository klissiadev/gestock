# 🛒 Request Module - Módulo do Gestock

O **Request Module** é uma biblioteca interna construída para o ecossistema backend do **Gestock**. Este módulo é estritamente responsável por gerenciar a criação de requisições de compra, orquestrar transações no banco de dados e notificar o setor financeiro de forma automatizada via e-mail.

> **Vai dar manutenção neste código?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para saber como configurar o ambiente local e entender a arquitetura.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo é projetado para lidar com o fluxo completo de uma requisição de produtos:

* **1. Criação de Requisições de Compra (`RequestModel`)**
  * Recebe payloads contendo o título, observações e uma lista de itens (produtos, quantidade e prioridade).
  * Garante a consistência dos dados inserindo a requisição e seus itens no banco de dados (`app_core.requisicoes` e `app_core.itens_requisicoes`) utilizando transações assíncronas.
* **2. Sistema de Notificações e Eventos**
  * Integra-se com o `EventService` do backend para gerar eventos de sistema (tipo `SUCCESS`) sempre que uma nova requisição é criada com sucesso.
* **3. Disparo Automatizado de E-mails (`mail_sender`)**
  * Utiliza o `BackgroundTasks` do FastAPI para buscar os nomes dos produtos no banco de forma assíncrona e compilar um e-mail sem travar a resposta da requisição original.
  * Renderiza e-mails em HTML dinâmicos baseados num template YAML para notificar o setor financeiro.

## 🔒 Dependências Internas
Este módulo depende diretamente de outro pacote interno do Gestock:
* **`auth-module`**: Utilizado para proteger a rota de requisições, garantindo que apenas usuários autenticados (`get_current_user`) possam solicitar compras.

## 🌐 Endpoints da API REST
O módulo expõe as seguintes rotas via FastAPI:

* **Criação:** `POST /requisicoes/` - Rota protegida (requer usuário autenticado) que processa e salva a requisição, retornando o ID do banco em caso de sucesso.

## 🔌 Como Integrar no Backend Principal

Como o `request_module` é uma biblioteca local, ele deve ser adicionado ao projeto principal prestando atenção à sua dependência do `auth_module`.

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório do backend do Gestock, adicione o módulo via CLI:
```bash
poetry add ../request_module
```

**Alternativa (Adição Manual no `pyproject.toml`):**
Para garantir que o backend reflita alterações em tempo real, adicione:
```toml
[tool.poetry.dependencies]
request-module = { path = "../caminho/para/request_module", develop = true }
```
E não esqueça de sincronizar o ambiente executando:
```bash
poetry install
```

**2. Registrando no FastAPI (`main.py`):**
```python
from fastapi import FastAPI

# Importando o roteador do módulo
from request_module.router.request_router import router as request_router

app = FastAPI(title="Gestock Backend")

# Conectando a rota de requisições
app.include_router(request_router)
```