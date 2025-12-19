import csv
import random
from datetime import datetime, timedelta


TOTAL = 3000
ARQUIVO = "produtos.csv"

nomes = [
"Notebook Gamer X15",
"Smartphone Pro Max 256GB",
"Monitor LED 27 Polegadas",
"Teclado Mecânico RGB",
"Mouse Gamer 7200 DPI",
"Headset Surround 7.1",
"SSD NVMe 1TB",
"HD Externo 2TB",
"Placa de Vídeo RTX 4070",
"Processador Ryzen 7 5800X",
"Memória RAM 16GB DDR4",
"Fonte 650W 80 Plus Bronze",
"Roteador Wi-Fi 6",
"Webcam Full HD",
"Microfone Condensador USB",
"Impressora Multifuncional Wi-Fi",
"Tablet 10 Polegadas 128GB",
"Smartwatch Série 8",
"Caixa de Som Bluetooth 40W",
"Hub USB-C 7 em 1",
"Carregador Turbo 30W",
"Power Bank 20.000mAh",
"Placa-Mãe ATX Z590",
"Cooler Líquido 240mm",
"Gabinete Mid Tower RGB",
"Controle Bluetooth para PC",
"Adaptador HDMI para VGA",
"Projetor Full HD 3500 Lumens",
"Antena Wi-Fi USB",
"Câmera de Segurança IP",
"Switch Gigabit 8 Portas",
"Notebook Ultrafino 14 polegadas",
"Smart TV 55 4K",
"Chromebook 11 polegadas",
"Leitor de Cartão SD/TF",
"Pen Drive 128GB",
"Estabilizador 1000VA",
"Nobreak 1500VA",
"Placa de Som USB",
"Volante Gamer com Pedais"

]

descricoes = [
"Computadores",
"Smartphones",
"Monitores",
"Periféricos",
"Armazenamento",
"Hardware",
"Redes",
"Impressão",
"Tablets",
"Wearables",
"Áudio",
"Acessórios",

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