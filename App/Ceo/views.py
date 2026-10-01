from flask import (flash,
redirect,render_template,current_app,url_for,request)
from ..Ceo import Ceo
from .forms import ProductForm,UpdateForm
from datetime import datetime
from flask_login import current_user,login_required
from ..models import User,Order,Product
from App import db
from App.decorators import Ceo_required
import os
from werkzeug.utils import secure_filename as sf
import secrets


def save_img(img,folder):
    token=secrets.token_hex(4)
    _, f_ext=os.path.splitext(img.filename)
    img_name=token+f_ext
    img_path=os.path.join(folder,img_name)
    img.save(img_path)
    return img_name

Date=datetime.utcnow()

@Ceo.route('/addproduct',methods=['POST','GET'])
@Ceo_required
@login_required
def add_product():
    form=ProductForm()
    if form.validate_on_submit():
        name=form.name.data
        price=form.price.data
        specs=form.specs.data
        img=form.img.data
        if img:
            filename=save_img(img,current_app.config['UPLOAD_FOLDER'])        
        product=Product(name=name,specs=specs,img=filename,price=price)
        db.session.add(product)
        db.session.commit()
        flash('Product added','info')
    return  render_template('product/add.html',form=form,date=Date)


@Ceo.route('/update/<int:id>',methods=['POST','GET'])
@login_required
def update_product(id):
    product=Product.query.filter_by(id=id).first_or_404()
    form=UpdateForm()
    name=form.name.data
    specs=form.specs.data
    img=form.img.data
    price=form.price.data
    if form.validate_on_submit():
        product=Product(name=name,specs=specs,img=img,price=price)
        db.session.commit()
        flash('Product updated','success')
    form.name.data=product.name
    form.specs.data=product.specs
    form.price.data=product.price
    return  render_template('product/update.html',form=form,date=Date)

