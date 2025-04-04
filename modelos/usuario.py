import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from comun.extensions import db
from .rol import Rol

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.Integer, default=1)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    rol = db.relationship('Rol', backref='usuarios')
    token = db.Column(db.String(500), nullable=True) 

    def __init__(self, nombre, email, contrasena, id_rol, estatus=1):
        self.nombre = nombre
        self.email = email
        self.contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.id_rol = id_rol
        self.estatus = estatus

    def verificar_contrasena(self, contrasena):
        return bcrypt.checkpw(contrasena.encode('utf-8'), self.contrasena.encode('utf-8'))

    def generar_token(self, secret_key):
        payload = {
            'exp': datetime.now() + timedelta(hours=24),
            'iat': datetime.now(),
            'sub': str(self.id)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        db.session.commit()
        self.token = token
        return self.token

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'estatus': self.estatus,
            'id_rol': self.id_rol,
            'rol': self.rol.to_dict() if self.rol else None,
            'token': self.token
        }