# ZeBkTest API Rest
Zebrand Backend Test

Este proyecto es una API REST hecha con Flask para el Zebrand Backend Test.

## Funcionalidades

* Gestión de usuarios:
    * Creación, actualización, eliminación y obtención de usuarios.
    * Autenticación de usuarios (login/logout) usando JWT.
    * Verificación de roles de administrador.
* Gestión de productos:
    * Creación, actualización, eliminación y obtención de productos.
    * Registro de estadísticas de visitas de productos por usuarios anonimos

## Tecnologías Utilizadas
* Flask
* Flask-SQLAlchemy
* PyMySQL
* bcrypt
* PyJWT

## Requisitos

* Python 3.7+
* MySQL

## Configuración

1.  **Clona el repositorio:**

2.  **Crea un entorno virtual:**

    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**

    * En Windows:

        ```bash
        venv\Scripts\activate
        ```

    * En macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configura la base de datos:**

    * Crea una base de datos MySQL con el nombre que desees.
    * Modifica el archivo `comun/constantes.py` y actualiza la configuración de  la constante `DB_CONEXION` con los detalles de tu base de datos.

6.  **Ejecuta la aplicación:**

    ```bash
    flask run
    ```
7. **Revisa que el servidor se este ejecutando usando**
    * En un ambiente DEV Puedes revisarlo en la liga `http://127.0.0.1:5000/`

8. **Ejecuta pruebas de API usando las colecciones Postman**

## Autor

Francisco Vazquez Ravell