import os
import pandas as pd
from datetime import datetime
from flask import Flask,request,render_template,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import current_user,LoginManager,login_user,UserMixin
from wtforms import BooleanField,StringField,SubmitField,DateField
from wtforms.validators import DataRequired,Length,Email
import requests as r

base=os.path.abspath(os.path.dirname(__file__))
templates='/home/magesajr/JAVA/App/templetes'

app=Flask(__name__, template_folder=templates)
app.config['SECRET_KEY']='my secretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db' 

db=SQLAlchemy(app)
moment=Moment(app)
bootstrap=Bootstrap5(app)
manager=LoginManager(app)


@manager.user_loader
def load_user(id):
     return User.query.get(int(id))


class User(UserMixin,db.Model):
     __table_name__='users'
     id=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.String(255))
     date=db.Column(db.DateTime())

     def __repr__(self):
          return f'{self.name} since {self.date}'

class RegisterForm(FlaskForm):
     name=StringField('name',validators=[DataRequired()])
     email=StringField('email',validators=[DataRequired()])
     date=DateField('date',default=datetime.utcnow,format="%Y,%b~%d")
     submit=SubmitField('Register')

class LoginForm(FlaskForm):
     name=StringField('name',validators=[DataRequired()])
     email=StringField('email',validators=[DataRequired(),Email()])
     submit=SubmitField('login')


@app.before_request
def create_table():
     db.create_all()


@app.route('/register',methods=['POST','GET'])
def register():
    flash(f'welcome to our I store','info')
    form=RegisterForm()
    Date=datetime.utcnow()
    if form.validate_on_submit():
        email=form.email.data
        name=form.name.data
        date=form.date.data
        user=User(name=name,date=date)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html',form=form,date=Date)


@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    Date=datetime.utcnow()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        flash('Invalid credentials','danger')
        return redirect('https://google.com')
    return render_template('login.html',form=form,date=Date)


@app.route('/',methods=['GET'])
def home():
     flash(f'welcome to our I store','info')
     return '<h1> hello welcome customer </h1>'


     

def Basefile():
    files=['config','__init__','models','run']
    for file in files:
        if os.path.exists(os.path.join(base,file)):
            print(f'{file} exists')
        with open(os.path.join(base,file+'.py'),'w'):
                  pass
        print(file,'created')
    return 'Done'

def BaseDirs(name:str):
    files=['__init__','views','forms','util']
    templates=['home','login','register','base','logout']
    if os.path.exists(os.path.join(base,name)):
        print(f' directrory {name} already exists')
    elif not os.path.exists(os.path.join(base,name)):
        out=os.path.join(base,name)
        dir=os.makedirs(out)
        for file in files:
            with open(os.path.join(out, file+'.py'),'w'):
                pass
    #os.remove(out)
            print(out,'created')
   
if __name__ =='__main__':
    BaseDirs('Ceo')
    app.run(debug=True)

