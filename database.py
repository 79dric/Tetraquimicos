import sqlite3

def conectar():
    return sqlite3.connect("catalogo.db")

def crear_tabla():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            descripcion TEXT,
            fuente TEXT
        )
    """)

    conexion.commit()
    conexion.close()
