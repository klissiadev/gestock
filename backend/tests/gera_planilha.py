import csv
import random
from datetime import datetime, timedelta, timezone

TOTAL = 45
ARQUIVO = "bora_bill.csv"

# Listas originais mantidas
nomes = [
    "Notebook Gamer X15", "Smartphone Pro Max 256GB", "Monitor LED 27 Polegadas",
    "Teclado Mecânico RGB", "Mouse Gamer 7200 DPI", "Headset Surround 7.1",
    "SSD NVMe 1TB", "HD Externo 2TB", "Placa de Vídeo RTX 4070",
    "Processador Ryzen 7 5800X", "Memória RAM 16GB DDR4", "Fonte 650W 80 Plus Bronze",
    "Roteador Wi-Fi 6", "Webcam Full HD", "Microfone Condensador USB",
    "Impressora Multifuncional Wi-Fi", "Tablet 10 Polegadas 128GB", "Smartwatch Série 8",
    "Caixa de Som Bluetooth 40W", "Hub USB-C 7 em 1", "Carregador Turbo 30W",
    "Power Bank 20.000mAh", "Placa-Mãe ATX Z590", "Cooler Líquido 240mm",
    "Gabinete Mid Tower RGB", "Controle Bluetooth para PC", "Adaptador HDMI para VGA",
    "Projetor Full HD 3500 Lumens", "Antena Wi-Fi USB", "Câmera de Segurança IP",
    "Switch Gigabit 8 Portas", "Notebook Ultrafino 14 polegadas", "Smart TV 55 4K",
    "Chromebook 11 polegadas", "Leitor de Cartão SD/TF", "Pen Drive 128GB",
    "Estabilizador 1000VA", "Nobreak 1500VA", "Placa de Som USB", "Volante Gamer com Pedais"
]

descricoes = [
    "Computadores", "Smartphones", "Monitores", "Periféricos", "Armazenamento",
    "Hardware", "Redes", "Impressão", "Tablets", "Wearables", "Áudio", "Acessórios"
]

tipos_permitidos = ["MP", "SA", "PA"]

# Novo cabeçalho alinhado com o banco de dados
cabecalho = [
    "id", "nome", "descricao", "estoque_minimo", "data_validade", 
    "created_at", "updated_at", "ativo", "tipo"
]

def gerar_data(inicio, fim):
    """Gera uma data aleatória (datetime) entre duas datas."""
    delta = fim - inicio
    return inicio + timedelta(
        days=random.randint(0, delta.days), 
        hours=random.randint(0, 23), 
        minutes=random.randint(0, 59)
    )

# Definindo um fuso horário fixo (ex: UTC-3 / Brasília) para o TIMESTAMP WITH TIME ZONE
fuso_br = timezone(timedelta(hours=-3))

data_inicio = datetime(2023, 1, 1, tzinfo=fuso_br)
data_fim = datetime(2024, 12, 31, tzinfo=fuso_br)

with open(ARQUIVO, "w", newline="", encoding="utf-8") as csvfile:
    # Usando vírgula como delimitador
    writer = csv.writer(csvfile, delimiter=',')
    
    writer.writerow(cabecalho)
    
    for id_produto in range(1, TOTAL + 1):
        nome = random.choice(nomes)
        
        # 20% de chance de não ter descrição
        descricao = random.choice(descricoes) if random.random() > 0.2 else ""
        
        estoque_minimo = random.randint(5, 50)
        
        # --- DATAS ---
        # Data de criação (Completa com Timezone)
        created_at = gerar_data(data_inicio, data_fim)
        str_created_at = created_at.strftime("%Y-%m-%d %H:%M:%S%z")
        
        # Atualização (Completa com Timezone)
        if random.random() > 0.5:
            updated_at = created_at + timedelta(days=random.randint(1, 30))
            str_updated_at = updated_at.strftime("%Y-%m-%d %H:%M:%S%z")
        else:
            str_updated_at = "" # Nulo
            
        if random.random() > 0.3:
            data_validade = created_at + timedelta(days=random.randint(90, 730))
            str_data_validade = data_validade.strftime("%Y-%m-%d")
        else:
            str_data_validade = ""

        ativo = random.choices([True, False], weights=[0.8, 0.2])[0]
        tipo = random.choice(tipos_permitidos)
        
        # Escreve a linha no CSV
        writer.writerow([
            id_produto,
            nome,
            descricao,
            estoque_minimo,
            str_data_validade,  # <--- Vai sair limpinho como "2025-10-25" ou ""
            str_created_at,
            str_updated_at,
            ativo,
            tipo
        ])

print("Arquivo CSV gerado com sucesso:", ARQUIVO)