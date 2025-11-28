# Sistema CRUD de Clientes - ISO9

Sistema completo de gestión de clientes para una empresa de ventas de equipos informáticos, desarrollado con Node.js + Python (API) y Frontend CRUD.

## 🏗️ Arquitectura

- **EC2 Web**: Node.js + Python (API) + Frontend CRUD
- **EC2 DB**: MySQL
- **Acceso**: IP elástica
- **Seguridad**: Comunicación interna entre servidores

## 📋 Características

✅ CRUD completo (Create, Read, Update, Delete)
✅ Datos del cliente: DNI/RUC, Nombre, Apellidos, Teléfono, Correo, Dirección, Estado
✅ Login de usuario completo
✅ MySQL separado en otro EC2
✅ Node.js maneja sesiones (con cookie simple)
✅ Python como API CRUD + Login
✅ Seguridad inter servidores
✅ Animaciones DOM incluidas
✅ Diseño profesional con Tailwind CSS

## 🚀 Instalación

### 1. Configurar Base de Datos (EC2 #2)

Conectarse a tu instancia EC2 de base de datos y ejecutar:

```bash
mysql -u root -p
```

Luego ejecutar el script `database.sql`:

```bash
mysql -u root -p < database.sql
```

O desde MySQL:

```sql
source database.sql;
```

### 2. Configurar Aplicación (EC2 #1)

Clonar o copiar los archivos del proyecto:

```bash
cd /path/to/project
```

Instalar dependencias de Python:

```bash
pip install -r requirements.txt
```

### 3. Configurar Conexión a Base de Datos

Editar el archivo `config.py` y reemplazar `TU_IP_INSTANCIA_EC2_DB` con la IP privada de tu instancia EC2 #2:

```python
DB_HOST = 'TU_IP_PRIVADA_EC2_DB'  # Ejemplo: '172.31.45.123'
DB_USER = 'root'
DB_PASSWORD = 'cristhian3738'
DB_NAME = 'clientedb'
DB_PORT = 3306
```

### 4. Configurar Grupos de Seguridad en AWS

**EC2 #1 (Aplicación):**
- Puerto 5000 (Python Flask) - Abierto al público o tu IP
- Puerto 3000 (Node.js) - Si lo usas

**EC2 #2 (Base de Datos):**
- Puerto 3306 (MySQL) - Solo accesible desde EC2 #1 (usar Security Group de EC2 #1)

### 5. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://TU_IP_PUBLICA:5000`

## 🔑 Credenciales de Prueba

**Usuario:** admin  
**Contraseña:** admin123

## 📁 Estructura del Proyecto

```
CRUD iso9/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración de BD y app
├── requirements.txt       # Dependencias Python
├── database.sql          # Script de inicialización de BD
├── templates/
│   ├── login.html        # Página de login
│   └── index.html        # Página principal CRUD
└── README.md             # Este archivo
```

## 🎨 Características de Diseño

- **Tailwind CSS**: Framework CSS moderno
- **Animaciones DOM**: 
  - fadeIn, slideIn, pulse
  - Efectos hover en botones y tarjetas
  - Transiciones suaves en formularios
  - Animaciones de carga
  - Efectos de escala en inputs

## 🔒 Seguridad

- Sesiones con cookies
- Login requerido para acceder al CRUD
- Comunicación segura entre EC2s usando Security Groups
- Contraseñas (en producción usar hash bcrypt)
- CORS configurado

## 📊 Endpoints API

- `POST /login` - Autenticar usuario
- `GET /logout` - Cerrar sesión
- `GET /clientes` - Obtener todos los clientes
- `GET /clientes/<id>` - Obtener un cliente
- `POST /clientes` - Crear nuevo cliente
- `PUT /clientes/<id>` - Actualizar cliente
- `DELETE /clientes/<id>` - Eliminar cliente
- `GET /test-db` - Probar conexión a BD

## 🧪 Pruebas

### Probar conexión a base de datos:

```bash
curl http://localhost:5000/test-db
```

### Probar login:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 📝 Notas Importantes

1. **IP Privada vs Pública**: Usar IP privada para comunicación entre EC2s
2. **Puertos**: Asegurar que los puertos estén abiertos en Security Groups
3. **Contraseña MySQL**: Cambiar en producción
4. **Secret Key**: Cambiar `SECRET_KEY` en producción
5. **HTTPS**: Implementar SSL/TLS en producción

## 🐛 Troubleshooting

### Error de conexión a MySQL:
- Verificar que MySQL esté corriendo: `systemctl status mysql`
- Verificar Security Groups
- Verificar IP en config.py
- Probar conexión: `telnet IP_EC2_DB 3306`

### Error 401 No autenticado:
- Verificar que hayas iniciado sesión
- Verificar cookies del navegador

### Error al cargar clientes:
- Verificar que la tabla existe: `SHOW TABLES;`
- Verificar datos: `SELECT * FROM clientes;`

## 🎯 Próximas Mejoras

- [ ] Hash de contraseñas con bcrypt
- [ ] Validación de formularios más robusta
- [ ] Paginación de tabla de clientes
- [ ] Búsqueda y filtros
- [ ] Exportar a PDF/Excel
- [ ] Dashboard con estadísticas
- [ ] Logs de auditoría

## 👨‍💻 Autor

Desarrollado para proyecto ISO9 - Sistema de Gestión de Clientes

## 📄 Licencia

Este proyecto es para fines educativos y de demostración.
