import pandas as pd

# =========================================================
# ESTOQUE INICIAL
# =========================================================

def criar_estoque_inicial(produtos_df):
    """
    Cria estoque inicial zerado para todos os produtos
    """
    estoque = produtos_df[["id"]].copy()
    estoque["quantidade"] = 0
    estoque.set_index("id", inplace=True)
    return estoque

# =========================================================
# ATUALIZA ESTOQUE COM ENTRADAS DO MÊS
# =========================================================

def atualizar_estoque_compras(estoque, entradas_df, ano, mes):
    """
    Soma todas as compras realizadas no mês ao estoque
    """
    compras_mes = entradas_df[
        (entradas_df["data_de_compra"].dt.year == ano) &
        (entradas_df["data_de_compra"].dt.month == mes)
    ]

    for _, compra in compras_mes.iterrows():
        estoque.loc[compra["id_produto"], "quantidade"] += compra["quantidade"]

    return estoque

# =========================================================
# VERIFICA DISPONIBILIDADE DE MP PARA OP
# =========================================================

def verificar_mp_disponivel(estoque, necessidades_mp):
    """
    Verifica se há MP suficiente para executar a OP
    """
    for id_mp, qtd in necessidades_mp.items():
        if estoque.loc[id_mp, "quantidade"] < qtd:
            return False
    return True

# =========================================================
# CONSUME MP DO ESTOQUE
# =========================================================

def consumir_mp(estoque, necessidades_mp):
    """
    Abate MP do estoque
    """
    for id_mp, qtd in necessidades_mp.items():
        estoque.loc[id_mp, "quantidade"] -= qtd

    return estoque
