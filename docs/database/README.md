# 📄 README – Estrutura do Banco de Dados (schema.sql)

## 📌 Descrição
Este arquivo contém a definição da estrutura do banco de dados utilizada pelo Gestock, incluindo:
- Criação de **tabelas**  
- Definição de **views**  
- Criação de **triggers** para manter as views materializadas atualizadas  

O objetivo é fornecer um script simples e portátil para recriar a estrutura do banco em qualquer ambiente PostgreSQL para o pleno funcionamento do Gestock

---

## 🚀 Como carregar o arquivo

### Usando pgAdmin 4
1. Conecte-se ao banco desejado.  
2. Clique com o botão direito → **Query Tool**.  
3. Vá em **File → Open...** e selecione `schema.sql`.  
4. Clique em **Execute (ícone de raio)** para rodar o script.  

### Usando linha de comando (psql)
```bash
psql -h <host> -U <usuario> -d <dbname> -f schema.sql
```

---

## ⚠️ Observações importantes
- Este arquivo **não contém roles nem owners**.  
- O sistema **Gestock depende de um único usuário com permissão geral** para executar todas as operações (inserções, consultas e manutenção).  
  - Certifique-se de rodar o script conectado com esse usuário, sabendo suas credenciais.  
  - Essas credenciais devem ser **configuradas no arquivo `.env` do sistema**, para que o Gestock consiga acessar o banco de dados corretamente.  
  - Caso contrário, as tabelas, views e triggers podem ser criadas sem permissões adequadas e o Gestock não terá acesso às mesmas.  
- Se precisar definir permissões específicas, faça isso manualmente após rodar o script.  
- Os triggers de refresh foram incluídos para manter as views materializadas consistentes.  
  - Avalie o impacto de performance se houver grande volume de dados.  

---

## 📊 Estrutura esperada
- **Tabelas**: definidas com `CREATE TABLE ...`  
- **Views**: `CREATE VIEW ...`  
- **Triggers**: funções PL/pgSQL que disparam `REFRESH MATERIALIZED VIEW`  

---
