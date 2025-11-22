import requests as r
import secrets as s
from flask_mail import Message

#test creditials 
PESAPAL_AUTH_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken'
PESAPAL_REG_DEMO='https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN'
PESAPAL_SUBMIT_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest'
PESAPAL_ORDER_CANCEL_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/CancelOrder'
PESAPAL_REFUND_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/RefundRequest'
PESAPAL_ORDER_TRACK_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId='
IPN_DEMO='a68237b3-cf86-4902-8213-dbf9e39e6de5'

CONSUMER_KEY_DEMO='ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8'
CONSUMER_SECRET_DEMO='q27RChYs5UkypdcNYKzuUw460Dg='


def generate_token(pay_load):
    res=r.post(PESAPAL_AUTH_DEMO,json=pay_load).json()
    token=res['token']
    return token

headers={
    'Authorization':f'Bearer '}


def register():
    payload_register={
    "url": "http://localhost:5000/register",
    "ipn_notification_type": "GET"}
    res=r.post(PESAPAL_REG_DEMO,headers=headers,json=payload_register).json()
    return res['ipn_id']


def payment_form(email,phone,amount:float,desc,city,curr:str):   
    payment_request={
        "id":s.token_urlsafe(10),
        "currency": curr,
        "amount": amount,
        "description": desc,
        "callback_url": "http://localhost:3000/success",
        "cancellation_url": "http://localhost:5000/cancel",
        "redirect_mode": "",
        "notification_id": f'{IPN_DEMO}',
        "branch": "Magesa Istore - HQ",
        "billing_address": {
            "email_address":f"{email}",
            "phone_number": f"{phone}",
            "country_code":"TZ",
            "first_name":"Samson",
            "middle_name": "magesa",
            "last_name": "jounior",
            "line_1": "ReedemHope LTD",
            "line_2": "",
            "city": city,
            "state": "Dar-es-salaam",
            "postal_code": "2040",
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
    List=r.post(PESAPAL_SUBMIT_DEMO,headers=headers,json=customer_details).json()
    return List

params={
    'payment_method':'',
    'amount':'',
    'created_date':'',
    'payment_status_description':''}

def order_track(order_id,headers):
    res=r.get(PESAPAL_ORDER_TRACK_DEMO+order_id,headers=headers).json()
    return res

subject='<<--Payment Recipt-->>'
def payment_email(sender,to,param,subject=subject,**kwargs):
    msg=Message(subject,recipients=[to],sender=sender)
    msg.body=f'''Payment Details
payment_method:{param['payment_method']}
amount:{param['amount']}
currency:{param['currency']}
account:{param['payment_account']}
status:{param['payment_status_description']}
transaction:{param['description']}
confimation_code:{param['confirmation_code']}
date:{param['created_date']}'''
    #msg.attach(file,data=data,content_type='image/png')
    return msg
