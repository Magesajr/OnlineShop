import secrets
from flask import url_for,current_app,render_template
from itsdangerous.url_safe import URLSafeTimedSerializer as s
from flask_mail import Message
from ..import mail  


def generate_token():
    pin=secrets.token_hex(3)
    t=s(pin,salt='login')
    token=t.dumps({'login':pin})
    return  {'pin':pin,
             'token':token}

def digest_token(user_token,token,max_age):
    pin=s(user_token)
    try:
        key=pin.loads(token,max_age,salt='login')['login']
    except:
        return False
    return secrets.compare_digest(key,user_token)

def token_email(subject,token,sender,reciptient,**kwargs):
    msg=Message(subject,recipients=[reciptient],sender=sender)
    msg.body='Use this Token to login to your Account'
    msg.html=render_template('mails/token.html',token=token)
    mail.send(msg)

    