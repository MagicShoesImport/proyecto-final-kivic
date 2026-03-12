import sqlite3
import hashlib

def hashear_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')
        self.cursor = self.conexion.cursor()
        self.crear_tablas()
    
    def crear_tablas(self):
        # Crea la tabla de usuarios
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT UNIQUE,
                                password TEXT,
                                nombre TEXT,
                                email TEXT,
                                rol TEXT DEFAULT 'empleado')''')
        
        #Crea la tabla de productos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                codigo TEXT UNIQUE,
                                nombre TEXT,
                                descripcion TEXT,
                                cantidad INTEGER,
                                precio REAL,
                                categoria TEXT)''')
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()