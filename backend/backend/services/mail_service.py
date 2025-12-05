import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging
import yaml

# Padrão de Log (temporario, deve existir um logger.py responsavel por padronizar TODOS os logs existentes)
logging.basicConfig(
    level=logging.INFO,  # nível mínimo que será exibido
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Carrega o .env + inicializa suas constantes
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
TLS_PORT = int(os.getenv("TLS_PORT", 587))
EMAIL = os.getenv("EMAIL", "")
TO_EMAIL = os.getenv("TO_EMAIL", "")
PASSWORD = os.getenv("PASSWORD", "")

# Carrega o template
def load_template(path="backend\\database\\mail_config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        logging.error("Arquivo de configuração não encontrado")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Erro ao interpretar YAML: {e}")
        return None
    except KeyError as e:
        logging.error(f"Chave ausente no YAML: {e}")
        return None

# Construtor de mensagem do email
def build_message(produtos: list, email_from: str, email_to: str):
    config = load_template()
    if not config:
        return None

    TITLE = config.get("title", "Aviso Automático")
    BODY_TEMPLATE = config.get("body", "Produtos abaixo do estoque mínimo:\n{lista_produtos}")

    # Monta lista de produtos dinamicamente
    lista_produtos = ""
    for p in produtos:
        try:
            lista_produtos += (
                f"- Nome: {p['nome_produto']}\n"
                f"  Código/SKU: {p['codigo_produto']}\n"
                f"  Quantidade atual: {p['qtde_atual']}\n"
                f"  Estoque mínimo: {p['estoque_minimo']}\n\n"
            )
        except KeyError as e:
            logging.error(f"Campo ausente no produto: {e}")
            return None

    # Substitui placeholder no template
    try:
        body = BODY_TEMPLATE.format(lista_produtos=lista_produtos.strip())
    except Exception as e:
        logging.error(f"Erro ao formatar template: {e}")
        return None

    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = TITLE
    msg.attach(MIMEText(body, "plain"))
    return msg

# Disparador de email
def mail_service():
    # Lista de dicionários por enquanto, mas seria bom se fosse lista de objetos PRODUTO
    produtos = [
        {
            "nome_produto": "Resistor 1kOhm",
            "codigo_produto": "XA3FJKAEFOCVKAWFDKA",
            "qtde_atual": 5,
            "estoque_minimo": 10
        },
        {
            "nome_produto": "Capacitor 100uF",
            "codigo_produto": "ZP9DKAJSDAKJDAKJD",
            "qtde_atual": 2,
            "estoque_minimo": 15
        }
    ]

    msg = build_message(produtos, EMAIL, TO_EMAIL)
    if not msg:
        logging.error("Falha ao construir mensagem")
        return

    try:
        with smtplib.SMTP(SMTP_SERVER, TLS_PORT, timeout=10) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        logging.info(f"E-mail enviado para {TO_EMAIL}")
    except smtplib.SMTPAuthenticationError:
        logging.error("Erro de autenticação no servidor SMTP")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"Destinatário inválido: {TO_EMAIL}")
    except smtplib.SMTPConnectError:
        logging.error("Não foi possível conectar ao servidor SMTP")
    except Exception as e:
        logging.error(f"Erro inesperado ao enviar e-mail: {e}")
