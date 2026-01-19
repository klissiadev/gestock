from datetime import datetime
import pandas as pd
from estoque import verificar_mp_disponivel, consumir_mp

def gerar_movimentacoes_internas(demanda_df, bom, estoque):
    """
    Gera movimentações internas de produção de SA e PA.

    Ajustes realistas:
    - Produção extra de PA (estoque de segurança)
    - Lote mínimo de SA (WIP)
    - Produção proporcional ao MP disponível
    """

    movimentacoes = []
    ops = []
    id_counter = 1
    op_counter = 2000

    # ===============================
    # PARÂMETROS DE REALISMO
    # ===============================
    FATOR_ESTOQUE_PA = 1.05      # produz 5% a mais de PA
    LOTE_MIN_SA = 20             # lote mínimo de SA

    for _, demanda in demanda_df.iterrows():
        id_pa = demanda["id_produto"]
        qtd_pa_demanda = demanda["quantidade"]
        ano = demanda["ano"]
        mes = demanda["mes"]

        # Quantidade real produzida de PA
        qtd_pa_produzida = int(qtd_pa_demanda * FATOR_ESTOQUE_PA)

        op = f"OP-{op_counter}"
        data_op = datetime(ano, mes, 10)

        # ===============================
        # CALCULAR NECESSIDADE TOTAL DE MP
        # ===============================
        necessidades_mp = {}

        for id_sa, qtd_sa in bom[id_pa].items():
            qtd_sa_necessaria = qtd_pa_produzida * qtd_sa
            qtd_sa_produzida = max(qtd_sa_necessaria, LOTE_MIN_SA)

            for id_mp, qtd_mp in bom[id_sa].items():
                necessidades_mp[id_mp] = (
                    necessidades_mp.get(id_mp, 0)
                    + (qtd_sa_produzida * qtd_mp)
                )

        # ===============================
        # AJUSTE DE PRODUÇÃO PARCIAL SE FALTAR MP
        # ===============================
        fator_disponivel = 1.0
        for id_mp, qtd_necessaria in necessidades_mp.items():
            estoque_disponivel = estoque.loc[id_mp, "quantidade"]
            if estoque_disponivel < qtd_necessaria:
                fator = estoque_disponivel / qtd_necessaria if qtd_necessaria > 0 else 0
                if fator < fator_disponivel:
                    fator_disponivel = fator

        # Ajusta produção de SA e PA proporcional ao MP disponível
        qtd_pa_produzida = int(qtd_pa_produzida * fator_disponivel)
        for id_sa in bom[id_pa]:
            qtd_sa_necessaria = qtd_pa_produzida * bom[id_pa][id_sa]
            qtd_sa_produzida = max(qtd_sa_necessaria, LOTE_MIN_SA)
            # Atualiza necessidades_mp proporcionalmente
            for id_mp, qtd_mp in bom[id_sa].items():
                necessidades_mp[id_mp] = int(qtd_sa_produzida * qtd_mp)

        # ===============================
        # VERIFICA ESTOQUE DE MP
        # ===============================
        if not verificar_mp_disponivel(estoque, necessidades_mp):
            ops.append({
                "op": op,
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
            movimentacoes.append({
                "id": id_counter,
                "id_produto": id_mp,
                "op": op,
                "tipo": "CONSUMO",
                "quantidade": qtd,
                "origem": "Estoque MP",
                "destino": "Linha SA",
                "data": data_op
            })
            id_counter += 1

        # ===============================
        # PRODUÇÃO DE SA (WIP REAL)
        # ===============================
        for id_sa, qtd_sa in bom[id_pa].items():
            qtd_sa_necessaria = qtd_pa_produzida * qtd_sa
            qtd_sa_produzida = max(qtd_sa_necessaria, LOTE_MIN_SA)

            movimentacoes.append({
                "id": id_counter,
                "id_produto": id_sa,
                "op": op,
                "tipo": "PRODUCAO",
                "quantidade": qtd_sa_produzida,
                "origem": "Linha SA",
                "destino": "Estoque SA",
                "data": data_op
            })
            id_counter += 1

        # ===============================
        # PRODUÇÃO DE PA (COM ESTOQUE)
        # ===============================
        movimentacoes.append({
            "id": id_counter,
            "id_produto": id_pa,
            "op": op,
            "tipo": "PRODUCAO",
            "quantidade": qtd_pa_produzida,
            "origem": "Linha PA",
            "destino": "Estoque PA",
            "data": data_op
        })
        id_counter += 1

        ops.append({
            "op": op,
            "id_produto": id_pa,
            "mes": mes,
            "ano": ano,
            "status": "CONCLUIDA"
        })

        op_counter += 1

    return pd.DataFrame(movimentacoes), pd.DataFrame(ops), estoque
