from flask import (flash,session,
redirect,render_template,current_app,url_for,request)
from ..main import main
from .util import generate_token,digest_token,token_email
from .forms import RegisterForm,LoginForm,TokenForm
from datetime import datetime,timedelta as delta
from flask_login import (login_required, 
current_user,login_user,logout_user)
from ..models import User,Order,Product
from App import db
from App.config import config as c
from supabase import Client,create_client

url:str=c.SUPABASE_URL
key:str=c.SUPABASE_KEY

supabase:Client=create_client(url,key)

Date=datetime.utcnow()

@main.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        flash('Your Already registered','danger')
        return redirect(url_for('.home'))
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
    session['login_token'] = generate_token()
    t=session['login_token']['pin']
    if form.validate_on_submit():
        email=form.email.data
        token_email('LOGIN TOKEN',t,current_app.config['MAIL_USERNAME'],email)
        return redirect(url_for('.login'))
    return render_template('main/token.html',form=form,date=Date,title='Login-Token')


@main.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        flash('You Have Already Logged In','warning')
        return redirect(url_for('.home'))
    if form.validate_on_submit():
        email=form.email.data
        token=form.token.data
        remember=form.remember.data
        next=request.args.get('Next')
        user=User.query.filter_by(email=email).first()
        session.permanent=True
        if user and digest_token(token,session['login_token']['token'],180):
            login_user(user,remember,
                       duration=current_app.config['REMEMBER_COOKIE'])
            if not next or next.startswith('/'):
                next=url_for('.home')
            return redirect(next)
        else:
            flash('Invalid or Expired token send new one','danger')
            return redirect(url_for('.token'))
    return render_template('login.html',form=form,date=Date,title='Login-Page')


@main.route('/logout')
def logout():
    logout_user()
    flash('you have logout','danger')
    return render_template('base.html',title='Sign-Out')



@main.route('/',methods=['GET'])
def home():
    page=request.args.get('page',type=int)
    pagin=Product.query.paginate(page=page,per_page=4)
    products=pagin.items
    image_url=supabase.storage.from_('onlineshop').get_public_url
    return render_template('main/home.html',image_url=image_url,
                           products=products,title='HomeStore',pagin=pagin)


@main.route('/welcome',methods=['GET'])
def welcome_page():
    flash(f'Welcome to Our Online Store We Offer self-Service','info')
    return render_template('index.html')



@main.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    page=request.args.get('page',type=int)
    user=User.query.filter_by(id=current_user.id).first()
    pagin=user.orders.order_by(Order.date_ordered.desc()).paginate(page=page,per_page=7)
    orders=pagin.items
    pagin_pays=user.orders.filter_by(paid=True).paginate(page=page,per_page=7)
    pays=pagin_pays.items
    return render_template('product/users_order.html',pays=pays,Pg=pagin_pays,
                           orders=orders,title='My-Orders',pagin=pagin)
