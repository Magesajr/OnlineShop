from flask import (flash,
redirect,render_template,current_app,url_for,request)
from ..main import main
from .util import generate_token,digest_token,token_email
from .forms import RegisterForm,LoginForm,TokenForm
from datetime import datetime,timedelta as delta
from flask_login import current_user,login_user,logout_user
from ..models import User,Order,Product
from App import db


Date=datetime.utcnow()

@main.route('/register',methods=['POST','GET'])
def register():
    flash(f'welcome to our I store','info')
    form=RegisterForm()
    Date=datetime.utcnow()
    if form.validate_on_submit():
        email=form.email.data
        address=form.address.data
        name=form.username.data
        phone=form.phonenumber.data
        user=User(username=name,email=email,address=address,phonenumber=phone)
        db.session.add(user)
        db.session.commit()
        flash('you have registered to our store','info')
        return redirect(url_for('.token'))
    return render_template('register.html',form=form,date=Date)


@main.route('/token',methods=['POST','GET'])
def token():
    if current_user.is_authenticated:
        flash('logout first','danger')
        return redirect(url_for('.home'))
    form=TokenForm()
    global login_token
    login_token = generate_token()
    t=login_token['pin']
    if form.validate_on_submit():
        email=form.email.data
        token_email('LOGIN TOKEN',t,current_app.config['APP_ADMIN'],email)
        return redirect(url_for('.login'))
    return render_template('main/token.html',form=form,date=Date)


@main.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('.home'))
    if form.validate_on_submit():
        email=form.email.data
        token=form.token.data
        remember=form.remember.data
        next=request.args.get('Next')
        user=User.query.filter_by(email=email).first()
        if user and digest_token(token,login_token['token'],100):
            login_user(user,remember,duration=delta(days=2))
            if not next or next.startswith('/'):
                next=url_for('.home')
            return redirect(next)
        else:
            flash('Invalid or expired token','danger')
    return render_template('login.html',form=form,date=Date)

@main.route('/logout')
def logout():
    logout_user()
    flash('you have logout','danger')
    return render_template('base.html')



@main.route('/',methods=['GET'])
def home():
    products=Product.query.all()
    flash(f'Welcome to Our Online Store We Offer self-Service','info')    
    return render_template('main/home.html',products=products,title='HomeStore')
