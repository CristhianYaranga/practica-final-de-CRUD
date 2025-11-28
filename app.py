from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configurar CORS para permitir solicitudes del frontend
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Configuración de sesión
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=2)

# Configuración de la base de datos
def get_db_connection():
    """Establece conexión con la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
            port=app.config['DB_PORT']
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Ruta principal
@app.route('/')
def index():
    """Página principal con el formulario CRUD"""
    if 'logged_in' not in session:
        return render_template('login.html')
    return render_template('index.html')

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar usuario"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        
        if user:
            session['logged_in'] = True
            session['username'] = username
            session.permanent = True
            return jsonify({'success': True, 'message': 'Login exitoso'})
        else:
            return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401
    except Error as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Ruta de logout
@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada'})

# CREATE - Crear nuevo cliente
@app.route('/clientes', methods=['POST'])
def crear_cliente():
    """Crea un nuevo cliente en la base de datos"""
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    data = request.get_json()
    dni = data.get('dni')
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    correo = data.get('correo')
    direccion = data.get('direccion')
    estado = data.get('estado', 'Activo')
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor()
        query = """INSERT INTO clientes (dni, nombre, apellidos, telefono, correo, direccion, estado) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (dni, nombre, apellidos, telefono, correo, direccion, estado))
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'id': cursor.lastrowid
        }), 201
    except Error as e:
        return jsonify({'success': False, 'message': f'Error al crear cliente: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# READ - Obtener todos los clientes
@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    """Obtiene todos los clientes de la base de datos"""
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
        clientes = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': clientes
        }), 200
    except Error as e:
        return jsonify({'success': False, 'message': f'Error al obtener clientes: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# READ - Obtener un cliente por ID
@app.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    """Obtiene un cliente específico por su ID"""
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
        cliente = cursor.fetchone()
        
        if cliente:
            return jsonify({
                'success': True,
                'data': cliente
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Cliente no encontrado'}), 404
    except Error as e:
        return jsonify({'success': False, 'message': f'Error al obtener cliente: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# UPDATE - Actualizar cliente
@app.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    """Actualiza los datos de un cliente existente"""
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    data = request.get_json()
    dni = data.get('dni')
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    correo = data.get('correo')
    direccion = data.get('direccion')
    estado = data.get('estado')
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor()
        query = """UPDATE clientes 
                   SET dni = %s, nombre = %s, apellidos = %s, telefono = %s, 
                       correo = %s, direccion = %s, estado = %s 
                   WHERE id = %s"""
        cursor.execute(query, (dni, nombre, apellidos, telefono, correo, direccion, estado, id))
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': 'Cliente actualizado exitosamente'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Cliente no encontrado'}), 404
    except Error as e:
        return jsonify({'success': False, 'message': f'Error al actualizar cliente: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# DELETE - Eliminar cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    """Elimina un cliente de la base de datos"""
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': 'Cliente eliminado exitosamente'
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Cliente no encontrado'}), 404
    except Error as e:
        return jsonify({'success': False, 'message': f'Error al eliminar cliente: {str(e)}'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Ruta de prueba de conexión
@app.route('/test-db')
def test_db():
    """Prueba la conexión a la base de datos"""
    connection = get_db_connection()
    if connection:
        if connection.is_connected():
            db_info = connection.get_server_info()
            connection.close()
            return jsonify({
                'success': True,
                'message': f'Conectado exitosamente a MySQL Server versión {db_info}'
            })
    return jsonify({
        'success': False,
        'message': 'Error al conectar con la base de datos'
    }), 500

if __name__ == '__main__':
    # host='0.0.0.0' escucha en todas las interfaces (pública y privada)
    # Para acceso público: usar IP elástica o IP pública de EC2
    # Para acceso interno entre EC2s: usar IP privada
    # Puerto 5000 debe estar abierto en el Security Group
    app.run(host='0.0.0.0', port=5000, debug=True)
