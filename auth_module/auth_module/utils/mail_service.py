import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
import yaml
from auth_module.utils.env_loader import load_env_from_root

# Configuração de Log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_env_from_root()
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
TLS_PORT = int(os.getenv("TLS_PORT", 587))
EMAIL = os.getenv("EMAIL", "")
PASSWORD = os.getenv("PASSWORD", "")

TEMPLATE_PATH = os.getenv("FORGOT_PASSWORD")

def load_template(path=TEMPLATE_PATH):
    try:
        # Tenta carregar o YAML. Se não existir, usamos um fallback hardcoded
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.warning(f"Usando templates padrão: {e}")
        return {
            "recovery_title": "Recuperação de Senha - Gestock",
            "recovery_body": "Olá!\n\nRecebemos um pedido para redefinir sua senha. Clique no link abaixo:\n\n{link}\n\nO link expira em 15 minutos."
        }

# Construtor para e-mail
def send_recovery_email(to_email: str, link: str):
    config = load_template()
    subject = config.get("recovery_title", "Recuperação de Senha")
    
    # 1. Pegamos o HTML do YAML e injetamos o link
    html_template = config.get("recovery_body_html", "Clique aqui: {link}")
    html_content = html_template.format(link=link)
    
    # 2. Montamos a mensagem como MULTIPART
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    # 3. Criamos a parte HTML (essencial mudar para "html")
    part_html = MIMEText(html_content, "html")
    msg.attach(part_html)

    # 4. Motor de envio (seu código smtplib)
    try:
        with smtplib.SMTP(SMTP_SERVER, TLS_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        logging.info("E-mail HTML enviado!")
    except Exception as e:
        logging.error(f"Erro no envio: {e}")