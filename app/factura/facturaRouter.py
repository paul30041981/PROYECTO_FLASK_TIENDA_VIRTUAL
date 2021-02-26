from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required, current_user
#import proyecto
# from categorysBD import PRODUCTS
from app.carrito.carritoModel import Carrito, CarritoForm
from app.factura.facturaModel import Factura, Detalle
from app import db
# from werkzeug import abort 

@app.route('/facturas')
@app.route('/facturas/<int:page>')
@login_required
def facturas(page=1):
    monto_total = 0
    id_usuario = current_user.id
    return render_template('factura/facturas.html', facturas = Factura.query.filter_by(user_id=id_usuario).paginate(page,5))
    
@app.route('/factura_create')
@app.route('/factura_create/<int:id>')
@login_required
def factura_create(id = 0):

    id_usuario = current_user.id
    cars = Carrito.query.filter_by(user_id=id_usuario).all()
    monto_total = 0
    for c in cars:
        monto_total = monto_total + (c.product.price * c.cantidad)
  
    factura = Factura(id_usuario, monto_total)
    db.session.add(factura)
    db.session.commit()

    for c in cars:
        detalle = Detalle(c.product.id, factura.id, c.cantidad)
        db.session.add(detalle)
        db.session.delete(c)

    db.session.commit()

    flash(f'''Compra realizada con exito''',)


    return redirect(url_for('carritos'))

