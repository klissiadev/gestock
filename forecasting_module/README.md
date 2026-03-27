# 📈 Forecasting Module - Previsão de Demanda e Detecção de Anomalias

O **Forecasting Module** é a biblioteca analítica e de Machine Learning do **Gestock** dedicada à detecção de anomalias em vendas, análise preditiva de demanda e sugestão inteligente de compras. Utilizando ferramentas modernas de ciência de dados e cálculos estatísticos, este módulo transforma dados históricos em estratégias acionáveis para gestão de estoque.

> **Vai dar manutenção neste código ou treinar novos modelos preditivos?** Leia a nossa [documentação de desenvolvimento](DEVELOPMENT.md) para entender a arquitetura do Registro de Modelos e dos Serviços de Anomalia.

## 🚀 Funcionalidades Principais e Arquitetura

O módulo foi desenhado para unir modelos de Machine Learning pré-treinados com lógicas de negócios diretas no banco de dados, dividindo-se nas seguintes frentes:

* **1. Serviço de Detecção de Anomalias (`AnomalyService` e `BatchDetector`)**
  * Recebe informações contextuais para realizar inferências matemáticas, extraindo *features* temporais e processando os dados utilizando escalonadores (`scaler.transform`).
  * O `BatchDetector` permite a classificação em lote processando `pandas` DataFrames para aplicar o modelo em múltiplos registros de forma eficiente.
* **2. Motor de Previsão de Demanda Matemática**
  * Calcula a Previsão de Demanda baseada na Média Móvel Exponencial (MME) dos últimos 3 meses.
  * A arquitetura aplica um fator de suavização (`alpha`) que dá maior peso aos dados mais recentes, tornando a previsão sensível a mudanças de curto prazo no comportamento de saída dos produtos.
* **3. Motor de Sugestão de Compras (BOM)**
  * Calcula a necessidade de compra de matérias-primas baseada no déficit projetado dos Produtos Acabados, realizando a "explosão" da ficha técnica (Bill of Materials).
* **4. Registro de Modelos (`ModelRegistry`)**
  * Gerencia o carregamento sob demanda de artefatos de IA armazenados em `.pkl` (via `joblib`), buscando o algoritmo específico para a exata combinação de Categoria e Loja.

## 🌐 Endpoints da API REST
O módulo expõe as seguintes rotas via FastAPI para interagir com os serviços de inteligência e cálculo:

**Previsão e Suprimentos (`/previsao`):**
* `GET /previsao/produtos-com-historico`: Retorna produtos acabados com movimentação de saída, estruturado para popular *dropdowns* no frontend.
* `GET /previsao/sugestoes-compra-insumos`: Gera a lista de compras. Aceita o parâmetro opcional `atualizar_view` para forçar o recálculo da *Materialized View* (`app_core.vw_product`) no banco de dados.
* `GET /previsao/{produto_id}`: Retorna os pontos do gráfico contendo o histórico real de demanda e a projeção para o "Próximo Mês (Previsão)".

**Detecção de Anomalias (`/anomalies`):**
* `GET /anomalies`: Requer o parâmetro `data_corte` e resgata registros de comportamentos atípicos a partir do período informado.

## 🔌 Como Integrar no Backend Principal

**1. Adicionando como dependência (Poetry):**
No terminal, dentro do diretório raiz do backend do Gestock, instale o pacote localmente:
```bash
poetry add ../forecasting_module
```

**Alternativa (Adição Manual no `pyproject.toml`):**
Para garantir o hot-reload de edições locais sem reinstalação:
```toml
[tool.poetry.dependencies]
forecasting-module = { path = "../caminho/para/forecasting_module", develop = true }
```
Sincronize o ambiente rodando `poetry install`.

**2. Registrando no FastAPI (`main.py`):**
Este módulo depende do pool de conexões assíncronas do backend (`psycopg.AsyncConnection` em `request.app.state.db_pool`) para os cálculos de banco de dados. 

Registre as rotas importando os *routers* do módulo:
```python
from fastapi import FastAPI
# Importações do Forecasting Module
from forecasting_module.api.anomaly_router import create_anomaly_router
from forecasting_module.api.router import router as previsao_router
from forecasting_module.services.anomaly_service import AnomalyService
from forecasting_module.services.batch_detector import BatchDetector
from forecasting_module.services.anomaly_app_service import AnomalyAppService
from forecasting_module.services.model_loader import ModelRegistry

app = FastAPI(title="Gestock Backend")

# Setup dos Serviços de Anomalia
MODEL_PATH = "forecasting_module/ml_artifacts/modelos_vendas_completo.pkl"
registry = ModelRegistry(MODEL_PATH)
anomaly_service = AnomalyService(registry)
detector = BatchDetector(anomaly_service)
anomaly_app_service = AnomalyAppService(detector)

# Registrando os endpoints
app.include_router(
    create_anomaly_router(app_service=anomaly_app_service), 
    prefix="/ml" # ou /anomalies
)
app.include_router(previsao_router) # Já carrega seu próprio prefixo /previsao internamente
```