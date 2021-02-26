from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, EqualTo
import enum
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash,check_password_hash

class RolUser(enum.Enum):
    admin='admin'
    cajero='cajero'
    almacen='almacen'
    consulta='consulta'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255),  nullable=False)
    pwhash = db.Column(db.String(300),  nullable=False)
    rol = db.Column(Enum(RolUser))
    carritos = db.relationship('Carrito', backref='user', lazy='select')
    factura = db.relationship('Factura', backref='user', lazy='select')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username=None, pwhash=None, rol=RolUser.consulta):
        self.username = username
        self.pwhash = generate_password_hash(pwhash)
        self.rol = rol

    def __repr__(self):
        return '<User %r>' % (self.username)
    
    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(255),  nullable=False)
#     pwhash = db.Column(db.String(300),  nullable=False)
#     rol = db.Column(Enum(RolUser))

 
#     def __init__(self, username=None, pwhash=None, rol=RolUser.consulta):
#         self.username = username
#         self.pwhash = generate_password_hash(pwhash)
#         self.rol = rol

#     def __repr__(self):
#         return '<User %r>' % (self.username)
    
#     def check_password(self, password):
#         return check_password_hash(self.pwhash, password)

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired('Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[InputRequired('Este campo es requerido')])
    # next = HiddenField('next')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired('Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[InputRequired(), EqualTo('confirm', message='Contraseñas deben de ser Iguales')])
    confirm = PasswordField('Repetir Contraseña', validators=[InputRequired('Este campo es requerido')])

class ChangePassword(FlaskForm):
    password = PasswordField('Nueva Contraseña', [InputRequired(), EqualTo('confirm', message='Contraseñas deben de ser Iguales')])
    confirm  = PasswordField('Repetir Contraseña')