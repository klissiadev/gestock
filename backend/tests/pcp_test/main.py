import pandas as pd

# =========================
# IMPORTS DOS MÓDULOS
# =========================
from produtos import criar_produtos_dataframe
from demanda import gerar_demanda_mensal, gerar_bom_fixa
from entradas import gerar_entradas_mp
from estoque import criar_estoque_inicial, atualizar_estoque_compras
from movimentacoes_internas import gerar_movimentacoes_internas
from saida import gerar_movimentacoes_saida

# =========================
# CONFIG
# =========================
ANO_PLANEJAMENTO = 2027
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# =========================
# GERADOR DE EXCEL
# =========================
def gerar_excel_pcp(produtos_df, entradas_df, movimentacoes_df, saidas_df, ops_df, ano):
    nome_arquivo = f"pcp_planejamento_{ano}.xlsx"
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        produtos_df.to_excel(writer, sheet_name="Produtos", index=False)
        entradas_df.to_excel(writer, sheet_name="Entradas_MP", index=False)
        movimentacoes_df.to_excel(writer, sheet_name="Movimentacoes_Internas", index=False)
        if not saidas_df.empty:
            saidas_df.to_excel(writer, sheet_name="Saidas_Vendas", index=False)
        ops_df.to_excel(writer, sheet_name="Ordens_Producao", index=False)
    print(f"\n📊 Arquivo Excel gerado com sucesso: {nome_arquivo}")

# =========================
# RELATÓRIO MENSAL
# =========================
def mostrar_resumo_mensal(ano, entradas_df, movimentacoes_df, saidas_df, ops_df):
    for mes in range(1, 13):
        print("\n" + "="*120)
        print(f"📆 MÊS {mes:02d}/{ano}")
        print("="*120)

        entradas_mes = entradas_df[pd.to_datetime(entradas_df["data_de_compra"]).dt.month == mes]
        print("\n🛒 ENTRADAS (COMPRAS)")
        print(entradas_mes if not entradas_mes.empty else "Nenhuma compra no mês.")

        mov_mes = movimentacoes_df[pd.to_datetime(movimentacoes_df["data"]).dt.month == mes]
        print("\n🔄 MOVIMENTAÇÕES INTERNAS")
        print(mov_mes if not mov_mes.empty else "Nenhuma movimentação interna.")

        print("\n💰 SAÍDAS (VENDAS)")
        if saidas_df.empty:
            print("Nenhuma venda registrada.")
        else:
            saidas_mes = saidas_df[pd.to_datetime(saidas_df["data_de_venda"]).dt.month == mes]
            print(saidas_mes if not saidas_mes.empty else "Nenhuma venda no mês.")

        ops_mes = ops_df[ops_df["mes"] == mes]
        print("\n🏭 ORDENS DE PRODUÇÃO")
        if ops_mes.empty:
            print("Nenhuma OP no mês.")
        else:
            print("\n✅ OPs CONCLUÍDAS")
            concluidas = ops_mes[ops_mes["status"] == "CONCLUIDA"]
            print(concluidas if not concluidas.empty else "Nenhuma OP concluída.")

            print("\n⛔ OPs NÃO CONCLUÍDAS")
            nao_concluidas = ops_mes[ops_mes["status"] == "NAO CONCLUIDA"]
            print(nao_concluidas if not nao_concluidas.empty else "Nenhuma OP não concluída.")

# =========================
# MAIN
# =========================
def main():
    print("\n📦 Criando produtos...")
    produtos_df = criar_produtos_dataframe()

    print("\n🧩 Gerando BOM...")
    bom = gerar_bom_fixa(produtos_df)

    print("\n📊 Gerando demanda...")
    demanda_df = gerar_demanda_mensal(produtos_df, ANO_PLANEJAMENTO)

    print("\n📦 Criando estoque inicial...")
    estoque = criar_estoque_inicial(produtos_df)

    # Ajuste: Demanda aumentada para cálculo de compras
    demanda_compra = demanda_df.copy()
    demanda_compra["quantidade"] = (demanda_compra["quantidade"] * 1.2).astype(int)

    print("\n🛒 Gerando compras de MP baseadas na produção real...")
    entradas_df = gerar_entradas_mp(demanda_compra, produtos_df, bom, estoque)

    movimentacoes_internas = []
    ops_status = []
    saidas = []

    # =========================
    # PROCESSAMENTO MENSAL
    # =========================


    for mes in range(1, 13):
        print("\n" + "="*120)
        print(f"📆 PROCESSANDO MÊS {mes:02d}/{ANO_PLANEJAMENTO}")
        print("="*120)

        # Estoque do mês
        estoque_trabalho = estoque.copy()

        # 1️⃣ Entradas (compras MP)
        estoque_trabalho = atualizar_estoque_compras(estoque_trabalho, entradas_df, ANO_PLANEJAMENTO, mes)

        # 2️⃣ Produção (Movimentações internas)
        demanda_mes = demanda_df[demanda_df["mes"] == mes]
        mov_df, ops_df, estoque_trabalho = gerar_movimentacoes_internas(demanda_mes, bom, estoque_trabalho)
        movimentacoes_internas.append(mov_df)
        ops_status.append(ops_df)

        # 3️⃣ Saídas (vendas de PA)
        saida_mes, estoque_trabalho = gerar_movimentacoes_saida(demanda_mes, estoque_trabalho)
        if not saida_mes.empty:
            saidas.append(saida_mes)

        # Fechamento do mês
        estoque = estoque_trabalho.copy()

        # Estoque final do mês
        print("\n📦 ESTOQUE NO FINAL DO MÊS")
        estoque_mes = estoque.merge(produtos_df[["id", "tipo", "nome"]], left_index=True, right_on="id")
        print(estoque_mes.sort_values(["tipo", "id"]).reset_index(drop=True))

    # =========================
    # Consolidação final
    # =========================
    movimentacoes_internas_df = pd.concat(movimentacoes_internas, ignore_index=True)
    ops_status_df = pd.concat(ops_status, ignore_index=True)
    saidas_df = pd.concat(saidas, ignore_index=True) if saidas else pd.DataFrame()

    print("\n🏭 STATUS DAS OPs (GERAL)")
    print(ops_status_df["status"].value_counts())

    # =========================
    # Exportação para Excel
    # =========================
    gerar_excel_pcp(produtos_df, entradas_df, movimentacoes_internas_df, saidas_df, ops_status_df, ANO_PLANEJAMENTO)

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    main()
