from app import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages, session
from sqlalchemy.sql.expression import not_, or_

from app.auth.userModel import User, LoginForm, RegisterForm
from app import db
# from werkzeug import abort 


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

    if 'username' in session:
        print(session['username'])
    
    form = LoginForm(meta={'csrf':False})

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            session['rol'] = user.rol.value
            session['id'] = user.id
            flash(f"Bienvenido {user.username}")
            return redirect(url_for('productos'))
        else:
            flash("Credenciales Incorrectas")
            
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
   session.pop('username')
   session.pop('id')
   session.pop('rol')
   return redirect(url_for('login'))


