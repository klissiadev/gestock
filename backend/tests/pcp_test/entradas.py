import pandas as pd
import random
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

VARIACAO_COMPRA = (-0.05, 0.10)  # -5% até +10%
FORNECEDORES = [
    "Fornecedor Alpha",
    "Fornecedor Beta",
    "Fornecedor Gamma",
    "Fornecedor Delta",
    "Fornecedor Epsilon",
    "Fornecedor Zeta",
    "Fornecedor Eta",
    "Fornecedor Theta",
    "Fornecedor Iota",
    "Fornecedor Kappa"
]

# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================

def gerar_entradas_mp(demanda_df, produtos_df, bom, estoque):
    """
    Gera compras de MP considerando estoque atual e estoque mínimo realista.
    """

    mp_ids = produtos_df[produtos_df["tipo"] == "MP"]["id"].tolist()
    compras = []
    ESTOQUE_MINIMO_MP = 20  # estoque mínimo para cada MP

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

                # Quantidade total de MP necessária para a produção do mês
                necessidade_mp = qtd_sa_necessaria * qtd_mp

                # Estoque atual
                estoque_atual = estoque.loc[id_mp, "quantidade"]

                # Compra apenas se estiver abaixo do mínimo
                quantidade_necessaria = max(0, necessidade_mp + ESTOQUE_MINIMO_MP - estoque_atual)

                if quantidade_necessaria <= 0:
                    continue  # estoque suficiente, não compra

                # Aplicar variação de compra
                fator = 1 + random.uniform(*VARIACAO_COMPRA)
                quantidade_compra = max(1, int(quantidade_necessaria * fator))

                # Registrar compra
                compras.append({
                    "produto_id": id_mp,
                    "quantidade": quantidade_compra,
                    "data_de_compra": data_compra,
                    "preco_de_compra": round(random.uniform(5, 50), 2),
                    "fornecedor": random.choice(FORNECEDORES)
                })

                # Atualizar estoque imediatamente
                estoque.loc[id_mp, "quantidade"] += quantidade_compra

    return pd.DataFrame(compras)


'''
Tabela de entrada possui:
- produto_id
- quantidade 
- data_de_compra
- preco_de_compra
- fornecedor

'''
