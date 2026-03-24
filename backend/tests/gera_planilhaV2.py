import csv
import random
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÕES E REGRAS DE NEGÓCIO (BOM) ---
ARQUIVOS = {
    "produtos": "1_produtos_cadastro.csv",
    "entradas": "2_entradas_mp.csv",
    "movimentacao": "3_movimentacao_interna.csv",
    "saidas": "4_saidas_pa.csv"
}

# Bill of Materials (Receita): O que cada PA consome
RECEITAS = {
    "Notebook Gamer": ["Placa-Mãe", "Memória RAM", "SSD NVMe", "Fonte ATX", "Tela LED"],
    "Smartphone Pro": ["Bateria Li-ion", "Tela OLED", "Placa Lógica", "Câmera Frontal", "Carcaça"]
}

FUSO_BR = timezone(timedelta(hours=-3))
DATA_BASE = datetime(2026, 1, 1, tzinfo=FUSO_BR) # Simulação começando em Jan/2026

# --- FUNÇÕES AUXILIARES ---

def salvar_csv(nome_arquivo, cabecalho, dados):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(dados)

# --- 1. GERAR CADASTRO DE PRODUTOS ---
produtos_rows = []
mps_disponiveis = []
for pa, componentes in RECEITAS.items():
    # Adiciona o PA
    pa_id = len(produtos_rows) + 1
    produtos_rows.append([pa_id, pa, "Produto Acabado", 10, "2028-12-31", "PA"])
    
    # Adiciona as MPs desse PA
    for mp in componentes:
        if mp not in [row[1] for row in produtos_rows]:
            mp_id = len(produtos_rows) + 1
            produtos_rows.append([mp_id, mp, "Matéria-Prima", 20, "", "MP"])
            mps_disponiveis.append({"id": mp_id, "nome": mp})

cabecalho_prod = ["id", "nome", "descricao", "estoque_minimo", "data_validade", "tipo"]
salvar_csv(ARQUIVOS["produtos"], cabecalho_prod, produtos_rows)

# --- 2. MÊS 1: ENTRADA DE MP (COMPRAS) ---
entradas_rows = []
for mp in mps_disponiveis:
    data_compra = DATA_BASE + timedelta(days=random.randint(1, 25))
    entradas_rows.append([
        mp["id"], 100, data_compra.strftime("%Y-%m-%d"), round(random.uniform(50, 500), 2), "Fornecedor Tech"
    ])

cabecalho_ent = ["produto_id", "quantidade", "data_de_compra", "preco_de_compra", "fornecedor"]
salvar_csv(ARQUIVOS["entradas"], cabecalho_ent, entradas_rows)

# --- 3. MÊS 2: MOVIMENTAÇÃO INTERNA (PRODUÇÃO ATÔMICA) ---
# Aqui garantimos que para cada PA que entra, as MPs saem.
mov_rows = []
pa_list = [p for p in produtos_rows if p[5] == "PA"]

for mes_offset in range(30, 60): # Fevereiro
    data_prod = DATA_BASE + timedelta(days=mes_offset)
    
    for pa in pa_list:
        op_numero = f"OP-{random.randint(1000, 9999)}"
        qtd_produzida = random.randint(2, 5)
        
        # ATOMICIDADE: Registra a ENTRADA do PA
        mov_rows.append([pa[0], op_numero, "ENTRADA", qtd_produzida, "Produção", "Estoque PA", data_prod.strftime("%Y-%m-%d")])
        
        # ATOMICIDADE: Registra a SAÍDA de cada MP da receita
        nome_pa = pa[1]
        for mp_nome in RECEITAS[nome_pa]:
            mp_id = next(p[0] for p in produtos_rows if p[1] == mp_nome)
            mov_rows.append([mp_id, op_numero, "SAIDA", qtd_produzida, "Estoque MP", "Produção", data_prod.strftime("%Y-%m-%d")])

cabecalho_mov = ["produto_id", "ordem_de_producao", "tipo", "quantidade", "origem", "destino", "data"]
salvar_csv(ARQUIVOS["movimentacao"], cabecalho_mov, mov_rows)

# --- 4. MÊS 3: SAÍDA PA (VENDAS) ---
saidas_rows = []
for pa in pa_list:
    for _ in range(10): # 10 vendas por produto
        data_venda = DATA_BASE + timedelta(days=random.randint(61, 90))
        saidas_rows.append([
            pa[0], random.randint(1, 3), data_venda.strftime("%Y-%m-%d"), round(random.uniform(2000, 5000), 2), "Cliente Final"
        ])

cabecalho_sai = ["produto_id", "quantidade", "data_de_venda", "preco_de_venda", "cliente"]
salvar_csv(ARQUIVOS["saidas"], cabecalho_sai, saidas_rows)

print("Refatoração concluída. 4 planilhas geradas com integridade de dados.")