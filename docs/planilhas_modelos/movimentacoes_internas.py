from datetime import datetime
import pandas as pd
from estoque import verificar_mp_disponivel, consumir_mp


def gerar_movimentacoes_internas(demanda_df, bom, estoque):

    movimentacoes = []
    ops = []
    id_counter = 1
    op_counter = 2000

    # ===============================
    # PARÂMETROS
    # ===============================
    FATOR_ESTOQUE_PA = 1.10
    LOTE_MIN_SA = 200

    def add_mov(mov):
        if mov["quantidade"] > 0:
            movimentacoes.append(mov)

    for _, demanda in demanda_df.iterrows():
        id_pa = demanda["id_produto"]
        qtd_pa_demanda = demanda["quantidade"]
        ano = demanda["ano"]
        mes = demanda["mes"]

        qtd_pa_produzida = int(qtd_pa_demanda * FATOR_ESTOQUE_PA)

        op = f"OP-{op_counter}"
        data_op = datetime(ano, mes, 10).date()

        # ===============================
        # NECESSIDADE DE SA
        # ===============================
        necessidades_sa = {
            id_sa: qtd_pa_produzida * qtd_sa
            for id_sa, qtd_sa in bom.get(id_pa, {}).items()
        }

        # ===============================
        # PRODUÇÃO DE SA
        # ===============================
        producao_sa = {}

        for id_sa, qtd_necessaria in necessidades_sa.items():

            if id_sa not in estoque.index:
                estoque.loc[id_sa] = 0

            estoque_atual = estoque.loc[id_sa, "quantidade"]
            falta = max(0, qtd_necessaria - estoque_atual)

            producao_sa[id_sa] = max(falta, LOTE_MIN_SA) if falta > 0 else 0

        # ===============================
        # NECESSIDADE DE MP
        # ===============================
        necessidades_mp = {}

        for id_sa, qtd_sa_prod in producao_sa.items():
            if qtd_sa_prod <= 0:
                continue

            for id_mp, qtd_mp in bom.get(id_sa, {}).items():
                necessidades_mp[id_mp] = (
                    necessidades_mp.get(id_mp, 0)
                    + (qtd_sa_prod * qtd_mp)
                )

        # ===============================
        # AJUSTE POR FALTA DE MP
        # ===============================
        fator_disponivel = 1.0

        for id_mp, qtd_necessaria in necessidades_mp.items():
            if id_mp not in estoque.index:
                estoque.loc[id_mp] = 0

            estoque_disp = estoque.loc[id_mp, "quantidade"]

            if qtd_necessaria > 0 and estoque_disp < qtd_necessaria:
                fator = estoque_disp / qtd_necessaria
                fator_disponivel = min(fator_disponivel, fator)

        # aplica fator
        qtd_pa_produzida = int(qtd_pa_produzida * fator_disponivel)

        for id_sa in producao_sa:
            producao_sa[id_sa] = int(producao_sa[id_sa] * fator_disponivel)

        # 🔒 cancela OP se produção zerou
        if qtd_pa_produzida <= 0:
            ops.append({
                "ordem_de_producao": op,
                "id_produto": id_pa,
                "mes": mes,
                "ano": ano,
                "status": "NAO CONCLUIDA"
            })
            op_counter += 1
            continue

        # ===============================
        # RECALCULA MP
        # ===============================
        necessidades_mp = {}

        for id_sa, qtd_sa_prod in producao_sa.items():
            if qtd_sa_prod <= 0:
                continue

            for id_mp, qtd_mp in bom.get(id_sa, {}).items():
                necessidades_mp[id_mp] = (
                    necessidades_mp.get(id_mp, 0)
                    + (qtd_sa_prod * qtd_mp)
                )

        # ===============================
        # VERIFICA MP
        # ===============================
        if not verificar_mp_disponivel(estoque, necessidades_mp):
            ops.append({
                "ordem_de_producao": op,
                "id_produto": id_pa,
                "mes": mes,
                "ano": ano,
                "status": "NAO CONCLUIDA"
            })
            op_counter += 1
            continue

        # ===============================
        # CONSUMO DE MP
        # ===============================
        estoque = consumir_mp(estoque, necessidades_mp)

        for id_mp, qtd in necessidades_mp.items():
            if qtd <= 0:
                continue

            add_mov({
                "id": id_counter,
                "id_produto": id_mp,
                "ordem_de_producao": op,
                "tipo": "CONSUMO",
                "quantidade": qtd,
                "origem": "Estoque MP",
                "destino": "Linha SA",
                "data": data_op
            })
            id_counter += 1

        # ===============================
        # PRODUÇÃO DE SA
        # ===============================
        for id_sa, qtd_prod in producao_sa.items():
            if qtd_prod <= 0:
                continue

            estoque.loc[id_sa, "quantidade"] += qtd_prod

            add_mov({
                "id": id_counter,
                "id_produto": id_sa,
                "ordem_de_producao": op,
                "tipo": "PRODUCAO",
                "quantidade": qtd_prod,
                "origem": "Linha SA",
                "destino": "Estoque SA",
                "data": data_op
            })
            id_counter += 1

        # ===============================
        # CONSUMO DE SA PARA PA (CORRIGIDO)
        # ===============================
        for id_sa, qtd_sa in bom.get(id_pa, {}).items():

            consumo_sa = qtd_pa_produzida * qtd_sa

            if id_sa not in estoque.index:
                estoque.loc[id_sa] = 0

            estoque_atual = estoque.loc[id_sa, "quantidade"]
            consumo_real = min(consumo_sa, estoque_atual)

            if consumo_real <= 0:
                continue

            estoque.loc[id_sa, "quantidade"] -= consumo_real

            add_mov({
                "id": id_counter,
                "id_produto": id_sa,
                "ordem_de_producao": op,
                "tipo": "CONSUMO",
                "quantidade": consumo_real,
                "origem": "Estoque SA",
                "destino": "Linha PA",
                "data": data_op
            })
            id_counter += 1

        # ===============================
        # PRODUÇÃO DE PA
        # ===============================
        estoque.loc[id_pa, "quantidade"] += qtd_pa_produzida

        add_mov({
            "id": id_counter,
            "id_produto": id_pa,
            "ordem_de_producao": op,
            "tipo": "PRODUCAO",
            "quantidade": qtd_pa_produzida,
            "origem": "Linha PA",
            "destino": "Estoque PA",
            "data": data_op
        })
        id_counter += 1

        ops.append({
            "ordem_de_producao": op,
            "id_produto": id_pa,
            "mes": mes,
            "ano": ano,
            "status": "CONCLUIDA"
        })

        op_counter += 1

    mov_df = pd.DataFrame(movimentacoes)

    if not mov_df.empty:
        mov_df = mov_df.rename(columns={"id_produto": "produto_id"})
        mov_df = mov_df[
            ["produto_id", "ordem_de_producao", "tipo",
             "quantidade", "origem", "destino", "data"]
        ]

    return mov_df, pd.DataFrame(ops), estoque