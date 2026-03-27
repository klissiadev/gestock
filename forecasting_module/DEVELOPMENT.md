# 🛠️ Guia de Desenvolvimento - Forecasting Module

Este guia detalha a arquitetura interna, os fluxos de dados e as camadas lógicas do **Forecasting Module**. Ele é essencial para quem for criar novos modelos preditivos, alterar cálculos de banco de dados ou adicionar novas rotas à API.

---

## 🏗️ Arquitetura e Camadas do Projeto

O módulo foi estruturado separando claramente as responsabilidades de acesso a dados, validação e regras de negócio/inteligência artificial.

### 1. Camada de Acesso a Dados (`database.py`)
Centralizada na classe `Repository`, esta camada gerencia toda a comunicação com o PostgreSQL via `psycopg`. 
* **Conexões Assíncronas e Síncronas:** A maioria das consultas utiliza cursores assíncronos (`async with self.conn.cursor()`), enquanto a extração de dados brutos para anomalia (`buscar_dados_anomalia`) opera de forma síncrona.
* **Uso de Views e CTEs:** Lógicas complexas são delegadas ao banco. O método `necessidade_compra` utiliza a *Common Table Expression* (CTE) `ProdutosFaltantes` para cruzar o déficit de fabricação com a ficha técnica (`app_core.ficha_tecnica`) e sugerir a quantidade exata de insumos a comprar.
* **Formatação Nativa:** Consultas como `buscar_historico_vendas` utilizam o `row_factory=dict_row` do `psycopg` para retornar dicionários que são imediatamente validados por modelos Pydantic.

### 2. Camada de Schemas e Validação (`models.py`)
Utiliza o `pydantic` para garantir a tipagem rigorosa das entradas e saídas da API.
* **Modelos Principais:** * `FieldSaida`: Valida os registros de movimentação contendo identificadores, quantidade, data e preço de venda.
  * `SugestaoCompraInsumo`: Estrutura o retorno da explosão de materiais com `materia_prima_id`, nome e a quantidade flutuante sugerida.
  * `PontoGrafico` e `ProdutoDropdown`: Moldam os dados de demanda preditiva e listas de seleção de forma otimizada para o consumo do *frontend*.

### 3. Camada de Serviços de Aplicação (`anomaly_app_service.py`)
Atua como a ponte entre os motores matemáticos (Batch Detector/ML) e o carregamento de dados.
* **Orquestração:** A classe `AnomalyAppService` invoca o `load_anomaly_data` e passa o *DataFrame* resultante para o detector em lote.
* **Tratamento de Tipos:** Antes de devolver a resposta para a API, o serviço iterage sobre as colunas do *DataFrame* que possuem tipagem `datetime64[ns]` ou `datetime64[ns, UTC]` e as converte para *strings*. Isso previne erros de serialização JSON no FastAPI.
* **Formato de Retorno:** Retorna um dicionário contendo a lista de anomalias detectadas (`data`) e a contagem total de registros (`count`).

---

## 🔄 Fluxos de Trabalho Principais

Para facilitar a manutenção, entenda como a informação viaja dentro do módulo:

### Fluxo de Previsão e Necessidade de Compras
1. A rota (`router.py`) recebe a chamada e, caso solicitado, executa um `REFRESH MATERIALIZED VIEW` na `vw_product` para garantir dados frescos.
2. O `Repository` calcula o déficit através da query `necessidade_compra`.
3. Os dados brutos do PostgreSQL são devolvidos e formatados pela rota utilizando o schema `SugestaoCompraInsumo`.

### Fluxo de Detecção de Anomalias
1. A rota recebe a `data_corte` e a repassa para o `AnomalyAppService`.
2. O serviço carrega a base de dados em formato tabular (*DataFrame Pandas*) através de conexões síncronas com a view `vw_anomaly_input`.
3. O `BatchDetector` itera sobre as linhas, solicitando a inferência do `AnomalyService` (que por sua vez busca o modelo e escalonador corretos no `ModelRegistry`).
4. Os resultados são limpos, convertidos para serialização segura, e devolvidos para o cliente.

## 📓 Cadernos de Experimentação e Treinamento (Jupyter)

A pasta `notebooks/` contém os laboratórios de pesquisa onde os algoritmos do **Forecasting Module** foram idealizados, validados e treinados antes de serem produtizados na API. É o ambiente de trabalho principal para Cientistas de Dados.

* **`notebooks/AnomalyDetection.ipynb`**: O coração do treinamento do modelo de anomalias.
  * **Engenharia de Features:** Responsável por explorar os dados e definir como as variáveis de contexto seriam usadas (ex: extração do dia da semana a partir da data para cruzar com `value` e `sell_price`).
  * **Treinamento e Escalonamento:** Ambiente onde o algoritmo de detecção de *outliers* é ajustado. Ele consolida o cálculo da função de decisão (`decision_function`) e aplica a normalização matemática dos dados (`scaler`).
  * **Exportação de Artefatos:** O passo final do *notebook* exporta os modelos validados e seus respectivos escalonadores agrupados por Categoria/Loja. O resultado é o arquivo serializado `modelos_vendas_completo.pkl` salvo em `ml_artifacts/` utilizando a biblioteca `joblib`.
* **`notebooks/demandPrediction.ipynb`**: Focado na prototipação do motor de projeção de séries temporais.
  * **Exploração de Dados (EDA):** Análise exploratória do histórico de movimentação de saídas dos produtos acabados e consolidação de tendências.
  * **Prototipação Matemática:** Validação do cálculo estatístico de Média Móvel Exponencial (MME). É neste caderno que o fator de suavização (onde $\alpha=2/(N+1)$ para $N=3$ meses) foi testado contra dados históricos reais para garantir a sensibilidade correta a mudanças de curto prazo, antes da lógica ser transcrita para o endpoint final no `router.py`.

## ⚙️ Configurando o Ambiente Local

Como o ecossistema do **Forecasting Module** utiliza o `uv` sob os panos, a preparação do ambiente é extremamente rápida.

### 1. Sincronizar dependências e criar ambiente
Na raiz da pasta do `forecasting_module` (onde está o arquivo `pyproject.toml` e `uv.lock`), execute:
```bash
uv sync
```

### 2. Ativar o ambiente virtual
**Em ambientes Windows:**
```bash
.venv\Scripts\activate
```
**Em ambientes Linux / macOS:**
```bash
source .venv/bin/activate
```
