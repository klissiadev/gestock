# 🛠️ Guia de Desenvolvimento - Admin Module

Este documento é destinado aos desenvolvedores que precisam dar manutenção, criar novas features ou rodar testes **exclusivamente dentro do código do `admin_module`**. Se você quer apenas usar o módulo no Gestock, consulte o [README.md](README.md).

## 📂 Arquitetura do Projeto

O módulo segue uma estrutura baseada em Domain-Driven Design (DDD) simplificado e separação de responsabilidades (Routers, Models, Services).

```text
admin_module/
├── pyproject.toml        # Configuração de dependências (Poetry/uv) e metadados
├── uv.lock               # Ficheiro de lock das versões do uv
└── src/
    └── admin_module/     # Raiz do código fonte do módulo
        ├── models/       # Lógica de negócio e acesso a dados e sistema
        │   ├── hardware_monitor.py
        │   ├── logs_fetcher.py
        │   └── system_health.py
        ├── pydantic/     # Schemas de validação de dados (Input/Output da API)
        │   └── logs_model.py
        ├── routers/      # Definição dos endpoints da API (FastAPI)
        │   ├── health_router.py
        │   ├── logs_router.py
        │   └── status_router.py
        ├── services/     # Casos de uso e regras de negócio complexas
        │   └── user_service.py
        └── utils/        # Ferramentas auxiliares e configurações globais
            ├── database.py
            └── env_loader.py
```

## 💻 Tecnologias e Dependências Base
* **Python:** `>= 3.11`
* **Dependências Principais:** `fastapi`, `psycopg`, `psycopg-pool`, `psutil`, `gputil`, `wmi`, `requests`.

## ⚙️ Configurando o Ambiente Local

O gerenciamento de dependências e do ambiente virtual interno deste módulo é feito através do gerenciador ultra-rápido **uv**.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `admin_module` (onde está o arquivo `pyproject.toml`), execute o comando abaixo para que o uv crie o `.venv` e baixe os pacotes:
```bash
uv sync
```

### 2. Ativar o ambiente virtual
Para que a sua IDE ou o seu terminal reconheçam as dependências instaladas, ative o ambiente:

**Em ambientes Windows:**
```bash
.venv\Scripts\activate
```

**Em ambientes Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Executando scripts isoladamente
Caso precise rodar testes internos ou executar arquivos específicos dentro do escopo do módulo para verificar o funcionamento de uma classe (ex: testar o `SystemHealth` ou `HardwareMonitor`):
```bash
uv run <caminho_para_o_script.py>

# Exemplo de teste do monitor de hardware:
uv run src/admin_module/models/hardware_monitor.py
```
