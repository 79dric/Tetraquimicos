
import sqlite3

def conectar():
    return sqlite3.connect("catalogo.db")


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            principio_activo TEXT,
            concentracion TEXT,
            presentacion TEXT,
            fabricante TEXT,
            descripcion TEXT,
            fuente TEXT
        )
    """)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tabla()
    print("Base de datos creada correctamente.")

