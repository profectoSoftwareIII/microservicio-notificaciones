# -*- coding: utf-8 -*-
"""
Created on Tue May 16 10:00:08 2023

@author: james
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import request
from twilio.rest import Client

app = Flask(__name__)


@app.route("/correo")
def enviarCorreo():
    smtp_server = os.environ["stmp_server"]
    smtp_port = 587
    username = os.environ["username_email"]
    password = os.environ["password_email"]
    from_addr = os.environ["username_email"]
    to_addr =  request.args.get("destino")
    subject = request.args.get("asunto")
    body = "Recordatorio para el usuario de la consulta \n" + request.args.get("mensaje")


        # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))
    
    # Intentar conectarse al servidor SMTP y enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar la conexión TLS
        server.login(username, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente")
        return "OK"
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return "KO"




        
@app.route("/sms")
def enviarSMS():
    destino = request.args.get("destino")
    mensaje = request.args.get("mensaje")
    hashString = request.args.get("hash")

    if hashString == os.getenv("HASH_STRING"):
        try:
            account_sid = os.getenv("account_sid")
            auth_token = os.getenv("auth_token")
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=mensaje, from_=os.getenv("sms_phone"), to="+57" + destino
            )

            return "OK"

        except Exception as e:
            print("error")
            print(e)
            return "KO"
        

        



if __name__ == "__main__":
    app.run()
