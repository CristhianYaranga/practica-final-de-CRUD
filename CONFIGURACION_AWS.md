# 🔧 Configuración de IPs en AWS

## 📌 Tipos de IPs en AWS EC2

### 1️⃣ IP Pública
- **Uso**: Para acceder desde Internet
- **Ejemplo**: `54.123.45.678`
- **Características**:
  - Cambia cada vez que reinicias la instancia
  - Accesible desde cualquier lugar con Internet
  - Necesitas IP Elástica si quieres que sea fija

### 2️⃣ IP Privada
- **Uso**: Para comunicación interna entre instancias EC2
- **Ejemplo**: `172.31.45.123` o `10.0.1.50`
- **Características**:
  - No cambia al reiniciar
  - Solo accesible dentro de la VPC de AWS
  - Más rápida y segura para comunicación interna

### 3️⃣ IP Elástica (Elastic IP)
- **Uso**: IP pública fija
- **Características**:
  - No cambia al reiniciar la instancia
  - Puedes asociarla/desasociarla de instancias
  - Es gratis SI está asociada a una instancia en ejecución

---

## 🏗️ Configuración para tu Proyecto

### EC2 #1 (Aplicación Web - Node.js + Python)

#### En `app.py`:
```python
# host='0.0.0.0' escucha en TODAS las interfaces
app.run(host='0.0.0.0', port=5000, debug=True)
```

**¿Qué significa `host='0.0.0.0'`?**
- Escucha en todas las interfaces de red
- Permite acceso desde:
  - IP pública (Internet) → `http://54.123.45.678:5000`
  - IP privada (otras EC2) → `http://172.31.45.123:5000`
  - localhost (dentro de la instancia) → `http://127.0.0.1:5000`

**Alternativas**:
```python
# Solo localhost (no accesible desde fuera)
app.run(host='127.0.0.1', port=5000)

# Solo IP privada
app.run(host='172.31.45.123', port=5000)  # Reemplaza con tu IP privada
```

---

### EC2 #2 (Base de Datos MySQL)

#### En `config.py`:
```python
# ✅ CORRECTO: Usar IP PRIVADA para conexión interna
DB_HOST = '172.31.45.123'  # IP privada de EC2 #2

# ❌ INCORRECTO: No usar IP pública para conexión interna
DB_HOST = '54.123.45.678'  # Más lento y menos seguro
```

**¿Por qué usar IP privada?**
- ✅ Más rápida (red interna de AWS)
- ✅ Más segura (no sale a Internet)
- ✅ Gratis (sin cargos de tráfico)
- ✅ No cambia al reiniciar

---

## 🔒 Configuración de Security Groups

### EC2 #1 (Aplicación Web)

**Inbound Rules (Reglas de Entrada)**:
```
Tipo          Puerto    Origen              Descripción
SSH           22        Tu IP               Acceso SSH
HTTP          80        0.0.0.0/0           Acceso web (opcional)
Custom TCP    5000      0.0.0.0/0           Flask App (o solo tu IP)
Custom TCP    3000      0.0.0.0/0           Node.js (si lo usas)
```

**Outbound Rules (Reglas de Salida)**:
```
Tipo          Puerto    Destino             Descripción
All Traffic   All       0.0.0.0/0           Permitir todas las salidas
```

### EC2 #2 (Base de Datos)

**Inbound Rules (Reglas de Entrada)**:
```
Tipo          Puerto    Origen              Descripción
SSH           22        Tu IP               Acceso SSH
MySQL/Aurora  3306      sg-xxxxx            Solo desde EC2 #1
```

⚠️ **IMPORTANTE**: En "Origen" de MySQL, pon el **Security Group ID** de EC2 #1 (ejemplo: `sg-0123456789abcdef0`)

**Outbound Rules (Reglas de Salida)**:
```
Tipo          Puerto    Destino             Descripción
All Traffic   All       0.0.0.0/0           Permitir todas las salidas
```

---

## 🌐 Cómo Acceder a tu Aplicación

### Desde Internet (Usuarios):
```
http://TU_IP_PUBLICA:5000
o
http://TU_IP_ELASTICA:5000
```

### Desde Otra EC2 (Interna):
```
http://IP_PRIVADA_EC2_1:5000
```

---

## 📋 Pasos de Configuración

