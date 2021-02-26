from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required, current_user
#import proyecto
# from productsBD import PRODUCTS
from app.producto.productoModel import Product, ProductForm, ProductSearchForm, EstadoProducto, CarritoForm
from app.category.categoryModel import Category
from app.carrito.carritoModel import Carrito

from app import db
# from werkzeug import abort 

# @app.before_request
# @login_required
# def constructor():
#    pass

@app.route('/productos')
@app.route('/product/<int:page>')
@login_required
def productos(page=1):

    form = ProductForm(meta={'csrf':False})
    categories = [ (c.id, c.name) for c in Category.query.order_by(Category.name).all() ]
    form.category_id.choices = categories

    return render_template('producto/productos.html', categories=categories, productos = Product.query.order_by(Product.id).paginate(page,5), form = form, cate="", namepro="")

@app.route('/productos_search', methods=('GET', 'POST'))
@app.route('/productos_search/<int:page>', methods=('GET', 'POST'))
@app.route('/productos_search/<int:page>/<int:categoria>', methods=('GET', 'POST'))
@login_required
def productos_search(page=1, categoria=0 ):

    print('categoria',categoria)
    print('page',page)
    form = ProductForm(meta={'csrf':False})
    categories = [ (c.id, c.name) for c in Category.query.order_by(Category.name).all() ]

    if(categoria == 0 ):
        if request.form['category'] == '':
            prod = Product.query.filter(Product.name.like(request.form.get('name') +'%')).order_by(Product.id).paginate(page,5)
        else:
            prod = Product.query.filter(Product.category_id == request.form['category']).filter(Product.name.like(request.form.get('name') +'%')).order_by(Product.id).paginate(page,5)
        cate = request.form['category']
    else:
        prod = Product.query.filter(Product.category_id == categoria).order_by(Product.id).paginate(page,5)
        cate = categoria

    return render_template('producto/productos.html', categories=categories, productos = prod, form = form, cate = cate, namepro=request.form.get('name'))

@app.route('/producto_delete/<int:id>')
@login_required
def producto_delete(id):
    prod = Product.query.get_or_404(id)#devuelve un objeto
    # db.session.delete(prod)
    prod.estado = EstadoProducto.Eliminado
    db.session.add(prod)
    db.session.commit()
    flash("Producto cambiado a estado Eliminado con Exito")
    return redirect(url_for('productos'))

@app.route('/producto_create', methods=('GET', 'POST'))
@login_required
def producto_create():
    
    form = ProductForm(meta={'csrf':False})
    categories = [ (c.id, c.name) for c in Category.query.all() ]
    form.category_id.choices = categories
    perecerero=True
    if form.validate_on_submit():
        # print('perecerero', form.perecerero.false_values) 
        # print('perecerero', form.perecerero)
        # print('perecerero', form.perecerero.__getattribute__('id'))
        # # print('perecerero', request.form.get("name") )
    
        if form.perecerero._value() == 'y':
            perecerero=False

        p = Product(
            request.form['name'], 
            request.form['price'], 
            request.form['category_id'],
            request.form['stock'],
            perecerero,
            request.form['fecha_vencimiento'],
            request.form['descripcion'],
            form.medida.data,
            form.estado.data
            )
        db.session.add(p)
        db.session.commit()
        flash("Producto Creado con Exito")
    
    if form.errors:
        flash(form.errors, 'danger')

    return redirect(url_for('productos'))

@app.route('/producto_update/<int:id>', methods=('GET', 'POST'))
@login_required
def producto_update(id):
    prod = Product.query.get_or_404(id)
    form = ProductForm(meta={'csrf':False})
    categories = [ (c.id, c.name) for c in Category.query.all() ]
    form.category_id.choices = categories
    perecerero=True

    if form.validate_on_submit():
            
        if form.perecerero._value() == 'y': perecerero=False

        prod.name = form.name.data
        prod.price = form.price.data
        prod.category_id = form.category_id.data
        prod.stock = form.stock.data
        prod.perecerero = perecerero
        prod.fecha_vencimiento = form.fecha_vencimiento.data
        prod.descripcion = form.descripcion.data
        prod.medida = form.medida.data
        prod.estado = form.estado.data
        db.session.add(prod)
        db.session.commit()
        flash("Producto Actualizado con Exito")
    
    if form.errors:
        flash(form.errors, 'danger')
   
    return redirect(url_for('productos'))


