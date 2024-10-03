import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_email(recipients, subject, body, attachment_path=None):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL = os.getenv('EMAIL', 'pruebagestion0@gmail.com')  # Retrieve email from env variables or default
    PASSWORD = os.getenv('PASSWORD', 'ogul poqw rdhq bniv')  # Replace with env var or a secure method

    try:
        # Establish the connection with the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        for recipient in recipients:
            try:
                # Create the email
                msg = MIMEMultipart()
                msg['From'] = EMAIL
                msg['To'] = recipient
                msg['Subject'] = subject

                # Attach the email body
                msg.attach(MIMEText(body, 'plain'))

                # Attach the file if provided and exists
                if attachment_path:
                    if os.path.isfile(attachment_path):
                        with open(attachment_path, 'rb') as attachment:
                            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                            msg.attach(part)
                    else:
                        print(f'El archivo {attachment_path} no existe.')

                # Send the email
                server.send_message(msg)
                print(f'Correo enviado a: {recipient}')

            except Exception as e:
                print(f'Ocurrió un error enviando el correo a {recipient}: {e}')

    except Exception as e:
        print(f'Error al conectarse al servidor SMTP: {e}')

    finally:
        server.quit()
