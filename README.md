# 📦 Gestock: Sistema Inteligente de Gestão de Estoque

  <p align="center">
  <img src="https://img.shields.io/github/repo-size/klissiadev/gestock?style=for-the-badge" alt="GitHub repo size">
  <img src="https://img.shields.io/github/languages/count/klissiadev/gestock?style=for-the-badge" alt="GitHub language count">
</p>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=react,postgres,python,fastapi,js,vite,tailwind,docker" />
  </a>
</p>

<p align="center">
  <img src="https://media.istockphoto.com/id/1138429558/pt/foto/rows-of-shelves.jpg?s=612x612&w=0&k=20&c=Q_IQ0T-vjlcsCPUrQj79xkifkD6nhmjWNAQQ4WQwHgo=" alt="Imagem do gestock">
  <br>creditos: istockphoto
</p>

O **Gestock** é uma plataforma avançada de gerenciamento de estoque que integra o poder da Inteligência Artificial (LLMs) e Machine Learning para transformar dados operacionais em insights estratégicos. O sistema automatiza processos, prevê demandas e oferece uma interface conversacional para consulta de dados complexos.

-----


### ⚠️ Status do Projeto
> 🚧 **Em Desenvolvimento:** Este projeto encontra-se em **fase beta**. Não é recomendado utilizá-lo em produção neste momento.

-----

## ✨ Funcionalidades Principais

  * **📊 Dashboards em Tempo Real:** Visualização clara de fluxos de entrada, saída e níveis de estoque.
  * **🤖 Chatbot Minerva (LLM):** Interface em linguagem natural para consultas ao banco de dados e geração de relatórios.
  * **📈 Previsão de Demanda (Forecasting):** Modelos de Machine Learning que antecipam necessidades de reposição.
  * **⚠️ Alertas Inteligentes:** Notificações automáticas sobre validade próxima e estoque baixo.
  * **📂 Importação Automatizada:** Processamento de planilhas CSV para atualização rápida de produtos e movimentações.
  * **🔐 Segurança e Administração:** Controle de acesso robusto com módulos dedicados de autenticação e monitoramento de hardware.

-----

## 🏗️ Arquitetura do Projeto

O sistema é dividido em módulos independentes para garantir escalabilidade e manutenção facilitada:

1.  **Backend (Core):** API central responsável pela lógica de negócio e persistência.
2.  **Frontend:** Interface web moderna e responsiva.
3.  **Auth Module:** Gerenciamento de usuários e segurança.
4.  **Forecasting Module:** Inteligência preditiva para análise de estoque.
5.  **LLM Module:** O "cérebro" do sistema, processando comandos em linguagem natural.
6.  **Admin/Request/Report Modules:** Ferramentas auxiliares para gestão e automação.

-----

## 🚀 Guia de Implementação

