from .util import (
refund,refund_email,
refund_form,payment_form,
payment_email,subimit_order,
order_track,generate_token)
from datetime import datetime
from App import db
import os, secrets as s
import requests as r
from ..payment import payment
from App.models import Product,Order
from .forms import BillFillForm,RefundForm
from flask_login import login_required,current_user
from flask import ( current_app,request,jsonify,g,
flash,render_template,redirect,url_for,send_file)
from App.decorators import Ceo_required
import qrcode as qr

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
    return render_template('product/order.html')


@payment.route('/orders',methods=['POST','GET'])
@login_required
def orders():
    users_order=Order.query.filter_by(user_id=current_user.id)\
    .order_by(Order.date_ordered.desc()).all()
    flash(f'My orders','info')    
    return render_template('product/users_order.html',orders=users_order,Title='Orders')

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
    global headers 
    global submit
    global order_id
    
    order=Order.query.filter_by(item_id=id).first()
    order_id=order.order_id
    payload_token={
    'consumer_key':current_app.config['CONSUMER_KEY_DEMO'],
    'consumer_secret':current_app.config['CONSUMER_SECRET_DEMO']}   
    headers={'Authorization':f'Bearer {generate_token(payload_token)}'}  
    amount=order.product.price
    name=current_user.username
    email=current_user.email
    phone=current_user.phonenumber
    city=current_user.address
    desc=f'payment for {order.product.name}'
    curr='TZS'
    pay=payment_form(amount,desc,name,email,phone,city,curr)
    submit=subimit_order(pay,headers)
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
    order=Order.query.filter_by(order_id=order_id).first()
    if not submit:
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
        params=order_track(submit['order_tracking_id'],headers)
        if params['payment_status_description']=='Completed':
            order.paid=True
            db.session.commit()
            data=f'''<<< Payment Receipt >>>...
method:{params['payment_method']}
currency:{params['currency']}
amount:{params['amount']}
confirmation_code:{params['confirmation_code']}
time:{params['created_date']}
order_id:{order_id}'''
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
            return redirect(url_for('.orders'))
        
        #render_template('payment/success_pay.html',param=params)
        else:
            flash('payment failed','danger')
            return redirect(url_for('.orders'))
        


@payment.route('/payments')
@login_required
@Ceo_required
def user_payments():
    order=Order.query.filter_by(paid=True).all()
    return render_template('payment/init.html',order=order,date=date)

@payment.route('/cancel')
def cancel_pay():
    res=r.post(current_app.config['PESAPAL_ORDER_CANCEL_DEMO'],headers=headers,
               data={'order_tracking_id':submit['order_tracking_id']}).json()
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
