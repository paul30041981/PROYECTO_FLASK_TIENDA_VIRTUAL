from functools import wraps
from flask_login import current_user
from flask import redirect, url_for



def administrator(f):
    ## request.method == POST
    @wraps(f)
    def access_administrator(*args, **kwargs):
        user = current_user
        if user.rol.value == "admin" or user.rol.value == "cajero" or  user.rol.value == "almacen" :
            return redirect(url_for('productos'))
        return f(*args, **kwargs)
    return access_administrator
