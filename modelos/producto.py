from flask_sqlalchemy import SQLAlchemy
from comun.extensions import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    marca = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.DECIMAL(20, 2), nullable=False, default=0.00)
    fecha_creacion = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    fecha_modificacion = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.now())


    def __init__(self, sku, nombre, marca, descripcion, precio):
        self.sku = sku
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.marca = marca
    
    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'nombre': self.nombre,
            'marca': self.marca,
            'descripcion': self.descripcion,
            'precio': str(self.precio), 
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }
