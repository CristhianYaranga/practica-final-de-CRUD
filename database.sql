-- Script para inicializar la base de datos clientedb
-- Ejecutar este script en tu instancia EC2 con MySQL

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS clientedb;
USE clientedb;

-- Crear tabla de usuarios para el login
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar usuario de prueba (usuario: admin, contraseña: admin123)
INSERT INTO usuarios (username, password, nombre) 
VALUES ('admin', 'admin123', 'Administrador')
ON DUPLICATE KEY UPDATE username=username;

-- Insertar algunos clientes de ejemplo
INSERT INTO clientes (dni, nombre, apellidos, telefono, correo, direccion, estado) VALUES
('12345678', 'Juan', 'Pérez García', '987654321', 'juan.perez@email.com', 'Av. Principal 123, Lima', 'Activo'),
('87654321', 'María', 'López Martínez', '912345678', 'maria.lopez@email.com', 'Jr. Comercio 456, Lima', 'Activo'),
('11223344', 'Carlos', 'Rodríguez Silva', '998877665', 'carlos.rodriguez@email.com', 'Calle Los Pinos 789, Callao', 'Inactivo')
ON DUPLICATE KEY UPDATE dni=dni;

-- Mostrar tablas creadas
SHOW TABLES;

-- Mostrar estructura de la tabla clientes
DESCRIBE clientes;

-- Mostrar estructura de la tabla usuarios
DESCRIBE usuarios;

SELECT 'Base de datos creada exitosamente!' as Mensaje;
