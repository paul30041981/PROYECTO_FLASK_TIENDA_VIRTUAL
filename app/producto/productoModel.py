from app import db
from datetime import datetime
from decimal import Decimal
from integer import Integer
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField ,SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange,Optional
import enum
from sqlalchemy import Enum

class MedidaProducto(enum.Enum):
    Litros = 'Litros'
    Kilos = 'Kilos'
    Caja = 'Caja'
    Paquete = 'Paquete'
    Articulo = 'Articulo'

class EstadoProducto(enum.Enum):
    Activado = 'Activado'
    Desactivado = 'Desactivado'
    Eliminado = 'Eliminado'

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255),  nullable=False)
    price = db.Column(db.Float,default=0.0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)
    stock = db.Column(db.Integer, default=0)
    medida = db.Column(Enum(MedidaProducto))
    estado = db.Column(Enum(EstadoProducto))
    perecerero = db.Column(db.Boolean)
    fecha_vencimiento = db.Column(db.Date, default=None)
    descripcion = db.Column(db.Text(), default=None)
    carritos = db.relationship('Carrito', backref='product', lazy='select')
    detalles = db.relationship('Detalle', backref='product', lazy='select')

 
    def __init__(self, name=None, price=None, category_id=None, stock=None, perecerero=None, fecha_vencimiento=None, descripcion=None, medida=None, estado=None):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.stock = stock
        self.perecerero = perecerero
        self.fecha_vencimiento = fecha_vencimiento
        self.descripcion = descripcion
        self.medida = medida
        self.estado = estado




    def __repr__(self):
        return '<Product %r>' % (self.name)

class ProductForm(FlaskForm):

    name = StringField('Nombre', validators=[DataRequired('Este campo nombre es requerido')])
    price = DecimalField('Precio S/.', 
                validators=[
                    DataRequired('Este campo precio es requerido'),
                    NumberRange(min=Decimal('0.0'), max=None, message='Precio debe de ser Mayor a 0')
                ])
    category_id = SelectField(u'Categoria', coerce=int, validators=[DataRequired('Este campo cantidad es requerido')])
    stock = IntegerField('Stock', 
                validators=[
                    DataRequired('Este campo cantidad es requerido'),
                    NumberRange(min=Integer('0'), max=None, message='Precio debe de ser Mayor a 0')
                ])
    medida = SelectField(u'Unidad de Medida', choices=[ (mp.value, mp.name) for mp in MedidaProducto ],
                validators=[
                    DataRequired('Este campo cantidad es requerido')])
    estado = SelectField(u'Estado', choices=[ (mp.value, mp.name) for mp in EstadoProducto ], default='Activado')
    perecerero = BooleanField('Perecerero', false_values={False, 'false', ''})
    # perecerero = BooleanField('Perecerero')
    fecha_vencimiento = DateField('Fecha Vencimiento', validators=[DataRequired('Este campo es requerido')])
    descripcion = TextAreaField('Descripcion', validators=[DataRequired('Este campos es necesario')])


class CarritoForm(FlaskForm):
    name = StringField('Nombre')
    price = DecimalField('Precio S/.')
    category_id = SelectField(u'Categoria', coerce=int)
    stock = IntegerField('Stock')
    medida = SelectField(u'Unidad de Medida', choices=[ (mp.value, mp.name) for mp in MedidaProducto ])
    estado = SelectField(u'Estado', choices=[ (mp.value, mp.name) for mp in EstadoProducto ], default='Activado')
    perecerero = BooleanField('Perecerero', false_values={False, 'false', ''})
    fecha_vencimiento = DateField('Fecha Vencimiento')
    descripcion = TextAreaField('Descripcion')
    cantidad = IntegerField('Cantidad', 
                validators=[
                    DataRequired('Este campo es necesario'),
                    NumberRange(min=Integer('1'), max=None, message='Precio debe de ser Mayor a 0')
                    ])

    # submit = SubmitField('Conectarse')

class ProductSearchForm(FlaskForm):
    name = StringField('Nombre')
    # category_id = SelectField(u'Categoria', coerce=int)
    # submit = SubmitField('Conectarse')