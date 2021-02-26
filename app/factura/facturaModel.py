from app import db
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    monto_total = db.Column(db.Float,default=0.0)
    detalles = db.relationship('Detalle', backref='factura', lazy='select')

    def __init__(self, user_id=None,  monto_total=None):
        self.user_id = user_id
        self.monto_total = monto_total

    def __repr__(self):
        return '<Factura %r>' % (self.name)

class Detalle(db.Model):
    __tablename__ = 'detalle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    facturat_id = db.Column(db.Integer, db.ForeignKey('facturas.id'),nullable=False)
    cantidad = db.Column(db.Integer, default=0)


    def __init__(self, product_id=None,facturat_id=None, cantidad=None):
        self.product_id = product_id
        self.facturat_id = facturat_id
        self.cantidad = cantidad

    def __repr__(self):
        return '<Detalle %r>' % (self.name)
