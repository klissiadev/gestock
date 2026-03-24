# ⚙️ Admin Module - Módulo do Gestock

O **Admin Module** é uma biblioteca de administração projetada para o ecossistema backend do **Gestock**. Este módulo centraliza as rotinas de monitorização de infraestrutura, auditoria de logs, verificação de saúde dos serviços (Health Checks) e gestão de utilizadores.

> **Vai dar manutenção neste código?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para saber como configurar o ambiente local com o `uv`.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo está dividido em quatro domínios principais:

* **1. Monitorização de Hardware (`HardwareMonitor`)**
  * Captura em tempo real do uso de CPU, RAM e tempo de atividade (uptime) do servidor.
  * Integração avançada com GPUs NVIDIA (via `GPUtil`) para métricas de carga, temperatura e VRAM.
  * Suporte fallback via WMI para placas AMD/Intel em ambientes Windows.
* **2. Saúde do Sistema (`SystemHealth`)**
  * Verificação concorrente da latência e estado operacional das integrações vitais do Gestock:
    * **PostgreSQL:** Validação da pool de conexões.
    * **Ollama (LLM):** Monitorização do motor de Inteligência Artificial local.
    * **Google SMTP:** Teste de disponibilidade para o envio de e-mails.
* **3. Auditoria e Logs (`LogFetcher`)**
  * **Importações:** Rastreamento de falhas e sucessos no processamento de ficheiros no sistema.
  * **Minerva (LLM):** Histórico detalhado de interações (prompts e respostas) entre os utilizadores e a IA.
* **4. Gestão de Utilizadores (`UserService`)**
  * Inativação segura de contas (soft delete) e listagem analítica com suporte a filtros dinâmicos.

## 🗄️ Arquitetura da Base de Dados
O módulo otimiza o acesso à base de dados criando um `ConnectionPool` global. A configuração assegura um máximo de 15 ligações simultâneas e faz uso do evento nativo `atexit` para fechar a pool de forma segura assim que a aplicação é encerrada.

## 🌐 Endpoints da API REST
Todas as rotas estão prefixadas com `/admin` e são geridas através do FastAPI via importação de `Routers`:

* **Status e Monitorização:** `GET /admin/health` e `GET /admin/hardware`.
* **Logs e Auditoria:** `POST /admin/logs/minerva`, `POST /admin/logs/importacao` e `POST /admin/logs/usuarios`.

### 🔌 Como Integrar no Backend Principal

Como o `admin_module` é uma biblioteca interna, ele deve ser adicionado localmente ao projeto principal.

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório do backend do Gestock, você pode adicionar via linha de comando:
```bash
poetry add ../admin_module
```

**Alternativa (Adição Manual no Poetry):**
Para refletir alterações do módulo em tempo real no backend sem precisar reinstalar, adicione manualmente no `pyproject.toml` do backend principal:
```toml
[tool.poetry.dependencies]
admin-module = { path = "../caminho/para/admin_module", develop = true }
```
E em seguida, atualize o ambiente rodando:
```bash
poetry install
```

**2. Alternativa (PIP):**
Caso não utilize Poetry no backend ou tenha acontecido algum problema, com o ambiente virtual ativo, instale em modo de edição:
```bash
pip install -e ../admin_module
```

**3. Registrando no FastAPI (`app.py`):**
```python
from fastapi import FastAPI

# Importando os roteadores do módulo
from admin_module.routers.health_router import router as health_router
from admin_module.routers.status_router import router as status_router
from admin_module.routers.logs_router import router as logs_router

app = FastAPI(title="Gestock Backend")

# Conectando as rotas de administração
app.include_router(health_router)
app.include_router(status_router)
app.include_router(logs_router)
```