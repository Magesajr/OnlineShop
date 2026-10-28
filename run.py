from flask import Flask,url_for,redirect,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from wtforms import StringField,FloatField,SubmitField,DateField
from  flask_sqlalchemy import SQLAlchemy
from  flask_migrate import Migrate
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+'dev.sqlite'
app.config['SECRET_KEY']="you will never guess"

db=SQLAlchemy(app)
migrate=Migrate(app,db,"mauzo_migration")
bootstrap=Bootstrap5(app)


class Mauzo(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,index=True)
	qty=db.Column(db.Float,nullable=False)
	price=db.Column(db.Float,index=True,nullable=False)
	date=db.Column(db.DateTime(timezone=True),default=datetime.utcnow)


class Manunuzi(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,index=True)
	qty=db.Column(db.Float,nullable=False)
	price=db.Column(db.Float,index=True,nullable=False)
	date=db.Column(db.DateTime(timezone=True),default=datetime.utcnow)


class MauzoForm(FlaskForm):
	name=StringField('jina la bidhaaa',validators=[DataRequired()])
	qty=FloatField('idadi',validators=[DataRequired()],description='robo 0.25,nusu 0.5,robotatu 0.75')
	price=FloatField('bei ya kuuza',validators=[DataRequired()])
	date=DateField('tarehe',default=datetime(2026,10,27))
	submit=SubmitField('ingiza Mauzo')
	

@app.route('/operations',methods=['GET'])
def db_init():
	d=Manunuzi.query.filter_by(id=7).first()
	db.session.delete(d)
	db.session.commit()
	flash(f'{d.name} deleted','info')
	return redirect(url_for('.index'))


@app.route('/mauzo',methods=['GET','POST'])
def index():
	form=MauzoForm()
	page=request.args.get('page',1,type=int)
	pagin=Mauzo.query.paginate(page=page,per_page=10)
	table=pagin.items
	if form.validate_on_submit():
		name=form.name.data
		qty=form.qty.data
		price=form.price.data
		date=form.date.data
		uza=Mauzo(name=name,qty=qty,price=price,date=date)
		db.session.add(uza)
		db.session.commit()
		flash('mauzo yamekamilika','success')
		return redirect(url_for('.index'))
	return render_template('index.html',form=form,table=table,pagin=pagin)


@app.route('/manunuzi',methods=['GET','POST'])
def index_nunua():
	form=MauzoForm()
	page=request.args.get('page',1,type=int)
	pagin=Manunuzi.query.paginate(page=page,per_page=10)
	table=pagin.items
	if form.validate_on_submit():
		name=form.name.data
		qty=form.qty.data
		price=form.price.data
		date=form.date.data
		nunua=Manunuzi(name=name,qty=qty,price=price,date=date)
		db.session.add(nunua)
		db.session.commit()
		flash('manunuzi yamekamilika','success')
		return redirect(url_for('.index_nunua'))
	return render_template('index.html',form=form,table=table,pagin=pagin)




if __name__=='__main__':
	app.run(debug=True,port=3000)