@app.route('/detalle/<int:id>')
@login_required
def detalle(id):
    prod = Product.query.get(id)
    prod = Product.query.get_or_404(id)
    return render_template("producto/detalle.html", prod = prod)

@app.route('/producto_seleccionado', methods=('GET', 'POST'))
@app.route('/producto_seleccionado/<int:id>', methods=('GET', 'POST'))
@login_required
def producto_seleccionado(id = 0,page=0):
# def producto_seleccionado(id = 0, cantidad_carrito=0,page=0):

    categories = Category.query.order_by(Category.name).all()
    prod = Product.query.get_or_404(id)#devuelve un objeto
    cantidad = request.args.get("cantidad_carrito")
    print(cantidad)
    if cantidad and len(cantidad) == 0:
        flash(f'''Error: No se Agrego al Carrito porque no se ingreso la cantidad''', 'danger')
    elif int(cantidad) <= 0:
        flash(f'''Error: No se Agrego al Carrito porque la Cantidad debe de ser mayor a cero''', 'danger')
    elif int(cantidad) > int(prod.stock):
        flash(f'''Error: No se Agrego al Carrito porque la Cantidad Ingresada es mayor al Stock disponible''', 'danger')
    else:
        id_usuario = current_user.id
        p = Carrito(
            id, 
            id_usuario, 
            cantidad
            )
        db.session.add(p)
        db.session.commit()
    flash(f"Producto {prod.name} Agregado al Carrito")

    return redirect(url_for('productos'))



 


# @app.route('/producto_insert', methods=["POST"])
# def producto_insert():
#     p = Product(request.form['name'], request.form['price'])
#     db.session.add(p)
#     db.session.commit()
#     flash("Producto Creado con Exito")
#     return redirect(url_for('producto_create'))

# @app.route('/producto_edit/<int:id>')
# def producto_edit(id):
#     # print(get_flashed_messages())
#     prod = Product.query.get_or_404(id)
#     return render_template('producto/producto_edit.html', prod = prod)

# @app.route('/test')
# def test():
#     # prod = Product.query.limit(2).all()
#     # print(prod)
#     # prod = Product.query.limit(2).first()
#     # print(prod)
#     # prod = Product.query.order_by(Product.id).limit(2).all()
#     # print(prod)
#     # prod = Product.query.order_by(Product.id.desc()).limit(2).all()
#     # print(prod)
#     # prod = Product.query.get({"id":1})
#     # print(prod)
#     # prod = Product.query.filter_by(name="producto 1").all()#devuelve una coleccion de un objeto
#     # print(prod)
#     # prod = Product.query.filter_by(name="producto 1", id=1).first()#devuelve un objeto
#     # print(prod)
#     # prod = Product.query.filter_by(name="producto 1").first()#devuelve un objeto
#     # print(prod)
#     # prod = Product.query.filter(Product.id > 1 ).all()#devuelve un objeto, para operadores < y > se debe de usar filter y no filter_by
#     # print(prod)
#     # prod = Product.query.filter(Product.id > 1 ).all()#devuelve un objeto, para operadores < y > se debe de usar filter y no filter_by
#     # print(prod)
#     # prod = Product.query.filter(Product.name.like('prod%') ).all()#devuelve un objeto, para operadores < y > se debe de usar filter y no filter_by
#     # print(prod)
#     # prod = Product.query.filter(not_(Product.id > 1 )).all()#devuelve un objeto, para operadores < y > se debe de usar filter y no filter_by
#     # print(prod)
#     # prod = Product.query.filter(or_(Product.id > 1, Product.name=="producto 2")).all()
#     # print(prod)

#     # #Agregar
#     # p = Product("Iphone", 50.5)
#     # db.session.add(p)
#     # db.session.commit()

#     # #Actualizar
#     # prod = Product.query.filter_by(name="producto 1").first()#devuelve un objeto
#     # prod.name = "UP1"
#     # db.session.add(prod)
#     # db.session.commit()

#     # #Eliminar
#     prod = Product.query.filter_by(name="UP1").first()#devuelve un objeto
#     db.session.delete(prod)
#     db.session.commit()

# @app.route('/productos')
# def productos():
#     # print(PRODUCTS.items())
#     # print(PRODUCTS.get(1))
#     print(Product.query.all())
#     # return render_template('producto/productos.html', productos = PRODUCTS)
#     return render_template('producto/productos.html', productos = Product.query.all())

#     return "Flask"