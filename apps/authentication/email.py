from flask_mail import Message
from flask import current_app
from .extensions import mail

def send_reset_password_email(email, reset_url):
    msg = Message(subject="Reset Password",
                  recipients=[email],
                  html=f"Para restablecer tu contraseña, haz clic en el siguiente enlace: <a href='{reset_url}'>Restablecer contraseña</a>")
    mail.send(msg)