### 1. Obtener IPs de tus Instancias

**En AWS Console:**
- Ve a EC2 → Instances
- Selecciona tu instancia
- En la parte inferior verás:
  - **Public IPv4 address**: IP pública (ej: 54.123.45.678)
  - **Private IPv4 addresses**: IP privada (ej: 172.31.45.123)

**Desde terminal SSH en la instancia:**
```bash
# Ver IP privada
hostname -I

# Ver IP pública
curl ifconfig.me
```

### 2. Configurar `config.py`

```python
# Reemplaza con la IP PRIVADA de tu EC2 de base de datos
DB_HOST = '172.31.XX.XXX'  # ← IP privada de EC2 #2
DB_USER = 'root'
DB_PASSWORD = 'cristhian3738'
DB_NAME = 'clientedb'
DB_PORT = 3306
```

### 3. Configurar Security Groups

**EC2 #1:**
1. Ve a EC2 → Security Groups
2. Selecciona el SG de EC2 #1
3. Agrega regla: Puerto 5000, Origen: 0.0.0.0/0 (o solo tu IP para mayor seguridad)

**EC2 #2:**
1. Ve a EC2 → Security Groups
2. Selecciona el SG de EC2 #2
3. Agrega regla: Puerto 3306, Origen: [Security Group ID de EC2 #1]

### 4. Probar Conexión

**Desde EC2 #1, probar conexión a MySQL:**
```bash
# Probar conectividad
telnet IP_PRIVADA_EC2_2 3306

# O con MySQL client
mysql -h IP_PRIVADA_EC2_2 -u root -p
```

---

## 🎯 Ejemplo Completo

### Escenario:
- **EC2 #1**: IP Pública: `54.234.56.78`, IP Privada: `172.31.10.50`
- **EC2 #2**: IP Pública: `54.234.56.99`, IP Privada: `172.31.10.100`

### config.py:
```python
DB_HOST = '172.31.10.100'  # ✅ IP privada de EC2 #2
DB_PASSWORD = 'cristhian3738'
DB_NAME = 'clientedb'
DB_PORT = 3306
```

### Acceder desde navegador:
```
http://54.234.56.78:5000
```

### Security Group EC2 #2:
```
MySQL/Aurora | 3306 | sg-abcd1234 (SG de EC2 #1)
```

---

## ⚠️ Problemas Comunes

### 1. No puedo conectar a MySQL desde EC2 #1
- ✅ Verifica que usas IP privada en `config.py`
- ✅ Verifica Security Group de EC2 #2 permite puerto 3306
- ✅ Verifica que MySQL esté escuchando en todas las interfaces: `bind-address = 0.0.0.0` en `/etc/mysql/mysql.conf.d/mysqld.cnf`

### 2. No puedo acceder a la app desde mi navegador
- ✅ Verifica que el puerto 5000 esté abierto en Security Group de EC2 #1
- ✅ Verifica que la app esté corriendo: `ps aux | grep python`
- ✅ Usa IP pública o IP elástica en el navegador

### 3. La IP pública cambia al reiniciar
- ✅ Solución: Asigna una IP Elástica a tu EC2 #1

---

## 🚀 Producción

Para producción, considera:

1. **Usar IP Elástica** para EC2 #1
2. **Configurar dominio** (ej: `miapp.com`)
3. **Usar HTTPS** con certificado SSL
4. **Usar Nginx** como proxy inverso
5. **Cambiar `debug=False`** en `app.py`
6. **Usar Gunicorn** en vez del servidor de desarrollo de Flask

```python
# Producción
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

---

## 📚 Resumen Rápido

| Concepto | Uso | Ejemplo |
|----------|-----|---------|
| **IP Pública** | Acceso desde Internet | `54.123.45.678` |
| **IP Privada** | Comunicación interna EC2 | `172.31.45.123` |
| **IP Elástica** | IP pública fija | Asignar en AWS Console |
| **`host='0.0.0.0'`** | Escucha en todas las interfaces | En `app.py` |
| **DB_HOST** | Usa IP privada de EC2 #2 | En `config.py` |
| **Puerto 5000** | Abrir en SG de EC2 #1 | Para acceso web |
| **Puerto 3306** | Abrir en SG de EC2 #2 | Solo desde EC2 #1 |
