# -*- coding: utf-8 -*-
"""
Created on Tue May 16 10:00:08 2023

@author: james
"""

from flask import Flask
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import request
#from twilio.rest import Client

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World PUTO"

@app.route("/correo")
def enviarCorreo():
    destino = request.args.get("destino")
    asunto = request.args.get("asunto")
    mensaje = request.args.get("mensaje")
    hashString = request.args.get("hash")
    
    print("DESTINO", destino, asunto, mensaje)
    
    if hashString == os.environ.get("SECURITY_HASH"):        
        message = Mail(
        from_email=os.environ.get("email_from"),
        to_emails= destino,
        subject=asunto,
        html_content=mensaje)
    
        print("MENSAJE", message)
    
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            return "OK"
      
        except Exception as e:
            return "KO"
    
    
if __name__ == "__main__":
    app.run()