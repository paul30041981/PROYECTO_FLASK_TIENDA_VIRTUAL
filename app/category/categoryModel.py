from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
import enum
from sqlalchemy import Enum

class Estado(enum.Enum):
    Activado = 'Activado'
    Desactivado = 'Desactivado'
    Eliminado = 'Eliminado'

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255),  nullable=False)
    estado = db.Column(Enum(Estado))

    products = db.relationship('Product', backref='category', lazy='select')

 
    def __init__(self, name=None, estado=None):
        self.name = name
        self.estado = estado

    def __repr__(self):
        return '<Category %r>' % (self.name)

class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired('Este campo nombre es requerido')])
    estado = SelectField(u'Estado', choices=[ (mp.value, mp.name) for mp in Estado ], default='Activado')
    
