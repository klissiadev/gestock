import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Templates Padrão de Título de mensagem e Corpo
TITLE = "[Aviso Automático] Produto abaixo do estoque mínimo"
BODY = """
Prezados(as),
Este é um aviso gerado automaticamente pelo GESTOCK.
O produto {nome_produto} encontra-se abaixo do nível mínimo estabelecido e necessita de reposição.
* Detalhes do produto:
- Nome: {nome_produto}
- Código/SKU: {codigo_produto}
- Quantidade atual: {qtde_atual}
- Estoque mínimo: {estoque_minimo}
Solicitamos que o setor financeiro providencie a liberação necessária para a reposição.
Este e-mail é automático e não requer resposta.
Atenciosamente,
GESTOCK
"""

# Constantes
SMTP_SERVER = "smtp.gmail.com"
TLS_PORT = 587
EMAIL = "gestock.assistente@gmail.com"
PASSWORD = "cruc jncx vzsw ghns"
TO_EMAIL = "juliooujc@gmail.com"

# Formatação de template para cada produto (exemplo abaixo)
message_body = BODY.format(
    nome_produto="Resistor 1kOhm",
    codigo_produto="XA3FJKAEFOCVKAWFDKA",
    qtde_atual=5,
    estoque_minimo=10
)

def mail_service():
    # Criando objeto de mensagem com cabeçalhos
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = TITLE
    
    # Adicionando corpo do e-mail
    msg.attach(MIMEText(message_body, "plain"))
    
    # Conexão SMTP
    smtp_service = smtplib.SMTP(SMTP_SERVER, TLS_PORT)
    smtp_service.starttls()
    smtp_service.login(EMAIL, PASSWORD)
    
    # Envio
    smtp_service.sendmail(EMAIL, TO_EMAIL, msg.as_string())
    smtp_service.quit()

# DEBUG: Chamando a função
# mail_service()

    

