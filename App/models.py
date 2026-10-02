import os
import secrets
from App import db
from .import manager
from itsdangerous.url_safe import URLSafeTimedSerializer as s
from itsdangerous.exc import BadTimeSignature,BadSignature,SignatureExpired
from flask import current_app,url_for
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime

@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),unique=True,nullable=False)
    phonenumber=db.Column(db.String(255),unique=True,nullable=False)
    address=db.Column(db.String(255),nullable=False)
    orders=db.relationship('Order',backref='user',lazy='dynamic',cascade='all,delete-orphan')
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email in  current_app.config['APP_ADMINS']:
                self.role = Role.query.filter_by(name='Ceo').first()
            else:
                self.role = Role.query.filter_by(default=True).first()
    
    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_CEO(self):
        return self.can(Permision.supervise)
                
    def __repr__(self):
        return f'''User Details
name:{self.username}
email:{self.email}
address:{self.address}
'''


class Unkown(AnonymousUserMixin):
    def can(self,perm):
        return False
    def is_CEO(self):
        return False

manager.anonymous_user=Unkown

class Order(db.Model):
    __tablename__='orders'
    item_id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.String(50))
    item_name=db.Column(db.String(255),nullable=False)
    date_ordered=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    paid=db.Column(db.Boolean,index=True,default=False)
    shipped=db.Column(db.Boolean,index=True,default=False)

    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    product_id=db.Column(db.Integer,db.ForeignKey('products.id'))

    def __init__(self,**kwargs):
        super(Order,self).__init__(**kwargs)
        if self.order_id is None:
            self.order_id = secrets.token_hex(10)
        
    def user_token(self,salt='safe'):
        pin=s(current_app.config['SECRET_KEY'],salt=salt)
        sam=pin.dumps({'token':self.order_id})
        return sam
    
    @staticmethod
    def confirm_token(token,max_age:int):
        key=s(current_app.config['SECRET_KEY'],salt='safe')
        try:
            confirm=key.loads(token,max_age=max_age,salt='safe')
        except BadTimeSignature as e:
            return f'{e}'
        return Order.query.filter_by(order_id=confirm['token']).first()
    
    
    def __repr__(self):
        return f'''Order Details
name:{self.item_name}
date:{self.date_ordered.__format__('%Y,%b-%d %H:%M:%S')}
shipped:{self.shipped}
buyer:{self.user.username}
paid:{self.paid}'''


class Product(db.Model):
    __tablename__='products'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),index=True,nullable=False)
    specs=db.Column(db.String(255),nullable=False)
    price=db.Column(db.Float,nullable=False)
    sold=db.Column(db.Boolean,default=False)
    img=db.Column(db.String(255),index=True)

    orders=db.relationship('Order',backref='product',lazy='dynamic',cascade='all,delete-orphan')

    def __repr__(self):
        return f'''Product Details
name:{self.name}
specs:{self.specs}
price:{self.price}
paid:{self.sold}
image_file:{self.img}'''


class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),index=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permit=db.Column(db.Integer)
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permit == None:
            self.permit = 0

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permit += perm
    
    def remove_permission(self,perm):
        if not self.has_permission(perm):
            self.permit -= perm

    def reset_permission(self):
        self.permit = 0
    
    def has_permission(self,perm):
        return self.permit & perm == perm
    
    @staticmethod
    def setting_roles():
        roles={
            'user':[Permision.browsing],
            'customer':[Permision.browsing,Permision.purchase],
            'Manager':[Permision.browsing,Permision.purchase,Permision.manage],
            'Ceo':[Permision.browsing,Permision.purchase,Permision.manage,Permision.supervise]
        }
        default_role='user'
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default =(role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Permision:
    browsing=1
    purchase=2
    manage=4
    supervise=8


