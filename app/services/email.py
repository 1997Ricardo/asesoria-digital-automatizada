import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_DEST = os.getenv("EMAIL_DEST")

def enviar_pdf_por_email(pdf_path: str, asunto: str, mensaje: str):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DEST
    msg.set_content(mensaje)

    # Adjuntar el archivo PDF
    with open(pdf_path, "rb") as f:
        contenido_pdf = f.read()
        msg.add_attachment(
            contenido_pdf,
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_path)
        )

    # Conexión segura al servidor de Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print(f"Correo enviado correctamente a {EMAIL_DEST} con el archivo {os.path.basename(pdf_path)}")