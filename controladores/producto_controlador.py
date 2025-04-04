from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.productos_estadisticas import ProductoEstadistica
from comun.extensions import db
from flask_mail import Message
from flask import current_app, session

def obtener_productos():
    productos = Producto.query.all()
    return[producto.to_dict() for producto in productos]

def obtener_producto_por_id(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        return producto.to_dict()
    return None

def crear_producto(datos):
    producto = Producto(
        sku=datos['sku'],
        nombre=datos["nombre"],
        descripcion=datos["descripcion"],
        precio=datos["precio"],
        marca=datos['marca']
        )
    db.session.add(producto)
    db.session.commit()
    enviar_correo_admins(producto,'nuevo')
    return producto.to_dict()

def actualizar_producto(producto_id, datos_producto):
    producto = Producto.query.get(producto_id)
    if producto:
        producto.nombre = datos_producto['nombre']
        producto.descripcion = datos_producto.get('descripcion')
        producto.precio = datos_producto['precio']
        producto.marca = datos_producto['marca']
        db.session.commit()
        enviar_correo_admins(producto,'actualizado')
        return producto.to_dict()
    return None

def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        enviar_correo_admins(producto,'eliminado')
        return True
    return False

def agregar_estadistica_producto(producto_id, ip_address):
    nueva_estadistica = ProductoEstadistica(id_producto=producto_id, ip=ip_address)
    db.session.add(nueva_estadistica)
    db.session.commit()

def enviar_correo_admins(producto, opcion):
    admins = Usuario.query.filter_by(id_rol=1).all()
    id_usuario_activo =  session.get('usuario_id')
    usuario_activo = Usuario.query.get(id_usuario_activo)
    mensaje_usuario = f'Usuario que realizo el cambio: {usuario_activo.id} - {usuario_activo.nombre}'
    if admins:
        correos_admins = [admin.email for admin in admins]
        match opcion:
            case 'nuevo':
                mensaje = f'El producto "{producto.nombre}" con ID {producto.id} ha sido creado. {mensaje_usuario}'
            case 'actualizado':
                mensaje = f'El producto "{producto.nombre}" con ID {producto.id} ha sido actualizado. {mensaje_usuario}'
            case 'eliminado':
                mensaje = f'El producto "{producto.nombre}" con ID {producto.id} ha sido eliminado. {mensaje_usuario}'
        msg = Message(f'Producto {opcion}', sender=current_app.config['MAIL_USERNAME'], recipients=correos_admins)
        msg.body = mensaje
        current_app.extensions['mail'].send(msg)