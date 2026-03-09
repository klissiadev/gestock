import pandas as pd
import random
from datetime import datetime
import calendar

CLIENTES = [
    "Loja Tech Brasil",
    "Distribuidora Gamer",
    "E-commerce X",
    "Empresa Corporativa Y",
    "Marketplace Z",
    "Tech Solutions",
    "Mega Informática",
    "Central Eletrônicos",
    "Loja Digital Prime",
    "Comercial Alpha"
]

VENDA_PARCIAL_PERMITIDA = True


def gerar_movimentacoes_saida(demanda_df: pd.DataFrame, estoque: pd.DataFrame):
    """
    Gera vendas mensais de TODOS os produtos PA existentes na demanda.

    Regras:
    - Para cada produto e mês, tenta vender entre 50% e 80% do estoque disponível NO FIM DO MÊS
    - Nunca vende mais do que a demanda do mês
    - Atualiza o estoque após cada venda
    """

    saidas = []

    # Garante ordenação cronológica
    demanda_df = demanda_df.sort_values(["ano", "mes"]).reset_index(drop=True)

    for (ano, mes), grupo_mes in demanda_df.groupby(["ano", "mes"]):

        ultimo_dia = calendar.monthrange(ano, mes)[1]
        data_venda = datetime(ano, mes, ultimo_dia).date()

        # Para cada produto vendido naquele mês
        for _, demanda in grupo_mes.iterrows():

            id_pa = demanda["id_produto"]
            demanda_mes = int(demanda["quantidade"])

            if id_pa not in estoque.index:
                continue

            estoque_disponivel = int(estoque.loc[id_pa, "quantidade"])

            if estoque_disponivel <= 0:
                continue

            # Percentual de saída: 50% a 80% do estoque disponível
            percentual_saida = random.uniform(0.5, 0.8)
            quantidade_planejada = int(estoque_disponivel * percentual_saida)

            if VENDA_PARCIAL_PERMITIDA:
                quantidade_vendida = min(quantidade_planejada, demanda_mes)
            else:
                quantidade_vendida = (
                    demanda_mes if estoque_disponivel >= demanda_mes else 0
                )

            if quantidade_vendida <= 0:
                continue

            # Atualiza estoque
            estoque.loc[id_pa, "quantidade"] -= quantidade_vendida

            saidas.append({
                "produto_id": id_pa,
                "quantidade": quantidade_vendida,
                "data_de_venda": data_venda,
                "preco_de_venda": round(random.uniform(150, 900), 2),
                "cliente": random.choice(CLIENTES)
            })

    df_saidas = pd.DataFrame(saidas)

    return df_saidas, estoque