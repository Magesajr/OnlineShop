from datetime import datetime
from App import db
import os, secrets as s,time
import requests as r
from ..payment import payment
from App.models import Product,Order
from .forms import BillFillForm
from flask_login import login_required,current_user
from flask import ( current_app,session,request,jsonify,
flash,render_template,redirect,url_for)
from App.decorators import Ceo_required
import qrcode as qr

import secrets,uuid
from .forms import LipaInitForm,LipaWithdrawForm
from .util import (refund_email,submit_order,lipa_status,
generate_token,payment_form,order_track,payment_email,
lipa_collect,lipa_token,X_sgn,lipa_withdraw)


date=datetime.utcnow()

@payment.route('/order/<int:id>',methods=['POST','GET'])
@login_required
def create_orders(id):
    product=Product.query.filter_by(id=id).first_or_404()
    name=product.name
    date=datetime.utcnow()
    user_id=current_user.id
    product_id=product.id    
    order=Order(item_name=name,date_ordered=date,user_id=user_id,product_id=product_id,paid=False,shipped=False)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('main.profile'))


@payment.route('/orders',methods=['POST','GET'])
@login_required
@Ceo_required
def orders():
    page=request.args.get('page',type=int)
    pagin=Order.query.order_by(Order.date_ordered.desc()).\
    paginate(page=page,per_page=10)
    users_order=pagin.items
    flash(f'My orders','info')    
    return render_template('product/users_order.html',
                           orders=users_order,Title='Orders',pagin=pagin)

@payment.route('/order',methods=['POST','GET'])
@login_required
@Ceo_required
def order():
    users_order=Order.query.all()
    flash(f'All orders','info')    
    return render_template('product/order.html',orders=users_order,Title='All Orders')


@payment.route('/payment/<int:id>',methods=['POST','GET'])
@login_required
def init_payment(id):
    order=Order.query.filter_by(item_id=id).first()
    session['order_id']=order.order_id
    payload_token={
    'consumer_key':current_app.config['CONSUMER_KEY_DEMO'],
    'consumer_secret':current_app.config['CONSUMER_SECRET_DEMO']}   
    session['headers']={'Authorization':f'Bearer {generate_token(payload_token)}'}  
    amount=order.product.price
    name=current_user.username
    email=current_user.email
    phone=current_user.phonenumber
    city=current_user.address
    desc=f'payment for {order.product.name}'
    curr='TZS'
    pay=payment_form(amount,desc,name,email,phone,city,curr)
    session['submit']=submit_order(pay,session['headers'])
    submit=session['submit']
    if submit['status']=="200":        
        return redirect(submit['redirect_url'])
    else:
        if current_user.is_CEO():
            message=submit['error']['message']
            flash(message,'danger')
            return render_template('payment/pay_failure.html',message=message)
        else:
            flash('Network busy try again in 5 minutes','danger')
    

@payment.route('/success')
def success_pay():
    order=Order.query.filter_by(order_id=session['order_id']).first()
    if not session['submit']['status'] == "200":
        flash('Not paid Yet','warning')
        return redirect(url_for('.orders'))
        
    #     with open(os.path.join(current_app.config['UPLOAD_FOLDER'],
    #     f'{current_user.username + s.token_hex(2) }.txt'),'w') as f:
    # f.write(f'''<<< Payment Receipt >>>...
    # Buyer:{current_user.username}
    # phone:{current_user.phonenumber}
    # method:{params['payment_method']}
    # currency:{params['currency']}
    # amount:{params['amount']}
    # confirmation_code:{params['confirmation_code']}
    # time:{params['created_date']}
    #         ''')                   
    else:
        params=order_track(session['submit']['order_tracking_id'],session['headers'])
        if params['payment_status_description']=='Completed':
            order.paid=True
            db.session.commit()
            data=f'''<<< Payment Receipt >>>...
method:{params['payment_method']}
currency:{params['currency']}
amount:{params['amount']} 
confirmation_code:{params['confirmation_code']}
time:{params['created_date']}
order_id:{session["order_id"]}'''
            Qr=qr.QRCode(
                version=1,
                error_correction=2,
                box_size=4,
                border=2
            )
            Qr.add_data(data)
            img=Qr.make_image(fill_color='blue',back_color='black')
            folder=os.path.join(current_app.config['UPLOAD_FOLDER'])
            file=f'{s.token_hex(3)}'
            img.save(os.path.join(folder,F'{file}.png'))
            with current_app.open_resource(os.path.join(folder,f'{file}.png')) as f:
                payment_email(file,f.read(),current_user.email,params=params)
            os.remove(os.path.join(folder,f'{file}.png'))
            flash(f'Your payment was {params['payment_status_description']},\
                  {params['description']}','primary')
            return redirect(url_for('main.profile'))
        
        else:
            flash('payment failed','danger')
            return redirect(url_for('main.profile'))
        



