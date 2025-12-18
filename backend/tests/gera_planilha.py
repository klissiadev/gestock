import csv
import random
from datetime import datetime, timedelta


TOTAL = 3000
ARQUIVO = "produtos.csv"

nomes = [
    "Arroz Branco 5kg", "Feijão Carioca 1kg", "Macarrão Espaguete 500g",
    "Açúcar Cristal 1kg", "Café Torrado 500g", "Óleo de Soja 900ml",
    "Farinha de Trigo 1kg", "Leite Integral 1L", "Sal Refinado 1kg",
    "Biscoito Cream Cracker 350g","Arroz Parboilizado 1kg", "Feijão Preto 1kg", "Macarrão Parafuso 500g",
    "Açúcar Mascavo 1kg", "Café Solúvel 200g", "Óleo de Girassol 900ml",
    "Farinha de Mandioca 1kg", "Leite Desnatado 1L", "Sal Grosso 1kg",
    "Biscoito Recheado Chocolate 140g",
    "Arroz Integral 1kg", "Feijão Vermelho 1kg", "Macarrão Penne 500g",
    "Açúcar Demerara 1kg", "Café Extra Forte 500g", "Óleo de Milho 900ml",
    "Farinha de Rosca 500g", "Leite Semidesnatado 1L", "Sal Light 1kg",
    "Biscoito Maisena 200g",
    "Arroz Agulhinha 5kg", "Feijão Branco 1kg", "Macarrão Talharim 500g",
    "Açúcar Refinado 1kg", "Café Moído 500g", "Óleo de Canola 900ml",
    "Farinha Integral 1kg", "Leite Zero Lactose 1L", "Sal Rosa 1kg",
    "Biscoito Wafer Morango 140g",
    "Arroz Premium 5kg", "Feijão Fradinho 1kg", "Macarrão Instantâneo 85g",
    "Açúcar Orgânico 1kg", "Café Gourmet 250g", "Óleo Vegetal 900ml",
    "Farinha de Milho 1kg", "Leite em Pó 400g", "Sal Marinho 1kg",
    "Biscoito Água e Sal 350g",
    "Arroz Tipo 1 5kg", "Feijão Jalo 1kg", "Macarrão Cabelo de Anjo 500g",
    "Açúcar de Coco 500g", "Café Tradicional 500g", "Óleo de Palma 900ml",
    "Farinha de Tapioca 1kg", "Leite Condensado 395g", "Sal Iodado 1kg",
    "Biscoito Integral 200g",
    "Arroz Integral 5kg", "Feijão Roxinho 1kg", "Macarrão Lasanha 500g",
    "Açúcar Light 500g", "Café Orgânico 250g", "Óleo de Linhaça 250ml",
    "Farinha de Centeio 1kg", "Creme de Leite 200g", "Sal Temperado 500g",
    "Biscoito de Polvilho 100g",
    "Arroz Cateto 1kg", "Feijão Azuki 1kg", "Macarrão Rigatoni 500g",
    "Açúcar Glacê 500g", "Café Especial 250g", "Óleo de Coco 200ml",
    "Farinha de Amêndoas 200g", "Leite Fermentado 450g", "Sal Defumado 500g",
    "Biscoito de Aveia 200g",
    "Arroz Japonês 1kg", "Feijão Rajado 1kg", "Macarrão Gravata 500g",
    "Açúcar Baunilhado 100g", "Café Descafeinado 250g", "Óleo de Abacate 250ml",
    "Farinha de Arroz 1kg", "Leite de Coco 200ml", "Sal para Churrasco 1kg",
    "Biscoito de Gengibre 150g",
    "Arroz Arbóreo 1kg", "Feijão Mulatinho 1kg", "Macarrão Conchinha 500g",
    "Açúcar Caramelizado 500g", "Café Premium 500g", "Óleo Extra Virgem 500ml",
    "Farinha de Linhaça 500g", "Leite Vegetal 1L", "Sal Especial 500g",
    "Biscoito Amanteigado 200g"
]

descricoes = [
    "Produto alimentício de alta qualidade",
    "Item essencial para o dia a dia",
    "Produto selecionado e embalado com cuidado",
    "Ideal para consumo familiar",
    "Produto com excelente custo-benefício"
]

categorias = ["Alimentos", "Bebidas", "Higiene", "Limpeza", "Mercearia"]

cabecalho = [
    "cod_produto", "nome", "descricao", "categoria",
    "estoque_atual", "estoque_minimo",
    "data_cadastro", "data_validade", "valor_unitario"
]

def gerar_data(inicio, fim):
    """Gera uma data aleatória entre duas datas."""
    delta = fim - inicio
    return inicio + timedelta(days=random.randint(0, delta.days))

data_inicio = datetime(2023, 1, 1)
data_fim = datetime(2024, 12, 31)

with open(ARQUIVO, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    
    writer.writerow(cabecalho)
    
    for i in range(1, TOTAL + 1):
        nome = random.choice(nomes)
        descricao = random.choice(descricoes)
        categoria = random.choice(categorias)
        estoque_atual = random.randint(10, 500)
        estoque_minimo = random.randint(5, 50)
        
        data_cadastro = gerar_data(data_inicio, data_fim)
        data_validade = data_cadastro + timedelta(days=random.randint(90, 730))
        
        valor_unitario = round(random.uniform(5.0, 80.0), 2)
        
        writer.writerow([
            i,
            nome,
            descricao,
            categoria,
            estoque_atual,
            estoque_minimo,
            data_cadastro.strftime("%d/%m/%Y"),
            data_validade.strftime("%d/%m/%Y"),
            valor_unitario
        ])

print("Arquivo CSV gerado com sucesso:", ARQUIVO)