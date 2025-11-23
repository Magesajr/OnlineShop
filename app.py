from flask import Flask,render_template,redirect,flash,url_for
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap5
from util import (generate_token,order_track,CONSUMER_KEY_DEMO,
CONSUMER_SECRET_DEMO,
payment_form,subimit_order,payment_email)
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (BooleanField,EmailField,FloatField,SelectField,
StringField,SubmitField,TelField)
from wtforms.validators import DataRequired,Length,Email,ValidationError,Optional


app=Flask(__name__,template_folder='templetes')
app.config['SECRET_KEY']='you nvr guees'
app.config['consumer_secret']=CONSUMER_SECRET_DEMO
app.config['consumer_key']=CONSUMER_KEY_DEMO
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('PASSWORD')


bootstrap=Bootstrap5(app)
mail=Mail(app)
date=datetime.utcnow()


class BillFillForm(FlaskForm):
    choices=['USD','TZS']
    email=EmailField('email',validators=[Email()])
    phone=TelField('phone',validators=[Optional(),Length(10,13)])
    Amount=FloatField('Amount',validators=[DataRequired()]) 
    city=StringField('city',validators=[Optional()])
    currency=SelectField('currency',choices=choices)
    description=StringField('payment description',validators=[Optional()])
    shipped=BooleanField('Need a deliverly?',validators=[Optional()])
    submit=SubmitField('Pay')

@app.route('/payment',methods=['GET','POST'])
def booking():
    global submit
    global email
    global headers
    
    payload_token={
    'consumer_key':app.config['consumer_key'],
    'consumer_secret':app.config['consumer_secret']}   
    headers={'Authorization':f'Bearer {generate_token(payload_token)}'}
    form=BillFillForm()
    city=form.city.data
    phone=form.phone.data
    email=form.email.data
    amount=form.Amount.data
    curr=form.currency.data
    deliverly=form.shipped.data
    desc=form.description.data
    if form.validate_on_submit():
        if deliverly and curr == 'TZS':
            amount += 20*1000
        elif deliverly and curr == 'USD':
            amount += 20
        pay=payment_form(email,phone,amount,desc,city,curr)
        submit=subimit_order(pay,headers)
        if submit['status']=="200":        
            return redirect(submit['redirect_url'])
        else:
            return submit['message']
    return render_template('payment.html',form=form,date=date)

@app.route('/success',methods=['POST','GET'])
def send_email():
    params=order_track(submit['order_tracking_id'],headers)
    msg=payment_email(app.config['MAIL_USERNAME'],email,params)
    mail.send(msg)
    flash(f'An email has been sent to your Account,\
           Your payment was {params['payment_status_description']},\
                  {params['description']}','primary')
    return render_template('success.html')

if __name__ =='__main__':
    app.run(port=3000)
