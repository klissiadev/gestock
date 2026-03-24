# 📄 README – Banco de Dados Gestock

## 📌 Descrição
Este diretório contém os scripts SQL necessários para a inicialização e teste do banco de dados do sistema **Gestock**.

Os arquivos disponíveis são:

1.  **`only_schemas.sql`**: Contém apenas a definição da estrutura (DDL), incluindo:
    * Criação de **tabelas** e relacionamentos.
    * Definição de **views** e **materialized views**.
    * Criação de **functions** e **triggers** (incluindo o refresh automático das views).
    * *Ideal para produção ou ambientes limpos.*

2.  **`database_testing.sql`**: Contém a estrutura completa + **dados mockados** (DML), incluindo:
    * Toda a estrutura do arquivo anterior.
    * Registros de teste para todas as tabelas.
    * Usuários pré-cadastrados com e-mails higienizados para validação de fluxos.
    * *Ideal para desenvolvedores e homologação.*
    * Usuario Admin padrão: `email-falso2@teste.com`
    * Senha Admin padrão: `Senha123`

---

## 🚀 Como carregar os arquivos

### Usando pgAdmin 4
1.  Conecte-se ao servidor PostgreSQL.
2.  Crie um banco de dados vazio chamado `gestock`.
3.  Clique com o botão direito no banco `gestock` → **Query Tool**.
4.  Vá em **File → Open...** e selecione o arquivo desejado (`only_schemas.sql` ou `database_testing.sql`).
5.  Clique em **Execute (F5 ou ícone de raio)**.

### Usando linha de comando (psql)
```bash
# Para carregar apenas a estrutura
psql -h <host> -U <usuario> -d gestock -f only_schemas.sql

# Para carregar estrutura + dados de teste
psql -h <host> -U <usuario> -d gestock -f database_testing.sql
```

---

## ⚠️ Observações importantes

* **Sem Roles/Owners:** Os arquivos foram gerados sem definições de `OWNER` ou `PRIVILEGES`. Os objetos pertencerão ao usuário que executar o script.
* **Nome do Banco:** O sistema está configurado para buscar o banco de nome `gestock`.
* **Permissões:** O Gestock utiliza um único usuário com permissão geral configurado via `.env`. Certifique-se de que este usuário tenha permissão de `SUPERUSER` ou seja o dono dos schemas para que os triggers de refresh das Materialized Views funcionem corretamente.
* **Triggers de Refresh:** Os triggers foram incluídos para garantir a consistência dos dados em tempo real. Em ambientes de altíssimo volume, monitore o impacto de performance nos disparos de `REFRESH MATERIALIZED VIEW`.
* **Dados Sensíveis:** No arquivo de teste, todos os e-mails reais foram substituídos por endereços fictícios por motivos de segurança e privacidade.
---

## 📊 Estrutura Técnica
* **Engine:** PostgreSQL 12+
* **Componentes:** Tabelas, Views, Materialized Views e Triggers PL/pgSQL.
* **Segurança:** Senhas no ambiente de teste utilizam hash Argon2id (compatível com a biblioteca de autenticação do sistema).