@payment.route('/cancel')
def cancel_pay():
    res=r.post(current_app.config['PESAPAL_ORDER_CANCEL_DEMO'],headers=session['headers'],
               data={'order_tracking_id':session['submit']['order_tracking_id']}).json()
    return render_template('payment/cancel_pay.html',res=res)



@payment.route('/booking',methods=['GET','POST'])
@login_required
def Refund():
    form=BillFillForm()
    amount=form.Amount.data
    email=form.email.data
    name=form.name.data
    phone=form.phonenumber.data
    if form.validate_on_submit():
        refund_email('payment refund',current_app.config['MAIL_USERNAME'])
        return render_template('payment/invoice.html')
    return render_template('payment/refund.html',form=form,date=date)



@payment.route('/lipa/init/<string:order_id>',methods=['POST','GET'])
def lipa_init(order_id):
    form=LipaInitForm()
    if form.validate_on_submit():
        network=form.provider.data
        phone=form.phone.data
        order=Order.query.filter_by(order_id=order_id).first()
        session['order_id']=order_id
        amount=str(order.product.price)

        body={
            'requestId':f'{uuid.uuid4()}',
            'providerCode':network,
            'msisdn':phone,
            'amount':str(100),
            'callbackUrl':f'{url_for('.lipa_query',_external=True,id=123)}',
            'reference':f'{current_user.username}',
            'narration':'System Subscription'
        }
        headers={
            'Authorization':f'Bearer {lipa_token()}',
            'X-Signature':f'{X_sgn(body,'post',current_app.config['LIPA_COLLECT'])}',
            'X-Idempotency-Key':f'{secrets.token_hex(10)}',
            'Content-Type':'application/json'
        }
        response=lipa_collect(headers,body)
        if response['status']=='SUCCESS':
            session['trans_id']=response['data']['transactionId']
            return redirect(url_for('.lipa_query',id=session['trans_id']))
        else:
            flash(response['message'],'danger')
    return render_template('payment/refund.html',form=form,date=date)


@payment.route('/lipa/status/<id>/',methods=['POST','GET'])
def lipa_query(id):
    headers={
        'Authorization':f'Bearer {lipa_token()}',
        'X-Signature':f'{X_sgn(id,'get',current_app.config['LIPA_QUERY']+id)}',
        'X-Idempotency-Key':f'{secrets.token_hex(10)}',
        'Content-Type':'application/json'
    }
    response=lipa_status(headers,id)
    if not response['data']['status']=='SUCCESS':
        time.sleep(20)
        response_2=lipa_status(headers,id)
    #return jsonify({'data':response_2['data']['status']})
    # print(response)
    #LOGIC AFTER THE PRODUCT IS PAID
    if response_2['data']['status'] =='SUCCESS':
        flash(f'Payment was SuccessFully check your receipt on your email','success')
        order=Order.query.filter_by(order_id=session['order_id']).first()
        order.paid=True
        db.session.commit()
        return redirect(url_for('main.profile'))
    else:
        flash(f'Payment failed','danger')      
        return redirect(url_for('main.profile'))



@payment.route('/lipa/withdraw',methods=['POST','GET'])
def lipa_self():
    form=LipaWithdrawForm()
    if form.validate_on_submit():
        network=form.provider.data
        amount=form.amount.data
        phone=form.phone.data

        body={
            "requestId":f'{uuid.uuid4()}',
            'providerCode':network,
            'msisdn':phone,
            'amount':amount,
            'reference':f'{current_user.username}',
            'narration':'Admin Personal Withdraw'
        }

        headers={
            'Authorization':f'Bearer {lipa_token()}',
            'X-Signature':f'{X_sgn(body,'post',current_app.config['LIPA_MINE'])}',
            'X-Idempotency-Key':f'{secrets.token_hex(10)}',
            'Content-Type':'application/json'
        }
        response=lipa_withdraw(headers,body)
        print(response)
        flash(response['message'],'info')
        return redirect(url_for('main.home'))
    return render_template('payment/refund.html',form=form,date=date)
