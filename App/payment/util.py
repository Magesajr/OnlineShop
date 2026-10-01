import requests as r
import json
from datetime import datetime
import secrets as s
from flask_mail import Message
from App import mail
from flask import current_app
from flask import render_template
from App.config import config as c


def generate_token(pay_load):
    res=r.post(c.PESAPAL_AUTH_DEMO,json=pay_load).json()
    token=res['token']
    return token

headers={
    'Authorization':f'Bearer '}


def register():
    payload_register={
    "url": "http://localhost:5000/register",
    "ipn_notification_type": "GET"}
    res=r.post(c.PESAPAL_REG_DEMO,headers=headers,json=payload_register).json()
    return res['ipn_id']


def payment_form(amount:float,desc,email,phone,name,city,curr:str):   
    payment_request={
        "id":s.token_urlsafe(10),
        "currency": curr,
        "amount": amount,
        "description": "" or desc,
        "callback_url": "http://localhost:5000/success",
        "cancellation_url": "http://localhost:5000/cancel",
        "redirect_mode": "",
        "notification_id": f'{c.IPN_DEMO}',
        "branch": "Magesa Istore - HQ",
        "billing_address": {
            "email_address": email,
            "phone_number": phone,
            "country_code":"TZ",
            "first_name": name,
            "middle_name": "",
            "last_name": "",
            "line_1": "Pesapal Limited",
            "line_2": "",
            "city": "" or city,
            "state": "",
            "postal_code": "",
            "zip_code": "" },
            "account_number":""}  
    return payment_request


def refund_form(code:str,amount:float,username:str,remarks:str):
    refund_header={
        "confirmation_code":code,
        "amount": amount,
        "username":username,
        "remarks": remarks
    }
    return refund_header


def subimit_order(customer_details,headers):
    List=r.post(c.PESAPAL_SUBMIT_DEMO,headers=headers,json=customer_details).json()
    return List

params={
    'payment_method':'',
    'amount':'',
    'created_date':'',
    'payment_status_description':''}

def order_track(order_id,headers):
    res=r.get(c.PESAPAL_ORDER_TRACK_DEMO+order_id,headers=headers).json()
    return res


def refund(refund_details):
    refund=r.post(c.PESAPAL_REFUND_DEMO,headers=headers,json=refund_details).json()
    return refund['message']


subject='<<--Payment Recipt-->>'
def payment_email(file,data,to,subject=subject,**kwargs):
    msg=Message(subject,recipients=[to],sender=current_app.config['APP_ADMIN'])
    msg.body='Payment Details'
    msg.html=render_template('mails/payment_email.html',**kwargs)
    msg.attach(file,data=data,content_type='image/png')
    mail.send(msg)

def refund_email(subject,to,**kwargs):
    msg=Message(subject,recipients=[to],sender=current_app.config['APP_ADMIN'])
    msg.body='The following are you\'re refund details'
    msg.html=render_template('mails/refund.html',**kwargs)
    mail.send(msg)
