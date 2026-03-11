import pandas as pd
from datetime import date, timedelta
from typing import List
from darts import TimeSeries
import psycopg

from forecasting_module.schemas.models import FieldSaida
from forecasting_module.db.database import Repository

def preparar_dados_para_tft(movimentacoes: List[FieldSaida], data_inicio: date, data_fim: date, produto_id: int) -> pd.DataFrame:
    """
    Recebe os dados validados do banco, preenche os dias sem vendas e 
    formata as colunas exatamente como o modelo TFT espera.
    """
    
    # Lista de objetos Pydantic em Lista de dicionario
    dados_dict = [mov.model_dump() for mov in movimentacoes]
    
    # Com base neles, cria um data frame
    df = pd.DataFrame(dados_dict)
    
    # Renomear pro padrao Darts
    df = df.rename(columns={
        'data_de_venda': 'date',
        'quantidade': 'y',
        'produto_id': 'item_id',
        'preco_de_venda': 'sell_price'
    })
    
    if df.empty:
        df = pd.DataFrame(columns=['date', 'y', 'item_id', 'sell_price'])
        
    df['date'] = pd.to_datetime(df['date'])
    
    # O range completo de dadas: Inicio -> Fim
    calendario_completo = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    df.set_index('date', inplace=True)
    df = df.reindex(calendario_completo)
    
    # Tratamento de valores nulos (dias sem venda, que nao tem registro de movimentacao)
    df['y'] = df['y'].fillna(0)
    df['item_id'] = df['item_id'].fillna(produto_id)
    df['sell_price'] = df['sell_price'].ffill().fillna(0)
    
    df = df.reset_index().rename(columns={'index': 'date'})
    
    # Covariaveis do Kaggle aqui
    # Nao sei o que colocar, entao botei Zero em todas + pra nao acusar que ta zoado
    df['snap_CA'] = 0
    df['snap_TX'] = 0
    df['snap_WI'] = 0
    df['event_name_1'] = 0
    df['event_type_1'] = 0
    df['event_name_2'] = 0
    df['event_type_2'] = 0
    
    return df



def gerar_previsao_estoque(conexao, produto_id: int, tft_days: int=112):
    """
    Orquestra o fluxo completo: Busca no banco, formata e mostra o dado formatado (testes)
    """
    
    # Definir a janela de tempo (O TFT exige 112 dias exatos de passado)
    data_fim = date.today()
    data_inicio = data_fim - timedelta(tft_days)

    # Buscar os dados no PostgreSQL (Retorna Lista de FieldSaida validados)
    repo = Repository(conexao)
    movimentacoes_validadas = repo.buscar_historico_vendas(produto_id, data_inicio)

    # Formatar para o Pandas
    df_formatado = preparar_dados_para_tft(
        movimentacoes=movimentacoes_validadas,
        data_inicio=data_inicio,
        data_fim=data_fim - timedelta(days=1), # Até ontem
        produto_id=produto_id
    )
    
    # TO DO: Converter do Pandas para Darts (TimeSeries)
    # Aplicar a escala matematica -> carrega o arquivo de escala e chama o .transform
    # Cria o horizonte de previsa0 -> padrao 28 dias
    # e chama o modelo TFT usando o .predict() usando a serie escalada + horizonte de previsao
    # previsao real -> pegar a escala matematica e inverter de volta -> .inverse_transform
    
    # Finalmente
    # Formatar a saida no padrao
    # Dicionario padrao: {produto_id, demanda_total_28_dias, previsao_diaria}
    
    return df_formatado


if __name__ == '__main__':
    from forecasting_module.core.env_loader import load_env_from_root
    import os
    load_env_from_root()
    STRING_CONEXAO = os.getenv("DATABASE_URL")
    
    try:
        with psycopg.connect(STRING_CONEXAO) as conn:
            print("Conectado! Formatando dados...")
            resultado_df = gerar_previsao_estoque(conexao=conn, produto_id=32)
            
            print("\n--- PRIMEIRAS LINHAS ---")
            print(resultado_df.head(5))
            print("\n--- ÚLTIMAS LINHAS ---")
            print(resultado_df.tail(30))
            
            print(f"\nTotal de dias formatados: {len(resultado_df)} (Deve ser exatos 112!)")
            
    except Exception as e:
        print(f"Erro no teste: {e}")

