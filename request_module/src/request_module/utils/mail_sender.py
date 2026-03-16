import os, smtplib, yaml, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Carregamento do template
CONFIG_PATH = os.path.join(os.getcwd(), "..\\request_module\\src\\request_module\\templates\\mail_template.yaml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config_yaml = yaml.safe_load(f)

async def buscar_nomes_produtos(pool, itens_requisicao):
    ids = [item.produto_id for item in itens_requisicao]
    async with pool.connection() as conn:
        cursor = await conn.execute(
            "SELECT id, nome FROM app_core.produtos WHERE id = ANY(%s)",
            (ids,)
        )
        produtos = await cursor.fetchall()
        return {p['id']: p['nome'] for p in produtos}

def workflow_envio_email(dados: dict):
    """Orquestra a montagem e o envio do e-mail"""
    try:
        assunto, corpo_html = preparar_email_html(dados)
        enviar_email_financeiro(corpo_html, assunto)
        logging.info(f"E-mail da req {dados.get('id_banco')} enviado.")
    except Exception as e:
        logging.error(f"Erro no workflow de e-mail: {e}")

def preparar_email_html(dados: dict):
    template = config_yaml['email']['templates']['nova_requisicao']

    linhas_html = ""
    for item in dados['itens']:
        status_prioridade = "SIM" if item.get('prioridade') else "Não"
        
        linhas_html += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{item.get('nome_produto')}</td>
            <td style="padding: 8px; border: 1px solid #ddd; text-align:center;">{item.get('quantidade')}</td>
            <td style="padding: 8px; border: 1px solid #ddd; text-align:center;">{status_prioridade}</td>
        </tr>"""

    # 3. Formata o corpo do e-mail garantindo que as chaves batam com o YAML
    corpo = template['corpo'].format(
        id_banco=dados.get('id_banco'),
        titulo=dados.get('titulo'),
        motivo=dados.get('observacao'),
        tabela_itens=linhas_html,
        data=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
    
    assunto = template['assunto'].format(
        titulo=dados['titulo']
    )
    
    return assunto, corpo

def enviar_email_financeiro(corpo_html: str, assunto: str):
    user = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    destinatario = config_yaml['email']['financeiro_destinatario']

    msg = MIMEMultipart()
    msg['From'], msg['To'], msg['Subject'] = user, destinatario, assunto
    msg.attach(MIMEText(corpo_html, 'html'))

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("TLS_PORT"))) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)