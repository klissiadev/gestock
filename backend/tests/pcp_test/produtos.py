import random
from datetime import date, timedelta
import pandas as pd


# =========================================================
# CONFIG
# =========================================================

TOTAL_POR_TIPO = 15

tipos_produto = ['MP'] * 15 + ['SA'] * 15 + ['PA'] * 15

nomes_produtos = [
    # MP
    'Placa PCB virgem','Microcontrolador ARM','Sensor óptico',
    'Resistor SMD','LED RGB','Capacitor cerâmico','Cristal oscilador',
    'Memória Flash','Conector USB','Conector USB-C','Diodo',
    'Parafuso metálico','Plástico ABS granulado','Solda em pasta','Chip controlador USB',

    # SA
    'Placa do teclado soldada','Placa do mouse com sensor calibrado',
    'Headset com circuito montado','Placa do teclado com firmware gravado',
    'Módulo eletrônico testado','Cabo USB montado','Carcaça do teclado injetada',
    'Carcaça do mouse injetada','Conjunto de switches mecânicos',
    'Teclas (keycaps) produzidas','Módulo wireless montado',
    'Placa de LED RGB montada','Carcaça do headset montada',
    'Conjunto de botões do mouse','Módulo final inspecionado',

    # PA
    'Teclado gamer','Mouse gamer RGB','Headset gamer',
    'Teclado mecânico RGB','Mouse óptico','Headset Bluetooth',
    'Teclado compacto','Mouse sem fio','Headset profissional',
    'Kit teclado + mouse','Teclado corporativo','Mouse corporativo',
    'Headset com microfone','Teclado sem fio','Mouse ergonômico'
]

# =========================================================
# GERADOR DE PRODUTOS
# =========================================================

def criar_produtos():
    produtos = []
    data_base = date.today()

    for idx, (nome, tipo) in enumerate(zip(nomes_produtos, tipos_produto), start=1):

        produto = {
            "id": idx,
            "nome": nome,
            "tipo": tipo,
            "descricao": gerar_descricao(nome, tipo),
            "estoque_minimo": gerar_estoque_minimo(tipo),
            "data_validade": gerar_data_validade(tipo, data_base)
        }

        produtos.append(produto)

    return produtos

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def gerar_descricao(nome, tipo):
    if tipo == 'MP':
        return f"Matéria-prima utilizada no processo de fabricação: {nome}."
    elif tipo == 'SA':
        return f"Produto semiacabado resultante de montagem parcial: {nome}."
    else:
        return f"Produto acabado pronto para venda ao consumidor: {nome}."

def gerar_estoque_minimo(tipo):
    if tipo == 'MP':
        return random.randint(100, 300)
    elif tipo == 'SA':
        return random.randint(40, 120)
    else:  # PA
        return random.randint(20, 60)

def gerar_data_validade(tipo, data_base):
    if tipo == 'MP':
        dias = random.randint(365, 900)
    elif tipo == 'SA':
        dias = random.randint(180, 365)
    else:  # PA
        dias = random.randint(90, 180)

    return data_base + timedelta(days=dias)

def criar_produtos_dataframe():
    produtos = criar_produtos()          # lista de dicionários
    df = pd.DataFrame(produtos)           # converte para DataFrame
    df["data_validade"] = pd.to_datetime(df["data_validade"]).dt.date

    return df

if __name__ == "__main__":
    df_produtos = criar_produtos_dataframe()

    print("\nDataFrame gerado com sucesso!")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(df_produtos)

'''
Gera a tabela de produtos que possui:
- ID
- Nome
- tipo
- descrição
- estoque_minimo
- data_validade

'''

