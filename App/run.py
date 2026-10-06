from App import create_app,db
from flask import current_app
from App.models import User,Order,Product,Role,Permision as perm
from flask_migrate import Migrate
import os,click,sys

base=os.path.abspath(os.path.dirname(__name__))

app=create_app('production')
migrate=Migrate(app,db,directory='production_migrations')

 
@app.shell_context_processor
def shell():
    return dict(
        db=db,user=User,oder=Order,product=Product,role=Role,
    perm=perm)


