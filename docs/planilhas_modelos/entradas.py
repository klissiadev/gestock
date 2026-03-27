import pandas as pd
import random
from datetime import datetime

VARIACAO_COMPRA = (-0.05, 0.10)

FORNECEDORES = [
    "Fornecedor Alpha", "Fornecedor Beta", "Fornecedor Gamma",
    "Fornecedor Delta", "Fornecedor Epsilon", "Fornecedor Zeta",
    "Fornecedor Eta", "Fornecedor Theta", "Fornecedor Iota",
    "Fornecedor Kappa"
]


def gerar_entradas_mp(demanda_df, produtos_df, bom, estoque):

    mp_ids = set(produtos_df[produtos_df["tipo"] == "MP"]["id"])
    estoque_min_map = produtos_df.set_index("id")["estoque_minimo"].to_dict()

    compras = []
    id_counter = 1

    for _, demanda in demanda_df.iterrows():
        id_pa = demanda["id_produto"]
        quantidade_pa = demanda["quantidade"]
        ano = demanda["ano"]
        mes = demanda["mes"]

        data_compra = datetime(ano, mes, 1).date()

        if id_pa not in bom:
            continue

        for id_sa, qtd_sa in bom[id_pa].items():
            qtd_sa_necessaria = quantidade_pa * qtd_sa

            if id_sa not in bom:
                continue

            for id_mp, qtd_mp in bom[id_sa].items():
                if id_mp not in mp_ids:
                    continue

                necessidade_mp = qtd_sa_necessaria * qtd_mp

                # 🔥 CONSULTA ESTOQUE ATUAL (dinâmico)
                if id_mp not in estoque.index:
                    estoque.loc[id_mp, "quantidade"] = 0

                estoque_atual = estoque.loc[id_mp, "quantidade"]
                estoque_minimo = estoque_min_map.get(id_mp, 0)

                # 🔥 COMPRA SOMENTE SE NECESSÁRIO
                quantidade_necessaria = max(
                    0,
                    necessidade_mp + estoque_minimo - estoque_atual
                )

                if quantidade_necessaria <= 0:
                    continue

                # variação
                # variação
                fator = 1 + random.uniform(*VARIACAO_COMPRA)
                quantidade_compra = int(quantidade_necessaria * fator)

                # garante que nunca seja zero
                if quantidade_compra <= 0:
                    quantidade_compra = 1

                compras.append({
                    #"id": id_counter,
                    "produto_id": id_mp,
                    "quantidade": quantidade_compra,
                    "data_de_compra": data_compra,
                    "preco_de_compra": round(random.uniform(5, 50), 0),
                    "fornecedor": random.choice(FORNECEDORES)
                })

                id_counter += 1

                # 🔥 ATUALIZA ESTOQUE IMEDIATAMENTE
                estoque.loc[id_mp, "quantidade"] += quantidade_compra

    return pd.DataFrame(compras)