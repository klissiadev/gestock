# Gestock - Gerador de Dados Mockados para PCP

Este repositório contém o motor de simulação de dados para o sistema **Gestock**. O objetivo é gerar planilhas e dados realistas de planejamento e controle de produção (PCP), cobrindo todo o ciclo de vida de um produto: desde a previsão de demanda e compra de matéria-prima até a produção interna e venda final.

## 🚀 Visão Geral

O gerador simula um ambiente industrial de 12 meses, processando mês a mês as necessidades de estoque baseadas em sazonalidade e fichas técnicas (BOM).

### Fluxo de Dados
1.  **Demanda:** Previsão de vendas para Produtos Acabados (PA) com base em sazonalidade.
2.  **MRP (Necessidades):** Cálculo de quanto de Matéria-Prima (MP) e Semiacabados (SA) é necessário.
3.  **Compras:** Geração de pedidos de compra para suprir as MPs faltantes.
4.  **Produção:** Execução de Ordens de Produção (OPs) e movimentações internas.
5.  **Vendas:** Consumo do estoque de PA e registro de saídas financeiras.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas:** Manipulação de DataFrames e lógica de estoque.
* **SQLAlchemy:** Conexão com banco de dados PostgreSQL.
* **Openpyxl:** Exportação de relatórios em formato Excel (.xlsx).

## 📂 Estrutura do Projeto

* `main.py`: Orquestrador central que executa o loop mensal de simulação.
* `banco.py`: Interface de conexão com o banco de dados para extração de produtos e fichas técnicas.
* `demanda.py`: Lógica de geração de demanda aleatória com ruídos e sazonalidade mensal.
* `entradas.py`: Gerador de compras de Matéria-Prima, considerando estoque mínimo e disponibilidade atual.
* `estoque.py`: Motor de regras de negócio para atualizar, verificar e consumir saldos de estoque.
* `movimentacoes_internas.py`: Simula a linha de produção, transformando MP em SA e SA em PA através de OPs.
* `saida.py`: Simula a venda dos produtos acabados para clientes finais.

## ⚙️ Configuração e Instalação

### 1. Requisitos
Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as credenciais do seu banco PostgreSQL:
```env
PG_USER=seu_usuario
PG_PASSWORD=sua_senha
PG_HOST=seu_host
PG_PORT=5432
PG_DATABASE=nome_do_banco
```

## 📊 Padrão de Saída (Exports)

O script gera um arquivo consolidado `pcp_planejamento_2025.xlsx` e diversos CSVs na pasta `exports/` seguindo o padrão aceito pelo Gestock:

* **Entradas_MP (`entradas.csv`):** Registra `produto_id`, `quantidade`, `preco_de_compra` e `fornecedor`.
* **Movimentacoes_Internas (`movimentacoes_internas.csv`):** Histórico de `CONSUMO` e `PRODUCAO` vinculado a uma Ordem de Produção (`OP-XXXX`).
* **Saidas_Vendas (`saidas.csv`):** Registra `produto_id`, `quantidade`, `preco_de_venda` e o `cliente`.
* **Status_OPs (`ops_status.csv`):** Indica se cada Ordem de Produção foi `CONCLUIDA` ou `NAO CONCLUIDA` devido a falta de insumos.

## 🧠 Lógica de Produção

O sistema utiliza um modelo de produção em três níveis:
1.  **MP (Matéria-Prima):** Insumos básicos comprados de fornecedores.
2.  **SA (Semiacabado):** Produzido internamente a partir de MPs.
3.  **PA (Produto Acabado):** Produto final pronto para venda, montado a partir de SAs.

---
*Este gerador faz parte do projeto de automação e análise de dados Gestock.*