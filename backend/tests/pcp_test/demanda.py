# demanda.py
import random
import pandas as pd

MESES = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

'''
Cada Mês possui um fator multiplicador.
Isso simula o comportamento real do mercado

'''
SAZONALIDADE = {
    1: 0.9, 2: 0.95, 3: 1.1, 4: 1.15, 5: 1.2, 6: 1.15,
    7: 0.75, 8: 0.95, 9: 1.0, 10: 0.85, 11: 1.35, 12: 1.4
}

# =========================================================
# BOM (Bill of Materials)
# =========================================================

# recebe um dataframe de produtos
def gerar_bom_fixa(df_produtos):
    bom = {}

    # separa os produtos por tipo
    df_mp = df_produtos[df_produtos["tipo"] == "MP"]
    df_sa = df_produtos[df_produtos["tipo"] == "SA"]
    df_pa = df_produtos[df_produtos["tipo"] == "PA"]

    # PA → SA
    '''
    Cada produto acabado usa de 2 a 4 semiacabados escolhidos aleatoriamente
    '''
    for _, pa in df_pa.iterrows():
        sa_usados = df_sa.sample(random.randint(2, 4))
        bom[pa["id"]] = {
            sa["id"]: random.randint(1, 2)
            for _, sa in sa_usados.iterrows()
        }

    # SA → MP
    '''
    Cada produto semiacabado usa de 3 a 6 de matéria prima
    '''
    for _, sa in df_sa.iterrows():
        mp_usados = df_mp.sample(random.randint(3, 6))
        bom[sa["id"]] = {
            mp["id"]: random.randint(1, 5)
            for _, mp in mp_usados.iterrows()
        }

    return bom

'''
Gera um BOM para cada produto acabada e produto semiacabado (fixo).
'''

# =========================================================
# DEMANDA
# =========================================================
'''
Recebe produtos e ano de simulação
Apenas produtos acabados geram demandas

'''
def gerar_demanda_mensal(df_produtos, ano):
    demandas = [] # irá armazenar todas as linhas de demanda
    demanda_id = 0

    produtos_pa = df_produtos[df_produtos["tipo"] == "PA"]

    '''
    Percorre todos os produtos acabados e cria 12 registros para cada, um em cada mês
    '''
    for _, produto in produtos_pa.iterrows():
        demanda_base = random.randint(180, 350) # gera uma demanda base para cada produto.

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
