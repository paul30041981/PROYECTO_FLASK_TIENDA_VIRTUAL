from app import db
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import datetime
from wtforms import IntegerField
from integer import Integer
from wtforms.validators import DataRequired, NumberRange

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
   
 
    def __init__(self, product_id=None, user_id=None, cantidad=None):
        self.product_id = product_id
        self.user_id = user_id
        self.cantidad = cantidad

    def __repr__(self):
        return '<Carrito %r>' % (self.cantidad)

class CarritoForm(FlaskForm):
    cantidad = IntegerField('Cantidad', 
            validators=[
                DataRequired('Este campo es necesario'),
                NumberRange(min=Integer('1'), max=None, message='Precio debe de ser Mayor a 0')
                ])
