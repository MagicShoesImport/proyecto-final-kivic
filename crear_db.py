import sqlite3
try:
    conn = sqlite3.connect('inventario.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, password TEXT NOT NULL, nombre TEXT NOT NULL, email TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo TEXT UNIQUE NOT NULL, nombre TEXT NOT NULL, descripcion TEXT, cantidad INTEGER DEFAULT 0, precio REAL DEFAULT 0.0, categoria TEXT, fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()
    print('Base de datos inventario.db creada correctamente.')
except Exception as e:
    print(f'Error al crear la base de datos: {e}')
