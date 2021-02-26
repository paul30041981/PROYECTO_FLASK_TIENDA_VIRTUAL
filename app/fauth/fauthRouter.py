from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages, session
from sqlalchemy.sql.expression import not_, or_
from flask_login import login_user, logout_user, current_user, login_required

from app.auth.userModel import User, LoginForm, RegisterForm
from app import db, login_manager
# from werkzeug import abort 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/user_create', methods=('GET', 'POST'))
def user_create():
    
    form = RegisterForm(meta={'csrf':False})

    if form.validate_on_submit():

        if User.query.filter_by(username = form.username.data).first():
            flash('El usuario ya existe en el sistema', 'danger')
        else:
            p = User(form.username.data, form.password.data)
            db.session.add(p)
            db.session.commit()
            flash("Usuario Creado con Exito")
            return redirect(url_for('user_create'))
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/user_create.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    pass
    if current_user.is_authenticated:
      flash("Ya estas autenticado")
      return redirect(url_for('productos'))
    
    form = LoginForm(meta={'csrf':False})

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # session['username'] = user.username
            # session['rol'] = user.rol.value
            # session['id'] = user.id
            flash(f"Bienvenido {user.username}")

            # next = request.form['next']
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url(next):
            #   return .abort(400)
            # print(next)
            # return redirect(next or url_for('categories'))
            return redirect(url_for('productos'))
        else:
            flash("Credenciales Incorrectas")
            
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
#    session.pop('username')
#    session.pop('id')
#    session.pop('rol')
    logout_user()
    return redirect(url_for('login'))


# @app.route('/protegido')
# @login_required
# def protegido():
#    return "Vista protegida"