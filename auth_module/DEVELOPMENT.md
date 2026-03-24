# 🛠️ Guia de Desenvolvimento - Auth Module

Este documento é destinado aos desenvolvedores que precisam dar manutenção, criar novas features ou rodar testes **exclusivamente dentro do código do `auth_module`**. Se você quer apenas usar o módulo no Gestock, consulte o [README.md](README.md).

## 💻 Tecnologias e Dependências Base
* **Python:** `>= 3.11`
* **Dependências Principais:** `fastapi[standard]`, `psycopg[binary,pool]`, `pwdlib[argon2]`, `pyjwt`, `python-dotenv`.

## 📂 Arquitetura do Projeto

O módulo segue uma estrutura de separação de responsabilidades limpa, organizando o código em rotas, esquemas de dados e utilitários de infraestrutura (Routers, Models, Utils).

```text
auth_module/
├── pyproject.toml        # Configuração de dependências (Poetry/uv) e metadados
├── uv.lock               # Ficheiro de lock das versões do uv
└── auth_module/          # Raiz do código fonte do módulo
    ├── models/           # Schemas de validação de dados (Input/Output da API)
    │   └── User.py
    ├── routers/          # Definição dos endpoints da API REST (FastAPI)
    │   ├── recovery_router.py
    │   └── user_router.py
    ├── templates/        # Ficheiros estáticos e de configuração
    │   └── recovery_template.yaml
    ├── utils/            # Funções utilitárias, segurança e conexões persistentes
    │   ├── database.py
    │   ├── env_loader.py
    │   ├── mail_service.py
    │   └── security.py
    └── main.py           # Ponto de entrada para testes locais e registo das rotas
```

### 🧠 Entendendo as Camadas (Sistema de Pastas)
* **`models/`**: Contém os esquemas Pydantic que validam rigorosamente os dados de entrada e saída (ex: `UserCreate`, `UserPublic`) e os modelos internos que representam os dados na base de dados (`UserDB`).
* **`routers/`**: Controladores que definem os endpoints da API. Estão divididos por domínio de negócio:
  * `user_router.py`: Lida com o registo, login OAuth2, listagem de perfil e inativação de contas (soft delete).
  * `recovery_router.py`: Orquestra o fluxo de esquecimento e redefinição de palavra-passe.
* **`templates/`**: Armazena os ficheiros de configuração e os templates baseados em YAML/HTML utilizados para a formatação das mensagens de e-mail enviadas aos utilizadores.
* **`utils/`**: A espinha dorsal da infraestrutura do módulo. Agrupa lógicas que interagem com o sistema ou recursos externos:
  * `database.py`: Gere o pool de ligações (`ConnectionPool`) com o PostgreSQL de forma persistente.
  * `security.py`: Trata do hashing de palavras-passe com Argon2 e da emissão/validação de tokens JWT.
  * `mail_service.py`: Lida com o motor de envio de e-mails via SMTP do Google.
  * `env_loader.py`: Garante que o ficheiro `.env` seja encontrado e carregado automaticamente, independentemente de onde o script seja executado.

## ⚙️ Configurando o Ambiente Local

O gerenciamento de dependências e do ambiente virtual interno deste módulo é feito através do **uv**.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `auth_module` (onde está o arquivo `pyproject.toml`), execute o comando abaixo para que o uv crie o `.venv` e baixe os pacotes:
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
Caso precise rodar testes internos ou executar arquivos específicos dentro do escopo do módulo para verificar o funcionamento de uma classe ou função (ex: testar o disparo de e-mails em `mail_service.py` ou a criação de hashes em `security.py`):
```bash
uv run <caminho_para_o_script.py>
```