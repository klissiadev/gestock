# 🔐 Auth Module - Módulo do Gestock

O **Auth Module** é uma biblioteca de segurança e autenticação desenhada para o ecossistema backend do **Gestock**. Este módulo centraliza as rotinas de registo de utilizadores, login seguro com tokens JWT, controlo de acesso baseado em papéis (RBAC) e fluxos de recuperação de palavra-passe.

> **Vai dar manutenção neste código?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para saber como configurar o ambiente local com o `uv`.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo está dividido em três domínios principais:

* **1. Autenticação e Registo (`UserAuth`)**
  * Cadastro de novos utilizadores com validação rigorosa de campos (e-mail único, tamanho de palavra-passe).
  * Geração de tokens JWT (Access Tokens) compatível com o fluxo `OAuth2PasswordRequestForm`.
  * Cifragem de segurança (hash) de palavras-passe utilizando o algoritmo Argon2 (via `pwdlib`).
* **2. Controlo de Acesso e Gestão (`RBAC & Management`)**
  * Sistema de papéis restrito aos níveis `admin` e `gestor`.
  * Proteção automática de rotas através da dependência `require_role`.
  * Inativação segura de contas (soft delete) exclusiva para administradores, mantendo a integridade do histórico na base de dados.
* **3. Recuperação de Palavra-passe (`RecoveryService`)**
  * Geração de tokens de recuperação dinâmicos e de uso único, baseados no hash da palavra-passe atual.
  * Processamento assíncrono (Background Tasks) para o envio de e-mails em HTML via servidor SMTP do Google.

## 🗄️ Arquitetura da Base de Dados
O módulo otimiza o acesso à base de dados criando um `ConnectionPool` global do pacote `psycopg`. A configuração assegura um mínimo de 1 e um máximo de 15 ligações simultâneas, e faz uso de `dict_row` para devolver os resultados das consultas diretamente como dicionários em vez de tuplas, facilitando a serialização dos dados. 

## 🌐 Endpoints da API REST
Todas as rotas estão prefixadas com `/auth` e são geridas através do FastAPI via importação de `Routers`:

* **Autenticação e Registo:** `POST /auth/register`, `POST /auth/login` e `GET /auth/me`.
* **Gestão de Contas:** `DELETE /auth/users/{user_id}`.
* **Recuperação:** `POST /auth/forgot-password` e `POST /auth/reset-password`.

### 🔌 Como Integrar no Backend Principal

Como o `auth_module` é uma biblioteca interna, ele deve ser adicionado localmente ao projeto principal. O módulo varre automaticamente a árvore de ficheiros em busca do `.env` raiz para carregar as variáveis de base de dados, JWT e SMTP.

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório do backend do Gestock, pode adicionar via linha de comandos:
```bash
poetry add ../auth_module
```

**Alternativa (Adição Manual no Poetry):**
Para refletir alterações do módulo em tempo real no backend sem precisar reinstalar, adicione manualmente no `pyproject.toml` do backend principal:
```toml
[tool.poetry.dependencies]
auth-module = { path = "../caminho/para/auth_module", develop = true }
```
E em seguida, atualize o ambiente correndo:
```bash
poetry install
```

**2. Alternativa (PIP):**
Caso não utilize Poetry no backend ou tenha acontecido algum problema, com o ambiente virtual ativo, instale em modo de edição:
```bash
pip install -e ../auth_module
```

**3. Registando no FastAPI (`app.py`):**
```python
from fastapi import FastAPI

# Importando os roteadores do módulo
from auth_module.routers.user_router import router as user_router
from auth_module.routers.recovery_router import router as recovery_router

app = FastAPI(title="Gestock Backend")

# Conectando as rotas de autenticação
app.include_router(user_router)
app.include_router(recovery_router)
```