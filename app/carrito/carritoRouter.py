from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required, current_user
#import proyecto
# from categorysBD import PRODUCTS
from app.carrito.carritoModel import Carrito, CarritoForm
from app import db
# from werkzeug import abort 

# @app.before_request
# @login_required
# def constructor():
#    pass

@app.route('/carritos')
@app.route('/carrito/<int:page>')
@login_required
def carritos(page=1):
    monto_total = 0
    id_usuario = current_user.id
    cars = Carrito.query.filter_by(user_id=id_usuario).all()
    for c in cars:
        monto_total = monto_total + (c.product.price * c.cantidad)
    return render_template('carrito/carritos.html', carritos = Carrito.query.paginate(page,5), total=monto_total)

@app.route('/carrito_delete/<int:id>')
@login_required
def carrito_delete(id):
    cat = Carrito.query.get_or_404(id)#devuelve un objeto
    db.session.delete(cat)
    db.session.commit()
    flash("Categoria Eliminada con Exito")
    return redirect(url_for('carritos'))
