import requests as r
from datetime import datetime
import secrets as s
from flask_mail import Message
from flask import render_template
from config import config as c


payload_token={
    'consumer_key':c.CONSUMER_KEY_DEMO,
    'consumer_secret':c.CONSUMER_SECRET_DEMO}

def generate_token():
    res=r.post(c.PESAPAL_AUTH_DEMO,json=payload_token).json()
    token=res['token']
    return token

headers={
    'Authorization':f'Bearer {generate_token()}'}

payload_register={
    "url": "http://localhost:5000/register",
    "ipn_notification_type": "GET"}

def register():
    res=r.post(c.PESAPAL_REG_DEMO,headers=headers,json=payload_register).json()
    return res['ipn_id']


def payment_form(*a):   
    payment_request={
        "id":s.token_urlsafe(10),
        "currency": "TZS",
        "amount":a[0],
        "description": "" or a[5],
        "callback_url": "http://localhost:5000/success",
        "cancellation_url": "http://localhost:5000/cancel",
        "redirect_mode": "",
        "notification_id": f'{register()}',
        "branch": "Magesa Istore - HQ",
        "billing_address": {
            "email_address": a[1],
            "phone_number": a[2],
            "country_code": "TZ",
            "first_name": a[3],
            "middle_name": "",
            "last_name": "",
            "line_1": "Pesapal Limited",
            "line_2": "",
            "city": "" or a[4],
            "state": "",
            "postal_code": "",
            "zip_code": "" },
            "account_number":"5117531004101187"}  
    return payment_request


def refund_form(code:str,amount:float,username:str,remarks:str):
    refund_header={
        "confirmation_code":code,
        "amount": amount,
        "username":username,
        "remarks": remarks
    }
    return refund_header


def subimit_order():
    List=r.post(c.PESAPAL_SUBMIT_DEMO,headers=headers,
    json=payment_form(25000,'sam@gmail.com','0772697673','magesa','dodoma','sample test')).json()
    return List

#id=subimit_order()['order_tracking_id']

#trans_url=': https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId='+f'{id}'

def tracking_trans(order_id):
    res=r.post(order_id,headers=headers).json() 
    return res

def refund(refund_details):
    refund=r.post(c.PESAPAL_REFUND_DEMO,headers=headers,json=refund_details).json()
    return refund['message']

print(subimit_order())

