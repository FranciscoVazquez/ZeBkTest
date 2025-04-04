from flask import Flask
from flask_mail import Mail
from comun import constantes
from endpoints.producto_endpoint import producto_bp
from endpoints.usuario_endpoint import usuario_bp
from comun.extensions import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = constantes.DB_CONEXION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.urandom(24) # Clave secreta aleatoria

#Configuracion para el servidor de correo
app.config['MAIL_SERVER'] = constantes.EMAIL_SERVIDOR
app.config['MAIL_PORT'] = constantes.EMAIL_PUERTO  
app.config['MAIL_USE_SSL'] = constantes.EMAIL_USA_SSL 
app.config['MAIL_USERNAME'] = constantes.EMAIL_USUARIO
app.config['MAIL_PASSWORD'] = constantes.EMAIL_CONTRASENIA  

db.init_app(app)
mail = Mail(app)
#Registramos las rutas validas
app.register_blueprint(producto_bp, url_prefix="/productos")
app.register_blueprint(usuario_bp, url_prefix="/usuarios")

if __name__ == 'main':
    with app.app_context():
        db.create_all()
        app.run(debug=True)