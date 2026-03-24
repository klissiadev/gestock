# ⚙️ Gestock - Backend

O backend do **Gestock** é uma API robusta construída com **FastAPI**, desenhada para ser o núcleo de um sistema avançado de gestão de inventário. Ele atua como um orquestrador central, integrando módulos de inteligência artificial, análise preditiva e monitorização de infraestrutura.

> **Vai dar manutenção neste código?** Leia o nosso [Guia de Desenvolvimento](DEVELOPMENT.md) para saber como configurar o ambiente local com o `poetry`.

A estrutura do projeto está dividida em duas camadas fundamentais:

* 🛠️ **Recursos Nativos**: Representam as funcionalidades essenciais integradas diretamente ao núcleo do backend, responsáveis pela operação transacional básica:
* 🧩 **Módulos Integrados**: bibliotecas internas especializadas que garantem a escalabilidade da plataforma.

## 💻 Setup do Ambiente (Poetry)

Este projeto utiliza o **Poetry** para gestão de dependências e ambientes virtuais.

### 1. Instalação de Ferramentas
Caso ainda não tenha o Poetry instalado via `pipx`:
```bash
pip install --user pipx
pipx install poetry
pipx inject poetry poetry-plugin-shell
```

### 2. Configuração e Ativação
Dentro do diretório `/backend`:
1.  **Instalar dependências**: `poetry install`.
2.  **Ativar o ambiente virtual**:
    * **Opção A**: `poetry shell`.
    * **Opção B**: `iex (poetry env activate)` (para ativação direta no terminal atual, dependendo da sua preferência).
3.  **Executar o projeto**: `task run`.

---

## 🚀 Recursos Principais (API Core)

A API fornece endpoints essenciais para a operação do dia a dia:

### 📦 Gestão de Produtos (`/produtos`)
* **Cadastro**: Criação de novos itens no catálogo.
* **Listagem**: Recuperação de todos os produtos cadastrados.
* **Busca Específica**: Consulta de nome de produto por ID.

### 🔄 Movimentações de Estoque (`/movimentacoes`)
Gerencia o fluxo físico de materiais através de três frentes:
* **Entradas**: Registro e listagem de novos suprimentos.
* **Saídas**: Registro e listagem de baixas de estoque.
* **Interna**: Registro de transferências ou ajustes entre locais de armazenamento.

### 📊 Analytics e KPIs (`/analytics`)
Visões estratégicas baseadas nos dados de movimentação:
* **Visão Geral**: Saldo total de estoque e divisão por tipo de material.
* **Alertas Críticos**: Identificação de produtos com estoque baixo ou em risco.
* **Desempenho de Vendas**: Relatórios mensais de vendas e ranking de "Top Produtos".
* **KPIs Financeiros**: Indicadores financeiros mensais detalhados por período.

---

## 🚀 Módulos Integrados

O sistema é composto por bibliotecas internas especializadas que garantem a escalabilidade da plataforma:

### 🔐 Módulo de Autenticação (`auth_module`)
Centraliza a segurança do ecossistema:
* **Identidade**: Registo e login com tokens JWT e cifragem Argon2.
* **Controle de Acesso**: Sistema RBAC para níveis `admin` e `gestor`.
* **Recuperação**: Fluxo de palavra-passe com envio de e-mail via SMTP Google.

### 🧠 Módulo de IA - Minerva (`llm_module`)
O motor de inteligência artificial conversacional:
* **Assistente**: Baseada em `qwen2.5:7B` para processamento de linguagem natural.
* **Tools**: Capacidade de consultar o banco de dados em tempo real para buscar produtos e movimentações.
* **Memória**: Persistência de contexto de chat diretamente no PostgreSQL.

### 📊 Módulo de Relatórios (`llm_report`)
Especializado em transformar dados massivos em relatórios gerenciais:
* **Processamento**: Utiliza `llama3.1:8b` com técnica de *Chunks* para evitar alucinações em grandes volumes.
* **Análises**: Geração automática de Curva ABC, Giro de Estoque e Inventário.

### 📉 Módulo de Previsão (`forecasting_module`)
Inteligência preditiva para o estoque:
* **Modelagem**: Utiliza `darts` e `scikit-learn` para prever a procura futura de produtos.

### 🛒 Módulo de Requisições (`request_module`)
Gere o fluxo de reposição de materiais:
* **Automação**: Criação de pedidos de compra com notificação automática por e-mail ao setor financeiro.
* **Integração**: Estritamente protegido por permissões do módulo de autenticação.

### 🛠️ Módulo Administrativo (`admin_module`)
Monitorização e saúde do sistema:
* **Hardware**: Captura em tempo real de uso de CPU, RAM e telemetria de GPUs.
* **Health Checks**: Verificação de latência do banco de dados e disponibilidade do motor de IA.

---

## 🛠️ Comandos Úteis (Taskipy)

Automatize tarefas comuns de desenvolvimento:
* `task lint`: Verifica boas práticas de código com Ruff.
* `task format`: Aplica formatação automática.
* `task test`: Executa a suíte de testes com relatório de cobertura.