### 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:
  * [Python 3.11+](https://www.python.org/)
  * [Node.js 18+](https://nodejs.org/)
  * [PostgreSQL](https://www.postgresql.org/)
  * [Poetry](https://www.google.com/search?q=https://python-poetry.org/docs/%23installation) (para o Backend)
  * [uv](https://github.com/astral-sh/uv) (para os demais módulos Python)
  * [Vite](https://v7.vite.dev/) (para o frontend)
  * [Git](https://git-scm.com)

-----

### 🔧 Passo a Passo

#### 1\. Configuração do Banco de Dados

Crie uma instância do PostgreSQL e execute os scripts localizados em:
`docs/database/only_schemas.sql` (ou `database_testing.sql` para dados iniciais).

#### 2\. Configuração do Backend

```bash
cd backend
poetry install
cp .env.example .env # Configure suas credenciais de banco e chaves de API
task run
```

#### 3\. Configuração dos Módulos Python (uv)

Para cada módulo (`auth_module`, `llm_module`, `forecasting_module`, etc.), execute:

```bash
cd <nome_do_modulo>
uv sync
uv run main.py # ou o ponto de entrada específico do módulo
```

#### 4\. Configuração do Frontend (Vite)

```bash
cd frontend
npm install
npm run dev
```

#### Melhores informações, leia os README e Guias de desenvolvimento

-----

## ⚙️ Configuração das Variáveis de Ambiente

O projeto utiliza arquivos `.env` para centralizar as configurações. Para que os módulos se comuniquem corretamente, certifique-se de definir as seguintes variáveis:

### 🗄️ Banco de Dados (PostgreSQL)
O sistema utiliza diferentes prefixos para garantir que os módulos (Core, Admin e LLM) acessem as instâncias corretas do banco.
```env
# URL de conexão principal (SQLAlchemy/Geral)
DATABASE_URL=postgresql://postgres:12345@localhost/gestock
SSLMODE=disable

# Configurações para o Módulo de Administração
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=gestock
PG_USER=postgres
PG_PASSWORD=12345

# Configurações para o Módulo de LLM (Minerva)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestock
DB_LLM_USER=postgres
DB_LLM_PASSWORD=12345
```

### 🔐 Segurança e Autenticação
Essas variáveis controlam a geração de tokens de acesso e a segurança das sessões de usuário.
```env
SECRET_KEY='CHAVE SECRETA MUITO LEGAL' # Altere para uma string aleatória em produção
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 📧 Serviço de E-mail (SMTP)
Configuração necessária para o envio de notificações de estoque e recuperação de senha.
```env
SMTP_SERVER=smtp.gmail.com
TLS_PORT=587
EMAIL=email@da_corporacao.com
PASSWORD=senha_gerada_para_o_servidor_SMTP # Senha de App (no caso do Gmail)
```

### 🤖 Inteligência Artificial (Módulo LLM)
Configurações que definem o comportamento e os limites do chatbot Minerva.
```env
# Caminho para o arquivo de instrução do sistema
SYSTEM_PROMPT_LOCATION=llm_module\src\prompts\chat_bot.md

# Limite de tokens/caracteres para evitar estouro de contexto
MAX_INPUT_SIZE=4000
```

---

### 💡 Dica de Implementação
Para facilitar a gestão, você pode criar um arquivo `.env` global na raiz do projeto e criar links simbólicos em cada pasta de módulo, ou simplesmente copiar o arquivo para dentro das pastas `backend/`, `llm_module/`, `auth_module/`, etc.

**Lembre-se:** Nunca envie o arquivo `.env` para repositórios públicos. O arquivo `.env.example` já está disponível no projeto como guia.

-----

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
  <td align="center">
      <a href="#" title="Antonio Gabriel">
        <img src="https://imgur.com/Gc0pH7H.png" width="100px;"  height="100px;" alt="Foto de Antonio Gabriel"/><br>
        <sub>
          <b>Antonio Gabriel</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Ana Klissia">
        <img src="https://i.imgur.com/0EMpIgW.png" width="100px;"  height="100px;" alt="Foto de Ana Klissia"/><br>
        <sub>
          <b>Ana Klissia</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Thais Carolina">
        <img src="https://i.imgur.com/7BpjjOZ.jpeg" width="100px;"  height="100px;" alt="Foto de Thais Carolina"/><br>
        <sub>
          <b>Thais Carolina</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o título do link">
        <img src="https://imgur.com/zhZzhiQ.png" width="100px;" height="100px;" alt="Foto de Julio Cleiton"/><br>
        <sub>
          <b>Júlio Cleiton</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Erick Roberto">
        <img src="https://imgur.com/QIKonAp.png" width="100px;"  height="100px;" alt="Foto de Erick Roberto"/><br>
        <sub>
          <b>Erick Roberto</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Gabriel Ribeiro">
        <img src="https://t4.ftcdn.net/jpg/17/79/86/53/360_F_1779865388_fomebP6faaqwzY8HV7US4CPywz9ryYVM.jpg" width="100px;"  height="100px;" alt="Foto de Gabriel Ribeiro"/><br>
        <sub>
          <b>Gabriel Ribeiro</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

*Desenvolvido com foco em eficiência e inteligência de dados.*
