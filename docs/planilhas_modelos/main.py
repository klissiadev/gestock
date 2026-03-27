import pandas as pd

# =========================
# IMPORTS DOS MÓDULOS
# =========================
from demanda import gerar_demanda_mensal, gerar_bom_fixa
from entradas import gerar_entradas_mp
from estoque import criar_estoque_inicial, atualizar_estoque_compras
from movimentacoes_internas import gerar_movimentacoes_internas
from saida import gerar_movimentacoes_saida
from banco import obter_ficha_tecnica, obter_produtos

# =========================
# CONFIG
# =========================
ANO_PLANEJAMENTO = 2025
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
bom_df = obter_ficha_tecnica()


# =========================
# GERADOR DE EXCEL
# =========================
def gerar_excel_pcp(produtos_df, entradas_df, movimentacoes_df, saidas_df, ops_df, ano):
    nome_arquivo = f"pcp_planejamento_{ano}.xlsx"

    # 🔥 AJUSTES IMPORTANTES ANTES DE EXPORTAR
    if not entradas_df.empty:
        entradas_df["preco_de_compra"] = entradas_df["preco_de_compra"].astype(float)
        entradas_df["data_de_compra"] = pd.to_datetime(entradas_df["data_de_compra"]).dt.strftime("%Y-%m-%d")


    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        # produtos_df.to_excel(writer, sheet_name="Produtos", index=False) cria a tabela produto
        entradas_df.to_excel(writer, sheet_name="Entradas_MP", index=False)
        movimentacoes_df.to_excel(writer, sheet_name="Movimentacoes_Internas", index=False)
        if not saidas_df.empty:
            saidas_df.to_excel(writer, sheet_name="Saidas_Vendas", index=False)
        # ops_df.to_excel(writer, sheet_name="Ordens_Producao", index=False) cria a tabela de ordens de produção 
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
    print("\n📦 obtendo produtos...")
    produtos_df = obter_produtos()

    print("\n🧩 Gerando BOM...")
    bom = gerar_bom_fixa(bom_df)

    print("\n📊 Gerando demanda...")
    demanda_df = gerar_demanda_mensal(produtos_df, ANO_PLANEJAMENTO)

    print("\n📦 Criando estoque inicial...")
    estoque = criar_estoque_inicial(produtos_df)

    # 🔥 NÃO inflar demanda (ou use leve ajuste se quiser)
    demanda_compra = demanda_df.copy()

    movimentacoes_internas = []
    ops_status = []
    saidas = []
    entradas_total = []

    # =========================
    # PROCESSAMENTO MENSAL
    # =========================
    for mes in range(1, 13):
        print("\n" + "="*120)
        print(f"📆 PROCESSANDO MÊS {mes:02d}/{ANO_PLANEJAMENTO}")
        print("="*120)

        # Copia do estoque do mês
        estoque_trabalho = estoque.copy()

        # =========================
        # 1️⃣ COMPRAS DO MÊS (🔥 CORREÇÃO)
        # =========================
        demanda_mes_compra = demanda_compra[demanda_compra["mes"] == mes]

        entradas_mes = gerar_entradas_mp(
            demanda_mes_compra,
            produtos_df,
            bom,
            estoque_trabalho
        )

        if not entradas_mes.empty:
            entradas_total.append(entradas_mes)

            # Atualiza estoque com compras do mês
            estoque_trabalho = atualizar_estoque_compras(
                estoque_trabalho,
                entradas_mes,
                ANO_PLANEJAMENTO,
                mes
            )

        # =========================
        # 2️⃣ PRODUÇÃO
        # =========================
        demanda_mes = demanda_df[demanda_df["mes"] == mes]

        mov_df, ops_df, estoque_trabalho = gerar_movimentacoes_internas(
            demanda_mes,
            bom,
            estoque_trabalho
        )

        movimentacoes_internas.append(mov_df)
        ops_status.append(ops_df)

        # =========================
        # 3️⃣ SAÍDAS (VENDAS)
        # =========================
        saida_mes, estoque_trabalho = gerar_movimentacoes_saida(
            demanda_mes,
            estoque_trabalho
        )

        if not saida_mes.empty:
            saidas.append(saida_mes)

        # =========================
        # FECHAMENTO DO MÊS
        # =========================
        estoque = estoque_trabalho.copy()

        # =========================
        # PRINT ESTOQUE
        # =========================
        print("\n📦 ESTOQUE NO FINAL DO MÊS")

        estoque_mes = estoque.merge(
            produtos_df[["id", "tipo", "nome"]],
            left_index=True,
            right_on="id"
        )

        print(
            estoque_mes
            .sort_values(["tipo", "id"])
            .reset_index(drop=True)
        )

    # =========================
    # CONSOLIDAÇÃO FINAL
    # =========================
    movimentacoes_internas_df = pd.concat(movimentacoes_internas, ignore_index=True)
    ops_status_df = pd.concat(ops_status, ignore_index=True)
    saidas_df = pd.concat(saidas, ignore_index=True) if saidas else pd.DataFrame()
    entradas_df = pd.concat(entradas_total, ignore_index=True) if entradas_total else pd.DataFrame()

    print("\n🏭 STATUS DAS OPs (GERAL)")
    print(ops_status_df["status"].value_counts())

    # =========================
    # EXPORTAÇÃO
    # =========================
    gerar_excel_pcp(
        produtos_df,
        entradas_df,
        movimentacoes_internas_df,
        saidas_df,
        ops_status_df,
        ANO_PLANEJAMENTO
    )

    print("\n" + "="*120)
    print("🔎 DEBUG FINAL - ESTRUTURA DOS DATAFRAMES")
    print("="*120)

    def print_info(nome, df):
        print(f"\n📊 {nome}")
        
        if df.empty:
            print("⚠️ DataFrame vazio")
            return
        
        print("\nColunas:")
        print(df.columns.tolist())
        
        print("\nTipos:")
        print(df.dtypes)
        
        print("\nAmostra:")
        print(df.head())


    print_info("PRODUTOS", produtos_df)
    print_info("ENTRADAS", entradas_df)
    print_info("MOVIMENTACOES INTERNAS", movimentacoes_internas_df)
    print_info("SAIDAS", saidas_df)
    print_info("OPS STATUS", ops_status_df)
# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    main()
