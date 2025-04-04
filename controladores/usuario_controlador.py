from modelos.usuario import Usuario
from comun.extensions import db
from flask import session, current_app
from comun import constantes
import bcrypt
import jwt

def obtener_usuarios():
    usuarios = Usuario.query.all()
    return [usuario.to_dict() for usuario in usuarios]

def obtener_usuario_por_id(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        return usuario.to_dict()
    return None

def crear_usuario(datos_usuario):
    # Verificamos si el correo electrónico ya existe
    usuario_existente = Usuario.query.filter_by(email=datos_usuario['email']).first()
    if usuario_existente:
        return None  

    nuevo_usuario = Usuario(
        nombre=datos_usuario['nombre'],
        email=datos_usuario['email'],
        contrasena=datos_usuario['contrasena'], 
        id_rol=datos_usuario['id_rol'],
        estatus=datos_usuario.get('estatus', 1)
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario.to_dict()

def actualizar_usuario(usuario_id, datos_usuario):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.nombre = datos_usuario['nombre']
        usuario.email = datos_usuario['email']
        usuario.id_rol = datos_usuario['id_rol']
        usuario.estatus = datos_usuario.get('estatus', usuario.estatus)
        if 'contrasena' in datos_usuario: # Solo cambiamos si nos la envian
            usuario.contrasena = bcrypt.hashpw(datos_usuario['contrasena'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.session.commit()
        return usuario.to_dict()
    return None

def eliminar_usuario(usuario_id):
     # Verificamos si el usuario logueado no se elimine a si mismo
    if 'usuario_id' in session and session['usuario_id'] == usuario_id:
        return False  

    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False

def verifica_token(token):
    try:
        payload = jwt.decode( jwt= token, key = current_app.config['SECRET_KEY'], algorithms=['HS256'])
        usuario = Usuario.query.get(payload['sub'])
        session[constantes.SESSION_USUARIO_ID] = usuario.id
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def verificar_admin():
    usuario = Usuario.query.get(session.get(constantes.SESSION_USUARIO_ID))
    if usuario and usuario.id_rol == constantes.ROL_ADMINISTRADOR:
            return True
    return False

def verificar_credenciales(email, contrasena):
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and usuario.verificar_contrasena(contrasena):
        return usuario
    return None

def actualizar_token_usuario(usuario_id, nuevo_token):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.token = nuevo_token
        db.session.commit()
        return True
    return False