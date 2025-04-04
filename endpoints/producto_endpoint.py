from flask import Blueprint, jsonify, request, session
from controladores.producto_controlador import (
    obtener_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
    agregar_estadistica_producto
)
from controladores.usuario_controlador import verifica_token, verificar_admin

producto_bp = Blueprint('producto', __name__)

@producto_bp.before_request
def verificar_sesion():
    if request.endpoint not in ['producto.get_productos', 'producto.get_producto']:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensaje': 'Se requiere token de autorizacion'}), 401
        if request.endpoint in ['producto.post_producto', 'producto.put_producto', 'producto.delete_producto']:
            if not verifica_token(token):
                return jsonify({'mensaje': 'Debes inciar nuevamente sesion'}), 403
            if not verificar_admin():
                return jsonify({'mensaje': 'No tienes permisos para esta acción'}), 403


@producto_bp.route('/', methods=['GET'])
def get_productos():
    productos = obtener_productos()
    return jsonify(productos)

@producto_bp.route('/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if producto:
        #Solo agregar estadistica si no hay sesion de usuario iniciada
        if 'usuario_id' not in session:
            agregar_estadistica_producto(producto_id, request.remote_addr) # Agrega la estadística
        return jsonify(producto)
    return jsonify({'mensaje': 'Producto no encontrado'}), 404

@producto_bp.route('/', methods=['POST'])
def post_producto():
    datos_producto = request.get_json()
    nuevo_producto = crear_producto(datos_producto)
    return jsonify(nuevo_producto), 201

@producto_bp.route('/<int:producto_id>', methods=['PUT'])
def put_producto(producto_id):
    datos_producto = request.get_json()
    producto_actualizado = actualizar_producto(producto_id, datos_producto)
    if producto_actualizado:
        return jsonify(producto_actualizado)
    return jsonify({'mensaje': 'Producto no encontrado'}), 404

@producto_bp.route('/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    eliminado = eliminar_producto(producto_id)
    if eliminado:
        return jsonify({'mensaje': 'Producto eliminado'})
    return jsonify({'mensaje': 'Producto no encontrado'}), 404