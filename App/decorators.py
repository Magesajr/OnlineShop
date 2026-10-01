from flask import abort
from functools import wraps
from flask_login import current_user
from App.models import Permision

def permission_needed(perm):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args,**kwargs):
            if not current_user.can(perm):
                abort(403)
            return f(*args,**kwargs)
        return decorated_func
    return decorator


def customer_required(f):
    return permission_needed(Permision.purchase)(f)

def manager_required(f):
    return permission_needed(Permision.manage)(f)

def Ceo_required(f):
    return permission_needed(Permision.supervise)(f)




