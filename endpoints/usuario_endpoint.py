from flask import Blueprint, jsonify, request, current_app, session
from controladores.usuario_controlador import (
    obtener_usuarios, obtener_usuario_por_id, crear_usuario, 
    actualizar_usuario, eliminar_usuario, verificar_admin, 
    verificar_credenciales, verifica_token,
    actualizar_token_usuario
    )

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.before_request
def verificar_sesion():
    if request.endpoint not in ['usuario.login']:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensaje': 'Se requiere token de autorizacion'}), 401
        if not verifica_token(token):
            return jsonify({'mensaje': 'Debes iniciar sesion nuevamente'}), 403
        if not verificar_admin():
            return jsonify({'mensaje': 'No tienes permisos para esta acción'}), 403

@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    usuarios = obtener_usuarios()
    return jsonify(usuarios)

@usuario_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        return jsonify(usuario)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@usuario_bp.route('/', methods=['POST'])
def post_usuario():
    datos_usuario = request.get_json()
    nuevo_usuario = crear_usuario(datos_usuario)
    if nuevo_usuario:
        return jsonify(nuevo_usuario), 201
    else:
        return jsonify({'mensaje': 'El correo electrónico ya existe'}), 400

@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
def put_usuario(usuario_id):
    datos_usuario = request.get_json()
    usuario_actualizado = actualizar_usuario(usuario_id, datos_usuario)
    if usuario_actualizado:
        return jsonify(usuario_actualizado)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
   eliminado = eliminar_usuario(usuario_id)
   if eliminado:
       return jsonify({'mensaje': 'Usuario eliminado'})
   elif eliminado is False:
       return jsonify({'mensaje': 'No puedes eliminarte a ti mismo'}), 400
   else:
       return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@usuario_bp.route('/login', methods=['POST'])
def login():
    datos_login = request.get_json()
    user = verificar_credenciales(datos_login["email"], datos_login["contrasena"])
    if user:
        token = user.generar_token(current_app.config['SECRET_KEY'])
        return jsonify({"mensaje": "Sesion iniciada", "token": token}), 200
    else:
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

@usuario_bp.route('/logout', methods=['POST'])
def logout():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        actualizar_token_usuario(usuario_id, None) 
        session.clear()
        return jsonify({'mensaje': 'Sesión cerrada'})
    else:
        return jsonify({'mensaje': 'No hay sesión iniciada'}), 400