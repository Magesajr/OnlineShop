from flask import (flash,
redirect,render_template,url_for,request)
from ..Ceo import Ceo
from .forms import ProductForm
from datetime import datetime
from flask_login import current_user,login_required
from ..models import User,Order,Product
from App import db
from .util import save_img,update_img,clean_bucket
from App.decorators import Ceo_required
from werkzeug.utils import secure_filename as sf




Date=datetime.utcnow()


@Ceo.before_request
@login_required
@Ceo_required
def before_request():
    pass

@Ceo.route('/addproduct',methods=['POST','GET'])
def add_product():
    form=ProductForm()
    if form.validate_on_submit():
        name=form.name.data
        price=form.price.data
        specs=form.specs.data
        img=form.img.data
        if img:
            filename=save_img(img)        
        product=Product(name=name,specs=specs,img=filename,price=price,admin_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash(f'Product {product.name} added Now','info')
    return  render_template('product/add.html',form=form,date=Date,title='Add-Product')


@Ceo.route('/update/<int:id>',methods=['POST','GET'])
def update_product(id):
    flash('Change product\'s','Info')
    product=Product.query.filter_by(id=id).first_or_404()
    form=ProductForm()
    name=form.name.data
    specs=form.specs.data
    new_img=form.img.data
    price=form.price.data
    if form.validate_on_submit():
        product.name=name
        product.specs=specs
        product.img=save_img(new_img)
        product.price=price
        db.session.commit()
        flash('Product is successfully updated','success')
        return redirect(url_for('main.home'))
    form.name.data=product.name
    form.specs.data=product.specs
    form.price.data=product.price
    return  render_template('product/add.html',form=form,date=Date,title='Edit-Product')


@Ceo.route('/clear/bucket',methods=['POST','GET'])
def clear_bucket():
    clean_bucket()
    flash('Image Storage have Been Cleared','danger')
    return redirect(url_for('main.home'))


@Ceo.route('/payments')
def users_payments():
    page=request.args.get('page',type=int)
    pagin=Order.query.filter_by(paid=True).order_by(Order.date_ordered.desc()).\
    paginate(page=page,per_page=10)
    order=pagin.items
    return render_template('payment/init.html',pagin=pagin,
                           order=order,date=Date,title='Paid-Orders')

@Ceo.route('/Admin')
def Admin_page():
    username=current_user.username
    phone=current_user.phonenumber
    return render_template('main/admin.html',users=username,orders=phone,pay=current_user.max_collect(),
                           title='Admin-Panel')


@Ceo.route('/users',methods=['GET'])
def users():
    page=request.args.get('page',type=int)
    pagin=User.query.paginate(page=page,per_page=10)
    users=pagin.items
    return render_template('main/users.html',pagin=pagin,
                           users=users,title='All-Users')

@Ceo.route('/Allorders')
def orders():
    page=request.args.get('page',type=int)
    pagin=Order.query.order_by(Order.date_ordered.desc()).\
    paginate(page=page,per_page=10)
    orders=pagin.items
    return render_template('main/orders.html',pagin=pagin,
                           orders=orders,title='All-Orders')

