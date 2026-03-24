# 🛠️ Guia de Desenvolvimento - Request Module

Este documento é destinado aos desenvolvedores que precisam dar manutenção, modificar os templates de e-mail ou adicionar regras de negócio **exclusivamente dentro do código do `request_module`**.

## 💻 Tecnologias e Dependências Base
* **Python:** `>= 3.11`
* **Dependências Principais:** `fastapi`, `psycopg` (para transações assíncronas no banco), `python-dotenv`, `auth-module`.

## 📂 Arquitetura do Projeto

A arquitetura garante a separação entre os contratos da API, a lógica de roteamento e os serviços de notificação externa:

```text
request_module/
├── pyproject.toml        # Configuração de dependências e metadados
└── src/
    └── request_module/   
        ├── models/       
        │   └── RequestModel.py     # Schemas Pydantic para validação do payload de entrada
        ├── router/      
        │   └── request_router.py   # Definição do endpoint, injeção de dependências e transação com o BD
        ├── templates/     
        │   └── mail_template.yaml  # Configurações de assunto, remetente financeiro e layout HTML do e-mail
        └── utils/        
            ├── env_loader.py       # Carregamento de variáveis de ambiente
            └── mail_sender.py      # Orquestração do envio de e-mails via SMTP
```

### 🧠 Guia de Responsabilidades

* **`models/`**: Todo e qualquer modelo do Pydantic (ex: `RequestItem`, `RequestModel`) utilizado para tipar as requisições deve ficar aqui.
* **`router/`**: Mantém as chamadas HTTP. É responsável por abrir transações assíncronas com o PostgreSQL e despachar tarefas para o plano de fundo (`BackgroundTasks`).
* **`templates/`**: Local onde as mensagens institucionais residem. O `mail_template.yaml` define quem receberá os e-mails (ex: setor financeiro) e a estrutura base do HTML.
* **`utils/`**: Utilitários que interagem com SMTP (`smtplib`) e carregamento de configurações ambientais.

## ⚙️ Configurando o Ambiente Local

Como este projeto utiliza o build system `uv_build` (conforme especificado no seu `pyproject.toml`), o gerenciamento de dependências é altamente otimizado.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `request_module`, execute:
```bash
uv sync
```
*Atenção:* O `request_module` mapeia o `auth-module` como um caminho local (`path = "../auth_module"`). Certifique-se de que a pasta do módulo de autenticação existe no nível superior relativo a este repositório.

### 2. Ativar o ambiente virtual
Para que sua IDE reconheça as importações corretamente:

**Em ambientes Windows:**
```bash
.venv\Scripts\activate
```

**Em ambientes Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Edição de Templates de E-mail
Para alterar o layout do e-mail de requisição, não é necessário alterar o código Python. Basta editar o arquivo `src/request_module/templates/mail_template.yaml`, modificando as chaves `assunto`, `corpo` ou o e-mail em `financeiro_destinatario`.