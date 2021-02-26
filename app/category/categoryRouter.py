from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_required
#import proyecto
# from categorysBD import PRODUCTS
from app.category.categoryModel import Category, CategoryForm, Estado
from app import db
# from werkzeug import abort 

# @app.before_request
# @login_required
# def constructor():
#    pass

@app.route('/categories')
@app.route('/category/<int:page>')
@login_required
def categories(page=1):
    return render_template('category/categories.html', categories = Category.query.paginate(page,5))

@app.route('/category_delete/<int:id>')
@login_required
def category_delete(id):
    cat = Category.query.get_or_404(id)#devuelve un objeto
    cat.estado = Estado.Eliminado
    db.session.add(cat)
    db.session.commit()
    flash("Producto cambiado a estado Eliminado con Exito")
    return redirect(url_for('categories'))

@app.route('/category_create', methods=('GET', 'POST'))
@login_required
def category_create():
    
    form = CategoryForm(meta={'csrf':False})
    if form.validate_on_submit():
        p = Category(
            request.form['name'], 
            form.estado.data# Estado.Activado
            )
        db.session.add(p)
        db.session.commit()
        flash("Categoria Creada con Exito")
        return redirect(url_for('category_create'))
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('category/category_create.html', form=form)

@app.route('/category_update/<int:id>', methods=('GET', 'POST'))
@login_required
def category_update(id):
    cat = Category.query.get_or_404(id)
    form = CategoryForm(meta={'csrf':False})

    if request.method == "GET":
        form.name.data = cat.name
        form.estado.data = cat.estado.value

    if form.validate_on_submit():
        cat.name = form.name.data
        cat.estado = form.estado.data
        db.session.add(cat)
        db.session.commit()
        flash("Categoria Actualizada con Exito")
        return redirect(url_for('category_update', id = cat.id ))
    
    if form.errors:
        flash(form.errors, 'danger')
   
    return render_template('category/category_edit.html',cat = cat ,form=form)
