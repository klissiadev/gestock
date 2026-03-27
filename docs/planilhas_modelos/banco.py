import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Carrega variáveis do .env
load_dotenv()

# Cria engine de conexão (PostgreSQL)
def criar_engine():
    usuario = os.getenv("PG_USER")
    senha = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    porta = os.getenv("PG_PORT")
    database = os.getenv("PG_DATABASE")
    
    engine = create_engine(f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{database}")
    return engine

# Função que retorna o DataFrame de produtos
def obter_produtos():
    engine = criar_engine()
    query = """
    SELECT id, nome, descricao, estoque_minimo, data_validade, ativo, tipo
    FROM app_core.produtos
    """
    df_produtos = pd.read_sql(query, engine)
    return df_produtos

# Função que retorna o DataFrame da ficha técnica (BOM)
def obter_ficha_tecnica():
    engine = criar_engine()
    
    query_ficha = """
    SELECT produto_final_id, materia_prima_id, quantidade_necessaria
    FROM app_core.ficha_tecnica
    """
    
    df_ficha = pd.read_sql(query_ficha, engine)
    
    return df_ficha

# Exemplo de uso
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.expand_frame_repr', False)
    
    produtos = obter_produtos()
    ficha_tecnica = obter_ficha_tecnica()


    print(ficha_tecnica.columns)
    print(ficha_tecnica.head())
    
    print("=== Produtos ===")
    print(produtos.drop(columns=['descricao'])) 
    
    print("\n=== Ficha Técnica (BOM) ===")
    print(ficha_tecnica)

    