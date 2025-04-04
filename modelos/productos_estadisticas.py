from comun.extensions import db
from datetime import datetime

class ProductoEstadistica(db.Model):
    __tablename__ = 'productos_estadisticas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    fecha = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    ip = db.Column(db.String(20), nullable=False)

    producto = db.relationship('Producto', backref='estadisticas')

    def to_dict(self):
        return {
            'id': self.id,
            'id_producto': self.id_producto,
            'fecha': self.fecha,
            'ip': self.ip
        }