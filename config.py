import os

class Config:
    """Configuración de la aplicación Flask y base de datos"""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de MySQL
    # IMPORTANTE: Cambiar DB_HOST por la IP de tu instancia EC2 de base de datos
    DB_HOST = os.environ.get('DB_HOST') or '54.198.164.17'  # Cambia esto por la IP de tu EC2 #2
    DB_USER = os.environ.get('DB_USER') or 'admin'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'cristhian3738'
    DB_NAME = os.environ.get('DB_NAME') or 'clientedb'
    DB_PORT = int(os.environ.get('DB_PORT') or 3306)
    
    # Configuración de CORS
    CORS_HEADERS = 'Content-Type'
