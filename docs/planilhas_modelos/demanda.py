# demanda.py
import random
import pandas as pd
from banco import obter_ficha_tecnica
from banco import obter_produtos

MESES = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

SAZONALIDADE = {
    1: 0.9, 2: 0.95, 3: 1.1, 4: 1.15, 5: 1.2, 6: 1.15,
    7: 0.75, 8: 0.95, 9: 1.0, 10: 0.85, 11: 1.35, 12: 1.4
}

# BOM que está no banco de dados
def gerar_bom_fixa(df):
    bom = {}

    for produto_id, grupo in df.groupby("produto_final_id"):
        bom[produto_id] = dict(
            zip(grupo["materia_prima_id"], grupo["quantidade_necessaria"])
        )

    return bom


# Demanda
def gerar_demanda_mensal(df_produtos, ano):
    demandas = [] 
    demanda_id = 0 
 
    produtos_pa = df_produtos[df_produtos["tipo"] == "PA"] 

    '''
    Percorre todos os produtos acabados e cria 12 registros para cada, um em cada mês
    '''
    for _, produto in produtos_pa.iterrows():
        demanda_base = random.randint(180, 350) # gera uma demanda base para cada produto.

        # loop que cria o demanda para cada produto acabado durante um Mês
        for mes in range(1, 13):
            quantidade = int(
                demanda_base *
                SAZONALIDADE[mes] *
                random.uniform(0.9, 1.1) # simula ruidos
            )

            demandas.append({
                "id": demanda_id,
                "id_produto": produto["id"],
                "ano": ano,
                "mes": mes,
                "quantidade": quantidade
            })

            demanda_id += 1

    return pd.DataFrame(demandas)


if __name__ == "__main__":

    # BOM
    df_bom = obter_ficha_tecnica()
    bom = gerar_bom_fixa(df_bom)

    print("\n=== BOM (dicionário) ===")
    print(bom)


    # Demanda gerada

    df_produtos = obter_produtos()
    demanda_df = gerar_demanda_mensal(df_produtos, 2026)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print("\n=== DEMANDA MENSAL ===")
    print(demanda_df)