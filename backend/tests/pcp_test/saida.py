import pandas as pd
import random
from datetime import datetime
import calendar

CLIENTES = [
    "Loja Tech Brasil",
    "Distribuidora Gamer",
    "E-commerce X",
    "Empresa Corporativa Y",
    "Marketplace Z"
]

VENDA_PARCIAL_PERMITIDA = True  # se False, só vende se tiver tudo

def gerar_movimentacoes_saida(demanda_df, estoque):
    """
    Gera vendas de produtos PA com base na demanda e estoque disponível
    """

    saidas = []
    id_counter = 1

    for _, demanda in demanda_df.iterrows():
        id_pa = demanda["id_produto"]
        quantidade_demandada = demanda["quantidade"]
        ano = demanda["ano"]
        mes = demanda["mes"]

        # Data da venda: último dia real do mês
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        data_venda = datetime(ano, mes, ultimo_dia)

        estoque_disponivel = estoque.loc[id_pa, "quantidade"]

        if estoque_disponivel <= 0:
            continue

        # Decide quantidade vendida
        if VENDA_PARCIAL_PERMITIDA:
            quantidade_vendida = min(quantidade_demandada, estoque_disponivel)
        else:
            if estoque_disponivel < quantidade_demandada:
                continue
            quantidade_vendida = quantidade_demandada

        quantidade_vendida = max(0, quantidade_vendida)
        status_venda = "PARCIAL" if quantidade_vendida < quantidade_demandada else "TOTAL"

        # Abate estoque
        estoque.loc[id_pa, "quantidade"] -= quantidade_vendida

        saidas.append({
            "id": id_counter,
            "id_produto": id_pa,
            "quantidade": quantidade_vendida,
            "data_de_venda": data_venda,
            "preco_de_venda": round(random.uniform(150, 900), 2),
            "cliente": random.choice(CLIENTES),
            "status_venda": status_venda
        })

        id_counter += 1

    return pd.DataFrame(saidas), estoque
